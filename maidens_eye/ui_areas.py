"""
Areas list UI components for Maiden's Eye application.

Contains the scrollable areas list section with player icons.
"""

import os
from tkinter import Canvas, Frame, Label, PhotoImage, ttk

from config import COLORS, FONT_FAMILY, FONT_SIZE_SMALL

# Global variable to cache player icon
_player_icon = None


def load_player_icon():
    """Load player icon from GIF file.
    
    Returns:
        PhotoImage object or None if loading fails
    """
    global _player_icon
    
    if _player_icon is not None:
        return _player_icon
    
    try:
        # Get the path relative to this file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "img", "maidens_eye_img_player_2.gif")
        
        # Load GIF image using tkinter's built-in PhotoImage (no external libs needed)
        _player_icon = PhotoImage(file=icon_path)
        return _player_icon
        
    except Exception as e:
        print(f"Error loading player icon: {e}")
        return None


def build_areas_section(parent):
    """Build scrollable areas list section.
    
    Args:
        parent: Parent widget
        
    Returns:
        Tuple of (areas_canvas, areas_frame) for populating with data
    """
    # Header
    areas_header_frame = Frame(parent, bg=COLORS["bg_dark"])
    areas_header_frame.pack(fill="x", padx=15, pady=(0, 5))
    
    # Left: Location header
    Label(
        areas_header_frame,
        text="Location",
        bg=COLORS["bg_dark"],
        fg=COLORS["fg_dim"],
        font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
        anchor="w"
    ).pack(side="left", expand=True, fill="x")
    
    # Right: Players header
    Label(
        areas_header_frame,
        text="Players",
        bg=COLORS["bg_dark"],
        fg=COLORS["fg_dim"],
        font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
        anchor="e",
        width=10
    ).pack(side="right")
    
    # Areas list container (with border)
    list_container = Frame(
        parent,
        bg=COLORS["border"],
        highlightthickness=1,
        highlightbackground=COLORS["border"]
    )
    list_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
    
    # Canvas for scrollable content
    areas_canvas = Canvas(
        list_container,
        bg=COLORS["bg_darker"],
        highlightthickness=0
    )
    areas_canvas.pack(side="left", fill="both", expand=True)
    
    # Scrollbar (hidden but functional scrolling with mouse wheel)
    # No scrollbar widget created - scrolling works with mouse wheel only
    
    # Frame inside canvas
    areas_frame = Frame(areas_canvas, bg=COLORS["bg_darker"])
    canvas_window = areas_canvas.create_window(
        (0, 0),
        window=areas_frame,
        anchor="nw",
        tags="areas_frame"
    )
    
    # Bind canvas resize events
    def on_frame_configure(event=None):
        areas_canvas.configure(scrollregion=areas_canvas.bbox("all"))
    
    def on_canvas_configure(event=None):
        canvas_width = event.width if event else areas_canvas.winfo_width()
        areas_canvas.itemconfig(canvas_window, width=canvas_width)
    
    areas_frame.bind("<Configure>", on_frame_configure)
    areas_canvas.bind("<Configure>", on_canvas_configure)
    
    # Enable mouse wheel scrolling
    def on_mousewheel(event):
        areas_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    areas_canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    return areas_canvas, areas_frame


def populate_areas_list(areas_frame, sections: dict):
    """Populate the areas list with location data.
    
    Args:
        areas_frame: Frame to populate
        sections: Dictionary of {location: player_count}
    """
    # Clear existing widgets
    for widget in areas_frame.winfo_children():
        widget.destroy()
    
    if not sections:
        # Show empty state
        Label(
            areas_frame,
            text="No active areas",
            bg=COLORS["bg_darker"],
            fg=COLORS["fg_dim"],
            font=(FONT_FAMILY, 10),
            pady=20
        ).pack()
        return
    
    # Create row for each area
    for location, count in sections.items():
        row_frame = Frame(areas_frame, bg=COLORS["bg_darker"], height=18)
        row_frame.pack(fill="x", padx=10, pady=0)
        row_frame.pack_propagate(False)  # Enforce fixed height
        
        # Location name
        Label(
            row_frame,
            text=location,
            bg=COLORS["bg_darker"],
            fg=COLORS["fg_light"],
            font=(FONT_FAMILY, 10),
            anchor="w",
            pady=0
        ).pack(side="left", expand=True, fill="x", pady=0)
        
        # Player count with icon
        count_frame = Frame(row_frame, bg=COLORS["bg_darker"])
        count_frame.pack(side="right")
        
        # Load player icon (cached after first call)
        player_icon = load_player_icon()
        
        if player_icon:
            icon_label = Label(
                count_frame,
                image=player_icon,
                bg=COLORS["bg_darker"],
                borderwidth=0
            )
            icon_label.image = player_icon  # Keep reference to prevent garbage collection
            icon_label.pack(side="left", padx=(0, 0))
        else:
            # Fallback to emoji if image loading fails
            Label(
                count_frame,
                text="👤",
                bg=COLORS["bg_darker"],
                fg=COLORS["accent_green"],
                font=(FONT_FAMILY, 9)
            ).pack(side="left", padx=(0, 1))
        
        Label(
            count_frame,
            text=str(count),
            bg=COLORS["bg_darker"],
            fg=COLORS["accent_green"],
            font=(FONT_FAMILY, 10, "bold"),
            anchor="w"
        ).pack(side="left")
