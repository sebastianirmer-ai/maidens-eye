"""
Custom UI widgets for Maiden's Eye application.

Contains custom tkinter widgets like the SparklineWidget for displaying player history.
"""

from collections import deque
from tkinter import Canvas

from config import COLORS, SPARKLINE_WIDTH, SPARKLINE_HEIGHT


class SparklineWidget(Canvas):
    """Custom Canvas widget for displaying a simple sparkline chart.
    
    Shows up to 60 data points as vertical bars (one per minute).
    Automatically scales to fit the available height.
    """
    
    def __init__(self, parent, width=SPARKLINE_WIDTH, height=SPARKLINE_HEIGHT, **kwargs):
        """Initialize sparkline widget.
        
        Args:
            parent: Parent tkinter widget
            width: Canvas width in pixels
            height: Canvas height in pixels
            **kwargs: Additional Canvas configuration options
        """
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=COLORS["bg_chart"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            **kwargs
        )
        self.data = deque(maxlen=60)
        self._width = width
        self._height = height
        
    def update_data(self, values: list):
        """Update the sparkline with new data (replaces all data).
        
        Args:
            values: List of integer values to display (max 60, oldest to newest)
        """
        self.data = deque(values[-60:], maxlen=60)
        self.redraw()
        
    def add_value(self, value: int):
        """Add a single new value to the sparkline (appends to right).
        
        Args:
            value: Integer value to add
        """
        self.data.append(value)
        self.redraw()
        
    def redraw(self):
        """Redraw the sparkline based on current data."""
        self.delete("all")
        
        if not self.data:
            # Show placeholder text when no data available
            self.create_text(
                self._width // 2,
                self._height // 2,
                text="No data yet",
                fill=COLORS["fg_dimmer"],
                font=("Segoe UI", 9)
            )
            return
        
        # Calculate dimensions
        max_val = max(self.data) if self.data else 1
        if max_val == 0:
            max_val = 1  # Avoid division by zero
        
        # Calculate bar width based on available space
        bar_width = max(2, self._width // 60)
        gap = 1
        total_bar_width = bar_width + gap
        
        # Draw bars from left to right (oldest to newest)
        for i, value in enumerate(self.data):
            # Calculate bar height (leave some padding at top/bottom)
            bar_height = int((value / max_val) * (self._height - 10)) if value > 0 else 2
            
            x = i * total_bar_width + 2
            y = self._height - bar_height - 2
            
            # Draw bar
            self.create_rectangle(
                x, y,
                x + bar_width, self._height - 2,
                fill=COLORS["fg_light"],
                outline=""
            )
