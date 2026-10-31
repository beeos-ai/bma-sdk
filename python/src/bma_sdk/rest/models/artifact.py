import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.artifact_origin import ArtifactOrigin, check_artifact_origin
from ..types import UNSET, Unset

T = TypeVar("T", bound="Artifact")


@_attrs_define
class Artifact:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_id (str):
        created_at (datetime.datetime):
        session_id (Union[Unset, str]): Session that owns the artifact; absent for an agent-level artifact.
        origin (Union[Unset, ArtifactOrigin]): input: uploaded to the session, sent as message media or received from an
            integration. machine_upload: uploaded by the agent from its machine (storage_upload). tool_output: written by a
            tool (oversized results, MCP media, viewed images).
        content_type (Union[Unset, str]):
        filename (Union[Unset, str]):
        digest (Union[Unset, str]):
        size_bytes (Union[Unset, int]):
    """

    id: str
    org_id: str
    project_id: str
    agent_id: str
    created_at: datetime.datetime
    session_id: Union[Unset, str] = UNSET
    origin: Union[Unset, ArtifactOrigin] = UNSET
    content_type: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    digest: Union[Unset, str] = UNSET
    size_bytes: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        agent_id = self.agent_id

        created_at = self.created_at.isoformat()

        session_id = self.session_id

        origin: Union[Unset, str] = UNSET
        if not isinstance(self.origin, Unset):
            origin = self.origin

        content_type = self.content_type

        filename = self.filename

        digest = self.digest

        size_bytes = self.size_bytes

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "agent_id": agent_id,
                "created_at": created_at,
            }
        )
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if origin is not UNSET:
            field_dict["origin"] = origin
        if content_type is not UNSET:
            field_dict["content_type"] = content_type
        if filename is not UNSET:
            field_dict["filename"] = filename
        if digest is not UNSET:
            field_dict["digest"] = digest
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        agent_id = d.pop("agent_id")

        created_at = isoparse(d.pop("created_at"))

        session_id = d.pop("session_id", UNSET)

        _origin = d.pop("origin", UNSET)
        origin: Union[Unset, ArtifactOrigin]
        if isinstance(_origin, Unset):
            origin = UNSET
        else:
            origin = check_artifact_origin(_origin)

        content_type = d.pop("content_type", UNSET)

        filename = d.pop("filename", UNSET)

        digest = d.pop("digest", UNSET)

        size_bytes = d.pop("size_bytes", UNSET)

        artifact = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            created_at=created_at,
            session_id=session_id,
            origin=origin,
            content_type=content_type,
            filename=filename,
            digest=digest,
            size_bytes=size_bytes,
        )

        return artifact
