import os
import time
import uuid
from typing import List, Optional

import boto3


def _lines_from_blocks(blocks: List[dict]) -> List[str]:
    # Textract returns many block types; we only want recognized lines.
    lines = []
    for b in blocks:
        if b.get("BlockType") == "LINE":
            txt = b.get("Text")
            if txt:
                lines.append(txt)
    return lines


def _detect_document_text_bytes(textract_client, file_bytes: bytes) -> str:
    resp = textract_client.detect_document_text(Document={"Bytes": file_bytes})
    blocks = resp.get("Blocks", [])
    lines = _lines_from_blocks(blocks)
    return "\n".join(lines)


def _start_text_detection_s3(
    textract_client,
    s3_client,
    bucket: str,
    key: str,
) -> str:
    job = textract_client.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    job_id = job["JobId"]

    # Poll until job completes
    while True:
        res = textract_client.get_document_text_detection(JobId=job_id, MaxResults=1000)
        status = res.get("JobStatus")
        if status in {"SUCCEEDED", "FAILED"}:
            if status == "FAILED":
                raise RuntimeError(f"Textract job failed: {job_id}")
            break
        time.sleep(2)

    # Pagination for blocks
    blocks = []
    next_token: Optional[str] = None
    while True:
        if next_token:
            res = textract_client.get_document_text_detection(
                JobId=job_id, MaxResults=1000, NextToken=next_token
            )
        else:
            res = textract_client.get_document_text_detection(JobId=job_id, MaxResults=1000)

        blocks.extend(res.get("Blocks", []))
        next_token = res.get("NextToken")
        if not next_token:
            break

    return "\n".join(_lines_from_blocks(blocks))


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF using AWS Textract.

    Env vars:
      - AWS_REGION (required)
      - TEXTRACT_S3_BUCKET (required only for PDFs larger than ~5MB)
    """
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if not region:
        raise RuntimeError("Missing AWS_REGION (or AWS_DEFAULT_REGION) for Textract")

    use_creds = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }
    # Let boto3 default credential chain work if keys are not provided.
    creds_provided = bool(use_creds["aws_access_key_id"] and use_creds["aws_secret_access_key"])

    client_kwargs = {"region_name": region}
    if creds_provided:
        client_kwargs.update(use_creds)

    textract = boto3.client("textract", **client_kwargs)
    s3 = boto3.client("s3", **client_kwargs)

    max_bytes = 5 * 1024 * 1024  # Textract detect_document_text Bytes limit (commonly 5MB)
    with open(file_path, "rb") as f:
        data = f.read()

    if len(data) <= max_bytes:
        return _detect_document_text_bytes(textract, data)

    bucket = os.getenv("TEXTRACT_S3_BUCKET")
    if not bucket:
        raise RuntimeError(
            "PDF is larger than Textract Bytes limit; set TEXTRACT_S3_BUCKET to use async Textract."
        )

    # Upload temporarily to S3
    key = f"textract-temp/{uuid.uuid4().hex}/{os.path.basename(file_path)}"
    s3.upload_file(file_path, bucket, key)

    try:
        return _start_text_detection_s3(textract, s3, bucket, key)
    finally:
        # Best-effort cleanup
        try:
            s3.delete_object(Bucket=bucket, Key=key)
        except Exception:
            pass

