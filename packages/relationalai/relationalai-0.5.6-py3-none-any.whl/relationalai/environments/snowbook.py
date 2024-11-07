from __future__ import annotations
from functools import wraps
from typing import Literal
import re

from rich import terminal_theme as themes

from ..errors import RAIException, RAIExceptionSet, RAIWarning, record

def patch(target, name):
    "Given the `target` class or module, replace method `name` with the decorated wrapper fn."
    original = getattr(target, name)

    def decorator(f):
        @wraps(original)
        def wrapped(*args, **kwargs):
            return f(original, *args, **kwargs)

        setattr(target, name, wrapped)
        return wrapped

    return decorator

FRAME_STYLE = {
    "warn": ("#fffce7", "#926c05"),
    "error": ("#ffecec", "#7d353b"),
}

class SnowbookEnvironment:
    last_run = None
    cells = {}
    states = {}
    _existing = None

    exceptions = []

    def _format_alert_header(self, msg: str):
        def replace_func(match):
            span = match.group(1)
            title = match.group(2).strip()
            suffix = re.sub(r'</span>(?!.*<span)', '', match.group(3), flags=re.DOTALL) + (match.group(4) or "")
            rest = match.group(5) or ""
            return "".join([
                f'### <div style="display: flex">{span}{title}</span> ',
                f'<span style="flex: 1; text-align: right; font-size: 1rem;">{span}{suffix}</span>{rest}</span>'
            ])

        pattern = re.compile(r'(<span.*?>)--- (.*?) -+(.*?)(?:(: )|-+)</span>(.*)$', re.MULTILINE)
        return pattern.sub(replace_func, msg)

    def _format_alert_footer(self, msg: str):
        pattern = re.compile(r'^(<p>\s*)?<span .*?>\s*----+\s*</span>(\s*</p>)?\s*$', re.MULTILINE)
        return pattern.sub("", msg)

    def _format_alert_line_breaks(self, msg: str):
        return re.sub(r'(</\w+>)$', r'\1  ', msg, flags=re.MULTILINE)

    def _format_alert(self, msg: str, status: Literal["error", "warn"] = "error"):
        (bg, fg) = FRAME_STYLE[status]

        formatted = msg
        for apply in [self._format_alert_header, self._format_alert_footer, self._format_alert_line_breaks]:
           formatted = apply(formatted)

        return "".join([
           f"""<div style="font-family: apercu-mono-regular, Menlo, Monaco, Consolas, 'Courier New', monospace;
                           padding: 8px 16px 0.1px 16px;
                           margin-bottom: 1em;
                           border-radius: 5px;
                           background-color: {bg};
                           color: {fg};">""".strip(),
           formatted,
           "</div>"
        ])

    def report_alerts(self, *alerts: Warning|BaseException):
       import streamlit as st # pyright: ignore
       for alert in alerts:
          status = "warn" if isinstance(alert, Warning) else "error"
          if isinstance(alert, RAIExceptionSet):
             self.report_alerts(*alert.exceptions)
             continue

          elif isinstance(alert, RAIWarning) or isinstance(alert, RAIException):
             with record() as (console, _):
                alert.pprint()
                raw = console.export_html(inline_styles=True, code_format="{code}", theme=themes.NIGHT_OWLISH)
          else:
             raw = str(alert)

          formatted = self._format_alert(raw, status)
          st.markdown(formatted, unsafe_allow_html=True)

    def _handle_exc(self, exc: BaseException):
        self.exceptions.append(exc)
        if isinstance(exc, RAIException):
           try:
              self.report_alerts(exc)
              return Exception("See above for details")
           except Exception as e:
              self.exceptions.append(e)

    def _patch(self):
        import snowbook # pyright: ignore

        @patch(snowbook.executor.notebook_compiler.NotebookCompiler, "compile_and_run_cell") # pyright: ignore
        def _(original, instance, cell, *args, **kwargs):
            id = self.last_run = cell.cell_content.id
            self.cells[id] = cell
            state = original(instance, cell, *args, **kwargs)
            self.states[id] = state
            return state

        @patch(snowbook.executor.notebook_compiler, "execute_compilation") # pyright: ignore
        def _(original, *args, **kwargs):
            import streamlit as st # pyright: ignore
            try:
                return original(*args, **kwargs)
            except st.errors.UncaughtAppException as e:
                raise self._handle_exc(e.exc) or e

    @classmethod
    def _attach(cls):
        if cls._existing:
            return cls._existing
        neue = cls()
        cls._existing = neue
        neue._patch()
        return neue

    def active_cell(self):
        return self.cells.get(self.last_run)

env = SnowbookEnvironment._attach()
