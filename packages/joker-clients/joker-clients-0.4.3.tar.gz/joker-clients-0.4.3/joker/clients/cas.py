#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import os
import typing
import zipfile
import zlib
from dataclasses import dataclass
from functools import cached_property
from urllib.parse import urljoin

import requests
from volkanic.errors import TechnicalError

from joker.clients import utils
from joker.clients.utils import Pathlike


class MemberFile(typing.TypedDict):
    cid: str
    filename: str


@dataclass
class _CASClientBase:
    inner_url: str
    outer_url: str = None

    def __post_init__(self):
        utils.ensure_url_root(self.inner_url)
        if self.outer_url is None:
            self.outer_url = self.inner_url
        else:
            utils.ensure_url_root(self.outer_url)

    @cached_property
    def session(self):
        # note: requests.session() is deprecated; use cap S
        return requests.Session()

    def save(self, content: bytes) -> str:
        raise NotImplementedError

    def load(self, cid: str) -> None | bytes:
        raise NotImplementedError

    def upload(self, path: Pathlike):
        content = open(path, "rb").read()
        return self.save(content)

    def download(self, cid: str, path: Pathlike):
        rand_hex = os.urandom(8).hex()
        tmp_path = f"{path}.{rand_hex}.tmp"
        with open(tmp_path, "wb") as fout:
            fout.write(self.load(cid))
        os.rename(tmp_path, path)


@dataclass
class ContentAddressedStorageClient(_CASClientBase):
    inner_url: str
    outer_url: str = None

    def save(self, content: bytes) -> str:
        url = urljoin(self.inner_url, "files")
        resp = self.session.post(url, files={"file": content})
        return resp.json()["data"]

    def load(self, cid: str) -> None | bytes:
        url = urljoin(self.inner_url, f"files/{cid}")
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.content
        if resp.status_code == 404:
            return
        raise TechnicalError(f"got response status code {resp.status_code}")

    def load_text(self, cid: str) -> None | str:
        content = self.load(cid)
        if not content:
            return
        return zlib.decompress(content, wbits=31).decode("utf-8")

    def save_text(self, text: str) -> str:
        content = zlib.compress(text.encode("utf-8"), wbits=31)
        return self.save(content)

    def get_outer_url(self, cid: str, filename: str):
        if filename.startswith("."):
            url = f"files/{cid}{filename}"
        else:
            url = f"files/{cid}?filename={filename}"
        return urljoin(self.outer_url, url)

    def create_archive(self, path: Pathlike, memberfiles: list[MemberFile]):
        with zipfile.ZipFile(path, "w") as zipf:
            for m in memberfiles:
                content = self.load(m["cid"])
                with zipf.open(m["filename"], "w") as fout:
                    fout.write(content)


@dataclass
class CascadisClient(_CASClientBase):
    inner_url: str
    outer_url: str = None

    def save(self, content: bytes) -> str:
        url = urljoin(self.inner_url, "cascadis/files")
        resp = self.session.post(url, files={"file": content})
        return resp.json()["data"]

    def load(self, cid: str) -> None | bytes:
        url = urljoin(self.inner_url, f"cascadis/content/{cid}")
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.content
        if resp.status_code == 404:
            return
        raise TechnicalError(f"got response status code {resp.status_code}")

    def fmt_outer_url(self, cid: str, filename: str, short=False):
        prefix = "cas/c" if short else "cascadis/content"
        if filename.startswith("."):
            url = f"{prefix}/{cid}{filename}"
        else:
            url = f"{prefix}/{cid}?filename={filename}"
        return urljoin(self.outer_url, url)
