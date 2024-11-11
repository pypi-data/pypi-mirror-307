import os
import re
import tarfile
import tempfile
import typing
from pathlib import Path

import pathspec
from loguru import logger
from tqdm import tqdm

WARN_FILE_SIZE = 50 * 1024 * 1024  # 100 MB


def get_all_files_in_dir(directory):
    return [
        os.path.join(root, file)
        for root, dirs, files in os.walk(directory)
        for file in files
    ]


def create_tarball(
    source_dir: Path, exclude_gitignore: bool, exclude_regex: str | None
) -> typing.IO[typing.Any]:
    temp = tempfile.NamedTemporaryFile(suffix=".tar")
    spec = None

    if exclude_gitignore and (source_dir / ".gitignore").exists():
        with open(source_dir / ".gitignore") as gitignore:
            spec_src = gitignore.read()
        spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.gitwildmatch.GitWildMatchPattern, spec_src.splitlines()
        )

    files = set(get_all_files_in_dir(source_dir))
    if spec is not None:
        files -= set(spec.match_files(files))

    # Run exclude regex
    if exclude_regex is not None:
        files = {file for file in files if not re.search(exclude_regex, file)}

    total_size = sum(os.path.getsize(file) for file in files)
    with tarfile.open(temp.name, "w:gz") as tar:
        with tqdm(
            total=total_size, unit="B", unit_scale=True, desc="Creating archive"
        ) as progress_bar:
            for file in files:
                if os.path.getsize(file) > WARN_FILE_SIZE:
                    logger.warning(
                        f"{file} is larger than {WARN_FILE_SIZE/(1024*1024)}MB"
                    )
                arcname = os.path.relpath(file, source_dir)
                tar.add(file, arcname=arcname)
                progress_bar.update(os.path.getsize(file))

    return temp
