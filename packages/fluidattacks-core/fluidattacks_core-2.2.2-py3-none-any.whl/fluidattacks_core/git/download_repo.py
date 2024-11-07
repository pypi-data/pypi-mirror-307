from .delete_files import (
    delete_out_of_scope_files,
)
from .download_file import (
    download_file,
)
from git import (
    GitError,
)
from git.cmd import (
    Git,
)
from git.repo import (
    Repo,
)
import logging
import os
from pathlib import (
    Path,
)
import shutil
import tarfile

LOGGER = logging.getLogger(__name__)


def _is_member_safe(
    member: tarfile.TarInfo,
) -> bool:
    return not (
        member.issym()
        or member.islnk()
        or os.path.isabs(member.name)
        or "../" in member.name
    )


def _safe_extract_tar(tar_handler: tarfile.TarFile, file_path: Path) -> bool:
    for member in tar_handler.getmembers():
        if not _is_member_safe(member):
            LOGGER.error("Unsafe path detected: %s", member.name)
            continue
        try:
            tar_handler.extract(member, path=file_path, numeric_owner=True)
            LOGGER.info("Extracted: %s", member.name)
        except tarfile.ExtractError as ex:
            LOGGER.error("Error extracting %s: %s", member.name, ex)

    return True


def remove_symlinks_in_directory(directory: str) -> None:
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path):
                os.unlink(file_path)


async def reset_repo(repo_path: str) -> bool:
    try:
        os.getcwd()
    except OSError as exc:
        LOGGER.error("Failed to get the working directory: %s", repo_path)
        LOGGER.error(exc)
        LOGGER.error("\n")
        os.chdir(repo_path)

    try:
        Git().execute(
            [
                "git",
                "config",
                "--global",
                "--add",
                "safe.directory",
                "*",
            ]
        )
    except GitError as exc:
        LOGGER.error("Failed to add safe directory %s", repo_path)
        LOGGER.error(exc)
        LOGGER.error("\n")

    try:
        repo = Repo(repo_path)
        repo.git.reset("--hard", "HEAD")
    except GitError as exc:
        LOGGER.error("Expand repositories has failed:")
        LOGGER.error("Repository: %s", repo_path)
        LOGGER.error(exc)
        LOGGER.error("\n")

        return False

    if repo.working_dir:
        remove_symlinks_in_directory(str(repo.working_dir))

    return True


async def download_repo_from_s3(
    download_url: str,
    destination_path: Path,
    git_ignore: list[str] | None = None,
) -> bool:
    os.makedirs(destination_path.parent, exist_ok=True)
    file_path = destination_path.with_suffix(".tar.gz")

    result = await download_file(download_url, str(file_path.absolute()))
    if not result:
        LOGGER.error("Failed to download repository from %s", download_url)
        return False

    try:
        shutil.rmtree(destination_path, ignore_errors=True)
        with tarfile.open(file_path, "r:gz") as tar_handler:
            _safe_extract_tar(tar_handler, file_path.parent)
    except PermissionError:
        LOGGER.error("Failed to extract repository from %s", file_path)
        return False

    os.remove(file_path)
    if not await reset_repo(str(destination_path.absolute())):
        shutil.rmtree(destination_path, ignore_errors=True)
        return False

    delete_out_of_scope_files(
        git_ignore or [], str(destination_path.absolute())
    )

    return True
