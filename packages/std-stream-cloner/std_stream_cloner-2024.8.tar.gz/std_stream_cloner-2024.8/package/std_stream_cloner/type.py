"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2020
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import inspect as spct
import os as opsy
import sys as sstm
import tempfile as tmpf
import typing as h
from datetime import datetime as dttm
from os import sep as FOLDER_SEPARATOR
from pathlib import Path as path_t

DATE_TIME_FORMAT = "%Y-%m-%d@%H:%M:%S"
STDOUT_PREFIX = ": "
STDERR_PREFIX = "! "

AUTO_STREAM_FILE = "auto"
DEFAULT = "default"

tmp_file_t = tmpf._TemporaryFileWrapper

std_stream_h = h.Literal["out", "err"]
stream_selection_h = std_stream_h | h.Literal["both"]
operation_h = h.Literal["pause", "resume"]
where_h = h.Literal["stream", "log"]


@d.dataclass(slots=True, repr=False, eq=False)
class _clone_t:

    name: std_stream_h
    path: str | path_t
    accessor: h.TextIO | None = None
    date_time_format: str | None = None
    should_print_where: bool = False
    stream_prefix: str | None = None
    #
    original: h.TextIO = d.field(init=False)
    PrintToStream: h.Callable[[str], int] = d.field(init=False)
    #
    _keep_alive: tmp_file_t | None = d.field(init=False, default=None)
    _latest_newline_position: int | None = d.field(init=False, default=None)

    def __post_init__(self) -> None:
        """"""
        if self.name == "out":
            self.original = sstm.stdout
            if self.stream_prefix == DEFAULT:
                self.stream_prefix = STDOUT_PREFIX
        else:
            self.original = sstm.stderr
            if self.stream_prefix == DEFAULT:
                self.stream_prefix = STDERR_PREFIX
        self.PrintToStream = self.original.write

        if self.stream_prefix is None:
            self.stream_prefix = ""
        if self.date_time_format == DEFAULT:
            self.date_time_format = DATE_TIME_FORMAT

        if self.path == AUTO_STREAM_FILE:
            self._keep_alive = tmpf.NamedTemporaryFile(
                mode="w+", prefix="stream-clone_", suffix=".log", delete=False
            )
            self.accessor = self._keep_alive.file
            self.path = path_t(self._keep_alive.name)
        elif self.accessor is None:
            self.path = path_t(self.path)
            if self.path.exists() and not self.path.is_file():
                raise ValueError(
                    f'Path "{self.path}" exists and is not a regular file.'
                )

            if self.path.exists():
                mode = "a+"
            else:
                mode = "w+"
            self.accessor = open(self.path, mode)

        self.ResumeCloning()

    def PauseCloning(self) -> None:
        """"""
        if self.name == "out":
            sstm.stdout = self.original
        else:
            sstm.stderr = self.original

    def ResumeCloning(self) -> None:
        """"""
        # To start cloning with an empty stream.
        self.flush()

        if self.name == "out":
            sstm.stdout = self
        else:
            sstm.stderr = self

    def PrintToLog(self, text: str, /) -> int:
        """"""
        for move in ("\f", "\v"):
            if move in text:
                text = text.replace(move, "\n")

        if text.startswith("\r"):
            text = text[1:]
            if self._latest_newline_position is not None:
                self.accessor.seek(
                    self._latest_newline_position + 1,
                    opsy.SEEK_SET,
                )
        elif text.startswith("\b"):
            length_before = text.__len__()
            text = text.lstrip("\b")
            length_after = text.__len__()
            self.accessor.seek(length_after - length_before, opsy.SEEK_CUR)

        set_position = False
        rewind_length = 0
        if text.endswith("\b"):
            length_before = text.__len__()
            text = text.rstrip("\b")
            length_after = text.__len__()
            rewind_length = length_after - length_before
        elif text.endswith("\r"):
            text = text[:-1]
            set_position = True

        output = text.__len__()
        if output > 0:
            for unwanted, replacement in zip(("\r", "\b", "\a"), ("⇦", "←", "🔔")):
                if unwanted in text:
                    text = text.replace(unwanted, replacement)
            self._UpdateLatestNewlinePosition(text)
            if text == "\n":
                self.accessor.write("\n")
            else:
                if self.date_time_format is None:
                    date_time = ""
                else:
                    date_time = dttm.now().strftime(self.date_time_format)
                if self.should_print_where:
                    where = _Where()
                else:
                    where = ""
                self.accessor.write(f"{date_time}{where}{self.stream_prefix}{text}")

        if rewind_length < 0:
            self.accessor.seek(rewind_length, opsy.SEEK_CUR)
        elif set_position and (self._latest_newline_position is not None):
            self.accessor.seek(self._latest_newline_position + 1, opsy.SEEK_SET)

        return output

    def _UpdateLatestNewlinePosition(self, text: str, /) -> None:
        """
        Must be called before writing to log file so that file descriptor has not moved
        yet.
        """
        newline_position = text.rfind("\n")
        if newline_position != -1:
            current_position = self.accessor.seek(0, opsy.SEEK_CUR)
            self._latest_newline_position = current_position + newline_position

    def write(self, text: str, /) -> int:
        """"""
        output = self.original.write(text)
        _ = self.PrintToLog(text)

        return output

    def flush(self) -> None:
        """"""
        self.original.flush()
        self.accessor.flush()


