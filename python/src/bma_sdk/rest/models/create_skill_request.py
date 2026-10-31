import json
from collections.abc import Mapping
from io import BytesIO
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from .. import types
from ..types import File

if TYPE_CHECKING:
    from ..models.org_skill_owner_input import OrgSkillOwnerInput
    from ..models.project_skill_owner_input import ProjectSkillOwnerInput
    from ..models.user_skill_owner_input import UserSkillOwnerInput


T = TypeVar("T", bound="CreateSkillRequest")


@_attrs_define
class CreateSkillRequest:
    """
    Attributes:
        owner (Union['OrgSkillOwnerInput', 'ProjectSkillOwnerInput', 'UserSkillOwnerInput']):
        archive (File):
    """

    owner: Union["OrgSkillOwnerInput", "ProjectSkillOwnerInput", "UserSkillOwnerInput"]
    archive: File

    def to_dict(self) -> dict[str, Any]:
        from ..models.org_skill_owner_input import OrgSkillOwnerInput
        from ..models.project_skill_owner_input import ProjectSkillOwnerInput

        owner: dict[str, Any]
        if isinstance(self.owner, OrgSkillOwnerInput):
            owner = self.owner.to_dict()
        elif isinstance(self.owner, ProjectSkillOwnerInput):
            owner = self.owner.to_dict()
        else:
            owner = self.owner.to_dict()

        archive = self.archive.to_tuple()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "owner": owner,
                "archive": archive,
            }
        )

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if isinstance(self.owner, OrgSkillOwnerInput):
            files.append(
                (
                    "owner",
                    (
                        None,
                        json.dumps(self.owner.to_dict()).encode(),
                        "application/json",
                    ),
                )
            )
        elif isinstance(self.owner, ProjectSkillOwnerInput):
            files.append(
                (
                    "owner",
                    (
                        None,
                        json.dumps(self.owner.to_dict()).encode(),
                        "application/json",
                    ),
                )
            )
        else:
            files.append(
                (
                    "owner",
                    (
                        None,
                        json.dumps(self.owner.to_dict()).encode(),
                        "application/json",
                    ),
                )
            )

        files.append(("archive", self.archive.to_tuple()))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.org_skill_owner_input import OrgSkillOwnerInput
        from ..models.project_skill_owner_input import ProjectSkillOwnerInput
        from ..models.user_skill_owner_input import UserSkillOwnerInput

        d = dict(src_dict)

        def _parse_owner(
            data: object,
        ) -> Union[
            "OrgSkillOwnerInput", "ProjectSkillOwnerInput", "UserSkillOwnerInput"
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_skill_owner_input_type_0 = (
                    OrgSkillOwnerInput.from_dict(data)
                )

                return componentsschemas_skill_owner_input_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_skill_owner_input_type_1 = (
                    ProjectSkillOwnerInput.from_dict(data)
                )

                return componentsschemas_skill_owner_input_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_skill_owner_input_type_2 = UserSkillOwnerInput.from_dict(
                data
            )

            return componentsschemas_skill_owner_input_type_2

        owner = _parse_owner(d.pop("owner"))

        archive = File(payload=BytesIO(d.pop("archive")))

        create_skill_request = cls(
            owner=owner,
            archive=archive,
        )

        return create_skill_request
