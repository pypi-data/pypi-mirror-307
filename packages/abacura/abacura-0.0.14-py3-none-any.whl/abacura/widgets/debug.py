"""Debug console widget"""
from datetime import datetime

from textual.css.query import NoMatches
from textual.widget import Widget
from textual.widgets import RichLog

from abacura.plugins import command, Plugin
from abacura.widgets.resizehandle import ResizeHandle

class DebugDock(Widget):
    """Experimental debug window"""
    def __init__(self, id: str, name: str = ""):
        super().__init__(id=id, name=name)
        self.tl = RichLog(id="debug", max_lines=2000, wrap=True)
        self.tl.can_focus = False

    def compose(self):
        yield ResizeHandle(self, "top")
        yield self.tl
