from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

from pydantic import AnyUrl, BaseModel, Field


class State(StrEnum):
    PENDING = "pending"
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETING = "completing"
    COMPLETE = "complete"
    FAILED = "failed"


class User(BaseModel):
    id: str = Field(
        description="Unique ID of a user",
    )
    organization: str = Field(
        description="Name of the organization of this user",
    )
    disabled: bool = Field(
        description="Indicate if user is disabled",
        default=False,
    )


class Resource(BaseModel):
    id: str = Field(
        description="ID of the resource",
    )
    owner: str = Field(
        description="ID of the organization that can access this resource",
    )
    creator: str = Field(
        description="User that created this resource",
    )
    created: datetime = Field(
        description="Date/Time when this resource was created",
    )
    changes: list[tuple[datetime, str]] = Field(
        description="Date/Time when this resource was updated with information about the change",
    )
    state: State = Field(
        description="State of this resource",
    )

    def add_change(self, what):
        now = datetime.now(UTC).replace(microsecond=0)
        self.changes.append((now, what))


class UploadPart(BaseModel):
    state: State = Field(
        description="Status of this file part",
    )
    url: AnyUrl | None = Field(
        description="URL to upload/download this file part over HTTP",
        default=None,
    )
    headers: dict[str, str] | None = Field(
        description="Additional headers to include in the request for this part",
        default=None,
    )


class UsingFileSystem(BaseModel):
    kind: str = "file"

    mode: Literal["push", "pull"] = Field(
        description="Uploading mode for this request",
        default="push",
    )
    path: Path = Field(
        description="File location",
    )


class UsingHTTP(BaseModel):
    kind: str = "http"

    mode: Literal["push", "pull"] = Field(
        description="Uploading mode for this request",
        default="push",
    )
    parts: list[UploadPart] = Field(
        description="List of file parts to limit the size of individual HTTP request",
    )
    headers: dict[str, str] | None = Field(
        description="Additional headers to include in the request",
        default=None,
    )


class UsingAWS(BaseModel):
    kind: str = "aws"

    bucket: str = Field(
        description="Name of the S3 bucket",
    )
    object: str = Field(
        description="Name of the object",
    )
    region: str = Field(
        description="Name of the region (AWS_REGION)",
    )
    access: str = Field(
        description="Access key ID (AWS_ACCESS_KEY_ID)",
    )
    secret: str = Field(
        description="Secret access key (AWS_SECRET_ACCESS_KEY)",
    )
    session: str | None = Field(
        description="Session token (AWS_SESSION_TOKEN)",
        default=None,
    )


class UsingAzure(BaseModel):
    kind: str = "azure"

    storage: str = Field(
        description="Name of the storage account",
    )
    container: str = Field(
        description="Name of the container",
    )
    blob: str = Field(
        description="Name of the blob",
    )
    application: str = Field(
        description="ID of the application of the service principal's app registration (AZCOPY_SPA_APPLICATION_ID)",
    )
    secret: str = Field(
        description="Client secret of the application (AZCOPY_SPA_CLIENT_SECRET)",
    )
    tenant: str = Field(
        description="ID of the tenant in the Azure portal (AZCOPY_TENANT_ID)",
    )


class UploadRequest(BaseModel):
    sha1: str = Field(
        description="File SHA-1 digest encoded as hexadecimal digits",
        pattern="[a-f0-9]{40}",
    )
    size: int = Field(
        description="File size in bytes",
    )
    access: UsingFileSystem | UsingHTTP | UsingAWS | UsingAzure | None = Field(
        description="Details on how to access the file",
        default=None,
    )


class Upload(Resource):
    size: int = Field(
        description="File size in bytes",
    )
    access: UsingFileSystem | UsingHTTP | UsingAWS | UsingAzure = Field(
        description="Details on how to access the file",
        default=None,
    )


class File(BaseModel):
    path: str = Field(
        description="File path relative to its set",
        max_length=128,
    )
    sha1: str = Field(
        description="File SHA-1 digest encoded as hexadecimal digits",
        pattern="[a-f0-9]{40}",
    )
    url: AnyUrl | None = Field(
        description="URL to access the file directly",
        default=None,
    )


class FileSetRequest(BaseModel):
    files: list[File] = Field(
        description="Files requested for upload",
    )
    mime: str | None = Field(
        description="MIME type of the file set (will autodetect if not set or set to 'auto')",
        default=None,
    )
    metadata: dict | None = Field(
        description="Associated metadata",
        default=None,
    )


class FileSet(Resource):
    mime: str = Field(
        description="MIME type of the file set",
    )
    files: list[File] = Field(
        description="Files associated to this set",
    )
    metadata: dict[str, Any] | None = Field(
        description="Associated metadata",
        default=None,
    )


class AnalysisRequest(BaseModel):
    module: str = Field(
        description="ID of the module used to perform the analysis",
    )
    inputs: dict[str, Any] = Field(
        description="Inputs to be supplied to the module",
    )
    account: str | None = Field(
        description="ID of an account (e.g. customer) for accounting",
        default=None,
    )


class Analysis(Resource):
    module: str = Field(
        description="ID of the module that produces the analysis",
    )
    inputs: dict[str, Any] = Field(
        description="Inputs supplied to the module",
    )
    results: dict[str, Any] | None = Field(
        description="If available, results produced by the module",
        default=None,
    )


class Argument(BaseModel):
    types: list[str] = Field(
        description="Supported types for the input argument",
    )
    description: str | None = Field(
        description="Description of the input",
        default=None,
    )
    optional: bool | None = Field(
        description="Set if this input is optional",
        default=False,
    )


class Module(BaseModel):
    id: str = Field(
        description="ID of the module",
    )
    inputs: dict[str, Argument] = Field(
        description="Information about the module arguments",
    )
    name: str | None = Field(
        description="Name of the module",
        default=None,
    )
    version: str | None = Field(
        description="Version of the module",
        default=None,
    )
    description: str | None = Field(
        description="Description of the module",
        default=None,
    )


class ModuleList(BaseModel):
    modules: list[str] = Field(
        description="ID of the modules available to create analysis",
    )
