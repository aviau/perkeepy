from typing import Protocol

import boto3
import click

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


if __name__ == "__main__":
    cli()
