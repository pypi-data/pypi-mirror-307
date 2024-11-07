import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Annotated, Any, List, Optional
from urllib.parse import urljoin

import requests
import typer
from jose import jwt
from md2weasypdf import Article, Printer, extensions

Printer.enabled_extensions = lambda article: [
    extensions.FootnoteExtension(),
    extensions.TableExtension(),
    extensions.ToaExtension(),
    extensions.AbbrExtension(),
    extensions.TocExtension(toc_depth=article.meta.get("toc_depth", "2-6")),
    extensions.SubscriptExtension(),
    extensions.TextboxExtension(),
    extensions.CheckboxExtension(),
    extensions.FencedCodeExtension(),
    extensions.MermaidExtension(),
    extensions.TableCaptionExtension() if article.meta.get("table_caption", True) else None,
    extensions.GridTableExtension(),
    extensions.SaneListExtension(),
]


class GhostClient:
    class RequestError(Exception):
        def __init__(self, response: requests.Response):
            self.response = response

    def __init__(self, base_url: str, token: str, tags: List[str], meta: Optional[dict[str, Any]] = None):
        self.base_url = base_url

        id, secret = token.split(':')
        iat = int(datetime.now().timestamp())
        self.token = jwt.encode(
            {'iat': iat, 'exp': iat + 5 * 60, 'aud': '/admin/'},
            bytes.fromhex(secret),
            algorithm='HS256',
            headers={'alg': 'HS256', 'typ': 'JWT', 'kid': id},
        )

        self.tags = tags
        self.meta = meta or {}

    def _request(self, method: str, url: str, params: Optional[dict] = None, json: Optional[Any] = None):
        response = requests.request(
            method=method,
            url=urljoin(self.base_url, "/ghost/api/admin/" + url),
            params=params,
            json=json,
            headers={
                "Authorization": f"Ghost {self.token}",
                "Accept-Version": "v5.94.0",
            },
        )
        if not response.ok:
            raise self.RequestError(response)

        return response

    def _post_data(self, article: Article, updated_at: Optional[str] = None):
        authors = re.findall(r"<([^@]+@[^>]+)>", str(subprocess.check_output(["git", "shortlog", "-s", "-e", "HEAD", "--", article.source]), "utf-8"))
        html_suffix = ""

        meta = self.meta | article.meta

        if meta.get("watermark"):
            html_suffix += f"""
            <!--kg-card-begin: html-->
            <style>
            .gh-content {{
                background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' height='150px' width='150px'><text transform='translate(40, 120) rotate(-45)' fill='rgba(0, 0, 0, 0.05)' font-weight='bold' font-size='30' font-family='sans-serif'>{meta.get("watermark")}</text></svg>");
                background-position: center center;
            }}
            </style>
            <!--kg-card-end: html-->
            """

        return {
            "posts": [
                {
                    "title": article.title + (f" - {article.alt_title}" if article.alt_title else ""),
                    "slug": article.filename.lower(),
                    "authors": authors,
                    "updated_at": updated_at,
                    "html": article.content + html_suffix,
                    "tags": self.tags,
                }
            ]
        }

    def get_post(self, slug: str):
        try:
            return self._request("GET", f"posts/slug/{slug}/").json()["posts"][0]

        except self.RequestError:
            return

    def update_post(self, post_id: str, article: Article, updated_at: str):
        return self._request("PUT", f"posts/{post_id}/", params={"source": "html"}, json=self._post_data(article, updated_at)).json()["posts"][0]

    def create_post(self, article: Article):
        return self._request("POST", "posts/", params={"source": "html"}, json=self._post_data(article)).json()["posts"][0]

    def create_or_update_post(self, article: Article):
        post = self.get_post(article.filename.lower())
        if post:
            post = self.update_post(post['id'], article, updated_at=post['updated_at'])

        else:
            post = self.create_post(article)

        return post


def main(
    base_url: str,
    token: str,
    input: Path,
    tags: List[str],
    meta: Annotated[
        Optional[str],
        typer.Option(help="Metadata for document generation passed to the layout, pass values using a JSON object"),
    ] = None,
):
    client = GhostClient(base_url, token, tags, meta=json.loads(meta) if meta else None)
    printer = Printer(input, output_dir=Path("."))

    for article in printer.get_articles():
        client.create_or_update_post(article)

        print(f"Updated {article.title} at {base_url}/{article.filename.lower()}")


if __name__ == "__main__":
    typer.run(main)
