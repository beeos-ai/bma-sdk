from typing import Literal, cast

AWSCredentialsSecretMaterialKind = Literal["aws_credentials"]

AWS_CREDENTIALS_SECRET_MATERIAL_KIND_VALUES: set[AWSCredentialsSecretMaterialKind] = {
    "aws_credentials",
}


def check_aws_credentials_secret_material_kind(
    value: str,
) -> AWSCredentialsSecretMaterialKind:
    if value in AWS_CREDENTIALS_SECRET_MATERIAL_KIND_VALUES:
        return cast(AWSCredentialsSecretMaterialKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AWS_CREDENTIALS_SECRET_MATERIAL_KIND_VALUES!r}"
    )
