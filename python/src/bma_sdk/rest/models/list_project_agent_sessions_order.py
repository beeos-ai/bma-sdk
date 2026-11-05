from typing import Literal, cast

ListProjectAgentSessionsOrder = Literal["asc", "desc"]

LIST_PROJECT_AGENT_SESSIONS_ORDER_VALUES: set[ListProjectAgentSessionsOrder] = {
    "asc",
    "desc",
}


def check_list_project_agent_sessions_order(
    value: str,
) -> ListProjectAgentSessionsOrder:
    if value in LIST_PROJECT_AGENT_SESSIONS_ORDER_VALUES:
        return cast(ListProjectAgentSessionsOrder, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_PROJECT_AGENT_SESSIONS_ORDER_VALUES!r}"
    )
