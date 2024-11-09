# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2023)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

import dataclasses as dtcl
from datetime import datetime as when_t
from sys import exit as Exit
from traceback import TracebackException as traceback_t
from typing import Any, Callable, ClassVar, Literal, NoReturn, Protocol, get_args

from rich.console import Console as console_t
from rich.markup import escape as PreProcessedForRich

_order_h = Literal["when", "context"]
_where_h = Literal["console", "output"]
_how_h = Literal["raw", "plain", "rich", "html"]


@dtcl.dataclass(slots=True, eq=False, repr=False)
class issue_t:
    _BASE_CONTEXT: ClassVar[str] = "BASE"

    when: when_t = dtcl.field(init=False, default_factory=when_t.now)
    context: str
    message: str

    def Formatted(
        self,
        with_time: bool,
        when_separator: str,
        ctxt_final: str,
        /,
        *,
        PreProcessed: Callable[[str], str] | None = None,
        ctxt_before: str = "",
        ctxt_after: str = "",
        cab: str = "",
        cae: str = "",
        ceb: str = "",
        cee: str = "",
    ) -> str:
        """"""
        if with_time:
            time = f"{self.when}{when_separator}"
        else:
            time = ""
        if PreProcessed is None:
            context, message = self.context, self.message
        else:
            context, message = map(PreProcessed, (self.context, self.message))
        if context.__len__() == 0:
            context = self.__class__._BASE_CONTEXT
        message = message.format(cab=cab, cae=cae, ceb=ceb, cee=cee)

        return f"{time}{ctxt_before}{context}{ctxt_final}{ctxt_after}{message}"


class _not_passed_t:
    pass


_NOT_PASSED = _not_passed_t()


class _console_protocol_t(Protocol):
    print: Callable[[...], None]


@dtcl.dataclass(slots=True, eq=False, repr=False)
class _issue_manager_t(list[issue_t]):
    when_separator: ClassVar[str] = " @ "
    context_separator: ClassVar[str] = ">"
    context_final: ClassVar[str] = ":: "
    color_context: ClassVar[str] = "gray53"
    color_value: ClassVar[str] = "dark_orange3"
    color_expected: ClassVar[str] = "green"

    console: console_t | _console_protocol_t = dtcl.field(init=False, default=None)
    _current_context: list[str] = dtcl.field(init=False, default_factory=list)

    def SetConsole(self, console: console_t | _console_protocol_t, /) -> None:
        """"""
        self.console = console

    def AddContextLevel(self, new_level: str, /) -> None:
        """"""
        self._current_context.append(new_level)

    def AddedContextLevel(self, new_level: str, /) -> _issue_manager_t:
        """
        Meant to be used as:
        with self.AddedContextLevel("new level"):
            ...
        """
        self.AddContextLevel(new_level)
        return self

    def GoBackToUpperContext(self) -> None:
        """"""
        self._current_context.pop()

    def Add(
        self, message: str, /, *, actual: Any = _NOT_PASSED, expected: Any = None
    ) -> None:
        """"""
        if actual is _NOT_PASSED:
            if not message.endswith("."):
                message += "."
        else:
            actual = _Formatted(actual)
            expected = _Formatted(expected, should_format_str=False)
            if message.endswith("."):
                message = message[:-1]
            # cab: color-actual-begin, cae: color-actual-end
            message = (
                f"{message}: Actual={{cab}}{actual}{{cae}}; "
                f"Expected={{ceb}}{expected}{{cee}}."
            )

        issue = issue_t(
            context=self.__class__.context_separator.join(self._current_context),
            message=message,
        )
        self.append(issue)

    @property
    def has_issues(self) -> bool:
        """"""
        return self.__len__() > 0

    def Report(
        self,
        /,
        *,
        order: _order_h = "when",
        where: _where_h = "console",
        how: _how_h = "plain",
        with_time: bool = False,
        should_clear: bool = True,
        should_exit: bool = True,
        with_exit_value: int = 36,
        with_exception: Exception = None,
    ) -> tuple[issue_t, ...] | tuple[str, ...] | None | NoReturn:
        """
        If "how" == "raw", all other parameters are ignored, and no action is taken
        beside returning the list of issues as "issue_t".
        """
        if self.__len__() == 0:
            return

        for parameter, hint, message in zip(
            (order, where, how),
            (_order_h, _where_h, _how_h),
            ("reporting order", "report destination", "report format"),
        ):
            if parameter not in (options := get_args(hint)):
                raise ValueError(
                    f"Invalid {message}. Actual={parameter}; Expected=One of {options}."
                )

        if how == "raw":
            return tuple(self)

        cls = self.__class__

        PreProcessed = None
        if how == "rich":
            PreProcessed = PreProcessedForRich
            ctxt_before = f"[{cls.color_context}]"
            ctxt_after = f"[/]"
            cab = f"[{cls.color_value}]"
            cae = ctxt_after
            ceb = f"[{cls.color_expected}]"
            cee = ctxt_after
        elif how == "html":
            ctxt_before = f"<span color={cls.color_context}>"
            ctxt_after = f"</span>"
            cab = f"<span color={cls.color_value}>"
            cae = ctxt_after
            ceb = f"<span color={cls.color_expected}>"
            cee = ctxt_after
        else:  # how == "plain"
            ctxt_before = ctxt_after = cab = cae = ceb = cee = ""

        if order == "when":
            output = list(self)
        else:  # order == "context"
            output = sorted(self, key=lambda _elm: _elm.context)

        output = map(
            lambda _elm: _elm.Formatted(
                with_time,
                cls.when_separator,
                cls.context_final,
                PreProcessed=PreProcessed,
                ctxt_before=ctxt_before,
                ctxt_after=ctxt_after,
                cab=cab,
                cae=cae,
                ceb=ceb,
                cee=cee,
            ),
            output,
        )

        if where == "output":
            return tuple(output)

        output = "\n".join(output)
        if how == "rich":
            if self.console is None:
                self.console = console_t(highlight=False, force_terminal=True)
            self.console.print(output, crop=False, overflow="ignore")
        else:
            print(output, flush=should_exit)

        if should_exit:
            if with_exception is None:
                Exit(with_exit_value)
            raise with_exception

        if should_clear:
            self.Clear()

    def Clear(self) -> None:
        """"""
        self.clear()

    def Reset(self) -> None:
        """"""
        self.clear()
        self._current_context = []

    def __enter__(self) -> None:
        """"""
        pass

    def __exit__(
        self,
        exc_type: Exception | None,
        exc_value: str | None,
        traceback: traceback_t | None,
        /,
    ) -> bool:
        """"""
        self.GoBackToUpperContext()
        return False


ISSUE_MANAGER = _issue_manager_t()


def _Formatted(value: Any, /, *, should_format_str: bool = True) -> str:
    """"""
    if value is None:
        return "None"
    if isinstance(value, str):
        if should_format_str:
            return '"' + value + '"'
        return value

    output = str(value)
    output = output.replace("{", "{{")
    output = output.replace("}", "}}")

    return output
