from typing import Literal, cast

MemoryStoreAccess = Literal["read", "read_write"]

MEMORY_STORE_ACCESS_VALUES: set[MemoryStoreAccess] = {
    "read",
    "read_write",
}


def check_memory_store_access(value: str) -> MemoryStoreAccess:
    if value in MEMORY_STORE_ACCESS_VALUES:
        return cast(MemoryStoreAccess, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MEMORY_STORE_ACCESS_VALUES!r}"
    )
