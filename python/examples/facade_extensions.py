"""BMA extensions to the Managed Agents API: session files and desktop stream."""

from __future__ import annotations

import os
import sys

from bma_sdk.facade_extensions import FacadeExtensions


def main(session_id: str) -> None:
    with FacadeExtensions(
        api_key=os.environ["BMA_API_KEY"],
        base_url=os.environ["BMA_BASE_URL"],  # origin, without /v1
        project_id=os.environ.get("BMA_PROJECT_ID"),
    ) as ext:
        file = ext.sessions.files.upload(session_id, file=("report.pdf", b"%PDF-1.7"))
        page = ext.sessions.files.list(session_id, limit=100)
        print(file.id, [f.filename for f in page.data])


if __name__ == "__main__":
    main(sys.argv[1])
