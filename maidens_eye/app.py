"""
Maiden's Eye - Demon's Souls Live Monitor

Main application module - orchestrates UI, data fetching, and background tasks.
Clean architecture with separated concerns across multiple modules.
"""

import threading
import time
import urllib.error
import urllib.request
from collections import deque
from tkinter import Tk, StringVar, BooleanVar

from config import (
    URL, TIMEOUT_SECONDS, USER_AGENT, DEFAULT_REFRESH_SECONDS,
    WINDOW_TITLE, WINDOW_GEOMETRY, WINDOW_MIN_SIZE,
    MAX_HISTORY_VALUES, HISTORY_UPDATE_INTERVAL, STATUS_UPDATE_INTERVAL
)
from parser import OnlineUsersParser
from utils import format_time_ago, play_beep
from styles import setup_window_styles
from ui_builder import (
    build_header, build_separator, build_hero_section,
    build_status_line, build_sparkline_section, build_footer,
    animate_hero_bounce
)
from ui_areas import build_areas_section, populate_areas_list


class App:
    """Main application class - orchestrates UI and data fetching."""
    
    def __init__(self, root: Tk):
        """Initialize the application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.parser = OnlineUsersParser()
        
        # Application state
        self.running = True
        self.refresh_seconds = DEFAULT_REFRESH_SECONDS
        self.previous_snapshot = None
        self.previous_total_players = None
        self.player_history = deque(maxlen=MAX_HISTORY_VALUES)
        self.last_update_time = None
        self.is_live = False
        self.last_history_update = 0
        
        # UI Variables
        self.total_players_var = StringVar(value="--")
        self.status_text_var = StringVar(value="Starting…")
        self.sound_var = BooleanVar(value=True)
        self.refresh_interval_var = StringVar(value=f"{DEFAULT_REFRESH_SECONDS}s")
        
        # Setup window and build UI
        self._setup_window()
        self._build_ui()
        self._start_background_tasks()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    # =========================================================================
    # INITIALIZATION
    # =========================================================================
    
    def _setup_window(self):
        """Configure main window properties."""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.minsize(*WINDOW_MIN_SIZE)
        setup_window_styles(self.root)
    
    def _build_ui(self):
        """Build all UI components."""
        # Header with controls
        self.refresh_combo, self.sound_btn = build_header(
            self.root,
            self.total_players_var,
            self.refresh_interval_var,
            self.trigger_refresh,
            self.on_refresh_interval_changed,
            self.toggle_sound
        )
        
        # Separator line
        build_separator(self.root)
        
        # Hero section (large player count)
        self.hero_label = build_hero_section(self.root, self.total_players_var)
        
        # Status line
        self.status_frame, self.live_label, self.update_label = build_status_line(self.root, self.status_text_var)
        
        # Sparkline chart
        self.sparkline = build_sparkline_section(self.root)
        
        # Areas list
        self.areas_canvas, self.areas_frame = build_areas_section(self.root)
        
        # Footer
        build_footer(self.root)
        
        # Update sound button icon
        self._update_sound_button()
    
    # =========================================================================
    # UI UPDATE METHODS
    # =========================================================================
    
    def _update_sound_button(self):
        """Update sound button icon based on enabled/disabled state."""
        self.sound_btn.configure(text="🔊" if self.sound_var.get() else "🔇")
    
    def update_status_line(self):
        """Update status line with current live state and time elapsed."""
        if self.is_live and self.last_update_time:
            elapsed = int(time.time() - self.last_update_time)
            time_str = format_time_ago(elapsed)
            self.live_label.configure(text="● Live", style="LiveOnline.TLabel")
            self.update_label.configure(text=f" · Updated {time_str}")
        else:
            self.live_label.configure(text="● Offline", style="LiveOffline.TLabel")
            self.update_label.configure(text=" · Waiting for data…")
    
    # =========================================================================
    # EVENT HANDLERS
    # =========================================================================
    
    def on_refresh_interval_changed(self, event=None):
        """Handle refresh interval dropdown change."""
        value = self.refresh_interval_var.get()
        try:
            # Extract number from "10s" format
            self.refresh_seconds = int(value.rstrip('s'))
        except ValueError:
            self.refresh_seconds = DEFAULT_REFRESH_SECONDS
    
    def toggle_sound(self):
        """Toggle sound on/off."""
        self.sound_var.set(not self.sound_var.get())
        self._update_sound_button()
    
    def trigger_refresh(self):
        """Manually trigger a data refresh."""
        threading.Thread(target=self.fetch_once, daemon=True).start()
    
    def on_close(self):
        """Handle window close event."""
        self.running = False
        self.root.destroy()
    
    # =========================================================================
    # BACKGROUND TASKS
    # =========================================================================
    
    def _start_background_tasks(self):
        """Start all background threads."""
        # Data polling thread
        self.poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.poll_thread.start()
        
        # Status line update loop
        self._schedule_status_update()
    
    def _poll_loop(self):
        """Background polling loop - fetches data periodically."""
        while self.running:
            self.fetch_once()
            
            # Sleep in small increments to allow quick shutdown
            for _ in range(self.refresh_seconds * 10):
                if not self.running:
                    break
                time.sleep(0.1)
    
    def _schedule_status_update(self):
        """Schedule periodic status line updates."""
        if self.running:
            self.update_status_line()
            self.root.after(STATUS_UPDATE_INTERVAL, self._schedule_status_update)
    
    # =========================================================================
    # DATA FETCHING AND PROCESSING
    # =========================================================================
    
    def fetch_once(self):
        """Fetch data from server once and update UI."""
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                text = response.read().decode(charset, errors="replace")
            
            snapshot = self.parser.parse(text)
            self.root.after(0, lambda: self.apply_snapshot(snapshot))
            
        except urllib.error.URLError:
            self.root.after(0, lambda: self.handle_fetch_error())
        except Exception:
            self.root.after(0, lambda: self.handle_fetch_error())
    
    def apply_snapshot(self, snapshot: dict):
        """Apply fetched data snapshot to UI.
        
        Args:
            snapshot: Parsed data dictionary with total, sections, etc.
        """
        # Update live status
        self.is_live = True
        self.last_update_time = time.time()
        
        # Update hero section with animation if value changed
        new_total = snapshot["total"]
        if self.previous_total_players is not None and new_total != self.previous_total_players:
            # Trigger bounce animation
            animate_hero_bounce(self.hero_label, self.root)
        
        self.total_players_var.set(str(new_total))
        self.previous_total_players = new_total
        
        # Update areas list
        populate_areas_list(self.areas_frame, snapshot["sections"])
        
        # Update player history (add one entry per minute)
        current_time = time.time()
        if current_time - self.last_history_update >= HISTORY_UPDATE_INTERVAL:
            self.player_history.append(snapshot["total"])
            self.sparkline.add_value(snapshot["total"])
            self.last_history_update = current_time
        elif not self.player_history:
            # First data point
            self.player_history.append(snapshot["total"])
            self.sparkline.add_value(snapshot["total"])
            self.last_history_update = current_time
        
        # Play sound if player count changed
        if self.previous_snapshot is not None:
            old_total = self.previous_snapshot["total"]
            new_total = snapshot["total"]
            if old_total != new_total and self.sound_var.get():
                direction = "up" if new_total > old_total else "down"
                play_beep(direction)
        
        self.previous_snapshot = snapshot
        self.update_status_line()
    
    def handle_fetch_error(self):
        """Handle data fetch errors."""
        self.is_live = False
        self.update_status_line()


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

def main():
    """Main entry point for the application."""
    root = Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()


