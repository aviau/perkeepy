import base64
from typing import Protocol

import boto3
import click

from perkeepy.blob import Ref
from perkeepy.blobserver.s3 import S3
from perkeepy.blobserver.s3 import S3Client


@click.group()
@click.option("--bucket", type=str, required=True)
@click.pass_context
def cli(ctx: click.Context, *, bucket: str) -> None:
    s3_client: S3Client = boto3.client("s3")
    blobserver = S3(s3_client=s3_client, bucket=bucket)
    ctx.obj = blobserver


@cli.command("list")
@click.pass_obj
def list_(blobserver: S3) -> None:
    for ref in blobserver.enumerate_blobs():
        click.echo(ref.to_str())


@cli.command("get")
@click.option("--ref", type=str, required=True)
@click.pass_obj
def get(blobserver: S3, *, ref: str) -> None:
    ref_: Ref = Ref.from_str(ref)
    blob = blobserver.fetch(ref_)

    if blob.is_utf8():
        click.echo(blob.get_bytes().decode("utf-8"))
    else:
        click.echo(base64.b64encode(blob.get_bytes()))


if __name__ == "__main__":
    cli()
