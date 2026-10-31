import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.org_skill_owner import OrgSkillOwner
    from ..models.project_skill_owner import ProjectSkillOwner
    from ..models.skill_file import SkillFile
    from ..models.user_skill_owner import UserSkillOwner


T = TypeVar("T", bound="Skill")


@_attrs_define
class Skill:
    """
    Attributes:
        id (str):
        org_id (str):
        owner (Union['OrgSkillOwner', 'ProjectSkillOwner', 'UserSkillOwner']):
        name (str): Machine-readable skill identifier consisting of lowercase ASCII segments separated by single
            hyphens.
        revision_id (str):
        revision (int): Latest revision number of the skill.
        description (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        skill_md (Union[Unset, str]):
        files (Union[Unset, list['SkillFile']]): Files in the skill archive, including SKILL.md, with paths relative to
            the skill's top-level directory. Returned when fetching a single skill; omitted from list responses.
    """

    id: str
    org_id: str
    owner: Union["OrgSkillOwner", "ProjectSkillOwner", "UserSkillOwner"]
    name: str
    revision_id: str
    revision: int
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    skill_md: Union[Unset, str] = UNSET
    files: Union[Unset, list["SkillFile"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.org_skill_owner import OrgSkillOwner
        from ..models.project_skill_owner import ProjectSkillOwner

        id = self.id

        org_id = self.org_id

        owner: dict[str, Any]
        if isinstance(self.owner, OrgSkillOwner):
            owner = self.owner.to_dict()
        elif isinstance(self.owner, ProjectSkillOwner):
            owner = self.owner.to_dict()
        else:
            owner = self.owner.to_dict()

        name = self.name

        revision_id = self.revision_id

        revision = self.revision

        description = self.description

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        skill_md = self.skill_md

        files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "owner": owner,
                "name": name,
                "revision_id": revision_id,
                "revision": revision,
                "description": description,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if skill_md is not UNSET:
            field_dict["skill_md"] = skill_md
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.org_skill_owner import OrgSkillOwner
        from ..models.project_skill_owner import ProjectSkillOwner
        from ..models.skill_file import SkillFile
        from ..models.user_skill_owner import UserSkillOwner

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        def _parse_owner(
            data: object,
        ) -> Union["OrgSkillOwner", "ProjectSkillOwner", "UserSkillOwner"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_skill_owner_type_0 = OrgSkillOwner.from_dict(data)

                return componentsschemas_skill_owner_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_skill_owner_type_1 = ProjectSkillOwner.from_dict(data)

                return componentsschemas_skill_owner_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_skill_owner_type_2 = UserSkillOwner.from_dict(data)

            return componentsschemas_skill_owner_type_2

        owner = _parse_owner(d.pop("owner"))

        name = d.pop("name")

        revision_id = d.pop("revision_id")

        revision = d.pop("revision")

        description = d.pop("description")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        skill_md = d.pop("skill_md", UNSET)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = SkillFile.from_dict(files_item_data)

            files.append(files_item)

        skill = cls(
            id=id,
            org_id=org_id,
            owner=owner,
            name=name,
            revision_id=revision_id,
            revision=revision,
            description=description,
            created_at=created_at,
            updated_at=updated_at,
            skill_md=skill_md,
            files=files,
        )

        return skill
