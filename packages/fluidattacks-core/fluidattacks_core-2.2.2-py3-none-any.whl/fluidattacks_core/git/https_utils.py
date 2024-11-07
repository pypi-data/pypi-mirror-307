from .classes import (
    InvalidParameter,
)
from .utils import (
    format_url,
)
import asyncio
import base64
import logging

LOGGER = logging.getLogger(__name__)


async def _execute_git_command(
    url: str, branch: str, is_pat: bool, token: str | None = None
) -> tuple[bytes, bytes, int | None]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-c",
        "http.sslVerify=false",
        "-c",
        "http.followRedirects=true",
        *(
            [
                "-c",
                "http.extraHeader=Authorization: Basic "
                + base64.b64encode(f":{token}".encode()).decode(),
            ]
            if is_pat
            else []
        ),
        "ls-remote",
        "--",
        url,
        branch,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, _stderr = await asyncio.wait_for(proc.communicate(), 20)
    return stdout, _stderr, proc.returncode


async def https_ls_remote(
    *,
    repo_url: str,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    branch: str = "HEAD",
    provider: str | None = None,
    is_pat: bool = False,
) -> str | None:
    url = format_url(
        repo_url=repo_url,
        user=user,
        password=password,
        token=token,
        provider=provider,
        is_pat=is_pat,
    )

    try:
        stdout, _stderr, return_code = await _execute_git_command(
            url, branch, is_pat, token
        )
        if _stderr and return_code != 0:
            LOGGER.error(
                "failed git ls-remote",
                extra={
                    "extra": {
                        "error": _stderr.decode(),
                        "repo_url": repo_url,
                    }
                },
            )
    except asyncio.exceptions.TimeoutError:
        LOGGER.warning(
            "git remote-ls time out",
            extra={"extra": {"repo_url": repo_url}},
        )
        return None

    if return_code != 0:
        return None

    return stdout.decode().split("\t")[0]


async def call_https_ls_remote(
    *,
    repo_url: str,
    user: str | None,
    password: str | None,
    token: str | None,
    branch: str,
    provider: str | None,
    is_pat: bool,
) -> str | None:
    if user is not None and password is not None:
        return await https_ls_remote(
            repo_url=repo_url,
            user=user,
            password=password,
            branch=branch,
        )
    if token is not None:
        return await https_ls_remote(
            repo_url=repo_url,
            token=token,
            branch=branch,
            provider=provider or "",
            is_pat=is_pat,
        )
    if repo_url.startswith("http"):
        return await https_ls_remote(
            repo_url=repo_url,
            branch=branch,
        )
    raise InvalidParameter()
