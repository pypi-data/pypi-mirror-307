import shutil
from hashlib import file_digest
from pathlib import Path

import requests

from dpkit.models import (
    Analysis,
    File,
    FileSet,
    FileSetRequest,
    Module,
    ModuleList,
    State,
    Upload,
    UploadRequest,
    User,
)


class Client:
    def __init__(self, session):
        self.session = session

    def check(self, r):
        if r.status_code >= 500:
            raise RuntimeError(f"{r.status_code} {r.content}")
        if r.status_code >= 400:
            payload = r.json()
            details = payload["detail"]
            raise RuntimeError(f"{r.status_code} {details}")
        return r

    def me(self) -> User:
        r = self.check(self.session.get("/me"))
        return User.model_validate(r.json())

    def new_upload(self, request) -> Upload:
        p = request.model_dump()
        r = self.check(self.session.post("/upload", json=p))
        return Upload.model_validate(r.json())

    def get_upload(self, id) -> Upload:
        r = self.check(self.session.get(f"/upload/{id}"))
        return Upload.model_validate(r.json())

    def complete_upload(self, id) -> Upload:
        r = self.check(self.session.post(f"/upload/{id}/complete"))
        return Upload.model_validate(r.json())

    def new_fileset(self, request) -> FileSet:
        p = request.model_dump()
        r = self.check(self.session.post("/fileset", json=p))
        return FileSet.model_validate(r.json())

    def get_fileset(self, id) -> FileSet:
        r = self.check(self.session.get(f"/fileset/{id}"))
        return FileSet.model_validate(r.json())

    def get_fileset_download(self, id) -> FileSet:
        r = self.check(self.session.get(f"/fileset/{id}/download"))
        return FileSet.model_validate(r.json())

    def get_modules(self) -> ModuleList:
        r = self.check(self.session.get("/module"))
        return ModuleList.model_validate(r.json())

    def get_module(self, id) -> Module:
        r = self.check(self.session.get(f"/module/{id}"))
        return Module.model_validate(r.json())

    def new_analysis(self, request) -> Analysis:
        p = request.model_dump()
        r = self.check(self.session.post("/analysis", json=p))
        return Analysis.model_validate(r.json())

    def get_analysis(self, id) -> Analysis:
        r = self.check(self.session.get(f"/analysis/{id}"))
        return Analysis.model_validate(r.json())

    def push_file(self, file, upload=None):
        if upload:
            if upload.access.kind not in ["file", "http"]:
                raise RuntimeError("client only support file & http access")
            if upload.access.mode != "push":
                raise RuntimeError("client only support push mode")
        else:
            with file.open("rb") as fd:
                sha1 = file_digest(fd, "sha1").hexdigest()
            size = file.stat().st_size
            upload = self.new_upload(UploadRequest(sha1=sha1, size=size))

        if upload.state == State.COMPLETE:
            return upload

        if upload.access.kind == "file":
            path = Path(upload.access.path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with Path(file).open("rb") as src, path.open("wb") as dst:
                shutil.copyfileobj(src, dst)

        if upload.access.kind == "http":
            with Path(file).open("rb") as src, requests.Session() as session:
                offset = 0
                for part in upload.access.parts:
                    if part.state == State.COMPLETE:
                        continue
                    h = {}
                    if upload.access.headers:
                        h.update(upload.access.headers)
                    if part.headers:
                        h.update(part.headers)
                    n = int(h.pop("Content-Length"))
                    if part.state != State.COMPLETE:
                        src.seek(offset)
                        data = src.read(n)
                        session.put(part.url, headers=h, data=data)
                    offset += n

        return self.complete_upload(id=upload.id)

    def pull_file(self, file, root):
        tmp = Path(root, file.path + ".tmp")
        tmp.parent.mkdir(parents=True, exist_ok=True)

        if file.url.scheme == "file":
            with Path(file.url.path).open("rb") as src, tmp.open("wb") as dst:
                shutil.copyfileobj(src, dst)
        else:
            with requests.get(file.url, stream=True) as r:
                r.raise_for_status()
                with tmp.open("wb") as fd:
                    for chunk in r.iter_content(chunk_size=8192):
                        fd.write(chunk)

        with tmp.open("rb") as fd:
            sha1 = file_digest(fd, "sha1").hexdigest()
        if sha1 != file.sha1:
            tmp.unlink()
            raise RuntimeError(f"mismatch {sha1=} for {file=}")

        tmp.rename(Path(root, file.path))

    def upload(self, path, mime="auto", metadata=None):
        if path.is_dir():
            files = [p for p in path.glob("**/*") if p.is_file()]
        else:
            files = [path]

        u = [self.push_file(f) for f in files]

        r = FileSetRequest(files=[], mime=mime, metadata=metadata)
        for i, file in enumerate(files):
            name = file.relative_to(path)
            sha1 = u[i].id
            r.files.append(File(path=str(name), sha1=sha1))

        return self.new_fileset(r)

    def download(self, resource, root):
        if isinstance(resource, Analysis):
            for key, value in resource.results.items():
                if not value.startswith("@"):
                    continue
                fileset = self.get_fileset(value[1:])
                out = Path(root, key)
                self.download(fileset, out)
            return

        if isinstance(resource, FileSet):
            fileset = self.get_fileset_download(resource.id)
            for file in fileset.files:
                self.pull_file(file, root)
            return

        raise RuntimeError("client can only download fileset and analysis")
