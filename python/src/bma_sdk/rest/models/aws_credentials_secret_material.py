from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.aws_credentials_secret_material_kind import (
    AWSCredentialsSecretMaterialKind,
    check_aws_credentials_secret_material_kind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AWSCredentialsSecretMaterial")


@_attrs_define
class AWSCredentialsSecretMaterial:
    """
    Attributes:
        kind (AWSCredentialsSecretMaterialKind):
        access_key_id (str):
        secret_access_key (str):
        session_token (Union[Unset, str]):
        role_arn (Union[Unset, str]):
        external_id (Union[Unset, str]): Requires role_arn.
    """

    kind: AWSCredentialsSecretMaterialKind
    access_key_id: str
    secret_access_key: str
    session_token: Union[Unset, str] = UNSET
    role_arn: Union[Unset, str] = UNSET
    external_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        access_key_id = self.access_key_id

        secret_access_key = self.secret_access_key

        session_token = self.session_token

        role_arn = self.role_arn

        external_id = self.external_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "access_key_id": access_key_id,
                "secret_access_key": secret_access_key,
            }
        )
        if session_token is not UNSET:
            field_dict["session_token"] = session_token
        if role_arn is not UNSET:
            field_dict["role_arn"] = role_arn
        if external_id is not UNSET:
            field_dict["external_id"] = external_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_aws_credentials_secret_material_kind(d.pop("kind"))

        access_key_id = d.pop("access_key_id")

        secret_access_key = d.pop("secret_access_key")

        session_token = d.pop("session_token", UNSET)

        role_arn = d.pop("role_arn", UNSET)

        external_id = d.pop("external_id", UNSET)

        aws_credentials_secret_material = cls(
            kind=kind,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            session_token=session_token,
            role_arn=role_arn,
            external_id=external_id,
        )

        return aws_credentials_secret_material
