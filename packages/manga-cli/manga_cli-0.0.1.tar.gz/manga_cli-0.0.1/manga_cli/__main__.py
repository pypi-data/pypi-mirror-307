from .api import search
from .api.utils import get_user_agent
from pathlib import Path
import asyncio
from typing import List
from textual import on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Input, Label, Button
from textual.reactive import reactive

class Main(App):
    CSS_PATH = Path(__file__).parent / "styles" / "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Dark Mode"), 
                ("up", "move_up", "Move Up"), 
                ("down", "move_down", "Move Down")]
    
    current_index: reactive[int] = reactive(0)
    layout: reactive[VerticalScroll] = reactive(VerticalScroll())
    searchbar: reactive[Input] = reactive(Input(placeholder="Search for Manga..."))
    
    def __init__(self):
        super().__init__()
        self._debounce_task = None
    
    def compose(self) -> ComposeResult:
        yield self.searchbar
        yield self.layout
        yield Footer()
    
    @on(Input.Changed)
    async def show_results(self, event: Input.Changed):
        if self._debounce_task and not self._debounce_task.done():
            self._debounce_task.cancel()
        self._debounce_task = asyncio.create_task(self._debounce_search())
    
    async def _debounce_search(self):
        """Handles the debounce logic for search."""
        await asyncio.sleep(0.5)
        query = self.searchbar.value
        if query: 
            self.layout.remove_children()
            results = await asyncio.to_thread(search, query)
            self.layout.mount_all([Button(result["title"]) for result in results])
    
    async def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    Main().run()
