import os
import shutil
import stat
import sys
import tempfile
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Generator


@contextmanager
def make_tempdir() -> Generator[Path, None, None]:
    """Execute a block in a temporary directory and remove the directory and
    its contents at the end of the with block.
    YIELDS (Path): The path of the temp directory.
    """
    d = Path(tempfile.mkdtemp())
    yield d

    # On Windows, git clones use read-only files, which cause permission errors
    # when being deleted. This forcibly fixes permissions.
    def force_remove(rmfunc, path, ex):
        os.chmod(path, stat.S_IWRITE)
        rmfunc(path)

    try:
        if sys.version_info >= (3, 12):
            shutil.rmtree(str(d), onexc=force_remove)  # type: ignore
        else:
            shutil.rmtree(str(d), onerror=force_remove)
    except PermissionError:
        warnings.warn(f"Could not remove temp directory {d}")
