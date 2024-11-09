__all__ = ["Executable"]

import os
from abc import ABC
from shutil import which
from typing import ClassVar


class Executable(ABC):
    EXECUTABLE: ClassVar[list[str] | str | None]
    EXECUTABLE_LINUX: ClassVar[list[str] | str | None]
    EXECUTABLE_DARWIN: ClassVar[list[str] | str | None]

    @property
    def executable(self) -> str:
        sysname: str = os.uname()[0]
        # Get the executable for the current system first, then check
        # the general executable.
        platform_specific_exec = getattr(self, f"EXECUTABLE_{sysname.upper()}", None)
        if platform_specific_exec is not None:
            if not isinstance(platform_specific_exec, list):
                # Make sure the platform specific executable is a list
                platform_specific_exec = [platform_specific_exec]
            for exec in platform_specific_exec:
                # Iterate over all possible executable paths or names
                # and check if 'which' finds the executable.
                # If so, return the result.
                result = which(exec)
                if result:
                    return result
        # No executable found using the platform specific executable.
        # Try using the generate executable instead.
        execs = getattr(self, "EXECUTABLE", None)
        if execs:
            if not isinstance(execs, list):
                execs = [execs]
            for exec in execs:
                result = which(exec)
                if result:
                    return result
        raise FileNotFoundError(f"Unable to find executable for class '{type(self)}'")