@d.dataclass(slots=True, repr=False, eq=False)
class stream_cloner_t:

    clone_out: _clone_t | None = None
    clone_err: _clone_t | None = None
    _err_is_not_out: bool = True

    def Start(
        self,
        *,
        out: str | path_t | None = None,
        err: str | path_t | None = None,
        both: str | path_t | None = AUTO_STREAM_FILE,
        prefix: (
            dict[stream_selection_h, str | None | dict[str, str | None]] | None
        ) = None,
    ) -> None:
        """"""
        if (out is None) and (err is None) and (both is None):
            raise ValueError("No stream specified.")
        if (both is not None) and not ((out is None) and (err is None)):
            raise ValueError('Stream(s) specified individually and with "both".')

        if prefix is None:
            prefix = {"out": None, "err": None}
        elif "both" in prefix:
            common = prefix["both"]
            prefix = {"out": common, "err": common}
        kwargs = {}
        for key, value in prefix.items():
            if value is None:
                value = {}
            elif value == DEFAULT:
                value = {"date_time_format": DEFAULT, "stream_prefix": DEFAULT}
            kwargs[key] = value

        if out is not None:
            self.clone_out = _clone_t("out", out, **kwargs["out"])
        if err is not None:
            if err == out:
                raise ValueError("Output and error streams have identical paths.")
            self.clone_err = _clone_t("err", err, **kwargs["err"])
        if both is not None:
            self.clone_out = _clone_t("out", both, **kwargs["out"])
            self.clone_err = _clone_t(
                "err",
                self.clone_out.path,
                accessor=self.clone_out.accessor,
                **kwargs["err"],
            )
            self._err_is_not_out = False

    def ShouldPrintWhereInLog(
        self, should_print_where: bool, /, *, which: stream_selection_h = "both"
    ) -> None:
        """"""
        if which == "both":
            if self.clone_out is not None:
                self.clone_out.should_print_where = should_print_where
            if (self.clone_err is not None) and self._err_is_not_out:
                self.clone_err.should_print_where = should_print_where
        elif which == "out":
            self.clone_out.should_print_where = should_print_where
        else:
            self.clone_err.should_print_where = should_print_where

    def Pause(self, which: stream_selection_h = "both") -> None:
        """"""
        self._PauseOrResume(which, "pause")

    def Resume(self, which: stream_selection_h = "both") -> None:
        """"""
        self._PauseOrResume(which, "resume")

    def PrintToStream(
        self,
        *objects,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
        which: std_stream_h = "out",
    ) -> int:
        """"""
        return self._PrintToEither(objects, sep, end, flush, which, "stream")

    def PrintToLog(
        self,
        *objects,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
        which: std_stream_h = "out",
    ) -> int:
        """"""
        return self._PrintToEither(objects, sep, end, flush, which, "log")

    def Flush(self, which: stream_selection_h = "both") -> None:
        """"""
        if which == "both":
            if self.clone_out is not None:
                self.clone_out.flush()
            if (self.clone_err is not None) and self._err_is_not_out:
                self.clone_err.flush()
        elif which == "out":
            self.clone_out.flush()
        else:
            self.clone_err.flush()

    def _PauseOrResume(
        self, which: stream_selection_h, operation: operation_h, /
    ) -> None:
        """"""
        if operation == "pause":
            method = "PauseCloning"
        else:
            method = "ResumeCloning"

        if which == "both":
            if self.clone_out is not None:
                getattr(self.clone_out, method)()
            if self.clone_err is not None:
                getattr(self.clone_err, method)()
        elif which == "out":
            getattr(self.clone_out, method)()
        else:
            getattr(self.clone_err, method)()

    def _PrintToEither(
        self,
        objects,
        sep: str,
        end: str,
        flush: bool,
        which: std_stream_h,
        where: where_h,
    ) -> int:
        """"""
        if where == "stream":
            method = "PrintToStream"
        else:
            method = "PrintToLog"

        text = sep.join(map(str, objects)) + end
        if which == "out":
            output = getattr(self.clone_out, method)(text)
        else:
            output = getattr(self.clone_err, method)(text)

        if flush:
            self.Flush(which)

        return output

    def __del__(self) -> None:
        """"""
        if self.clone_out is None:
            path_out = None
        else:
            self.clone_out.flush()
            self.clone_out.PauseCloning()
            path_out = self.clone_out.path
        if self.clone_err is None:
            path_err = None
        else:
            self.clone_err.flush()
            self.clone_err.PauseCloning()
            path_err = self.clone_err.path

        if (path_out == path_err) and (path_out is not None):
            print(f"Stdout and stderr clones at {path_out}")
        else:
            if path_out is not None:
                print(f"Stdout clone at {path_out}")
            if path_err is not None:
                print(f"Stderr clone at {path_err}")


def _Where() -> str:
    """"""
    frame = spct.stack()[3][0]
    details = spct.getframeinfo(frame)

    module = path_t(details.filename)
    for path in sstm.path:
        if module.is_relative_to(path):
            module = module.relative_to(path).with_suffix("")
            module = str(module).replace(FOLDER_SEPARATOR, ".")
            break

    return f"_{module}:{details.function}:{details.lineno}"


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
