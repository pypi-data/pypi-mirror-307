from .codecommit_utils import (
    call_codecommit_ls_remote,
)
from .https_utils import (
    call_https_ls_remote,
)
from .ssh_utils import (
    call_ssh_ls_remote,
)
import logging

LOGGER = logging.getLogger(__name__)


async def ls_remote(
    repo_url: str,
    repo_branch: str,
    *,
    credential_key: str | None = None,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    provider: str | None = None,
    is_pat: bool = False,
    arn: str | None = None,
    org_external_id: str | None = None,
) -> str | None:
    last_commit: str | None = None
    if credential_key is not None:
        last_commit = await call_ssh_ls_remote(
            repo_url, credential_key, repo_branch
        )
    elif arn is not None and org_external_id is not None:
        last_commit = await call_codecommit_ls_remote(
            repo_url,
            arn,
            repo_branch,
            org_external_id=org_external_id,
        )
    else:
        last_commit = await call_https_ls_remote(
            repo_url=repo_url,
            user=user,
            password=password,
            token=token,
            branch=repo_branch,
            provider=provider,
            is_pat=is_pat,
        )

    return last_commit
