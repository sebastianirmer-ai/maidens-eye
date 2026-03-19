"""
UI builder module for Maiden's Eye application.

Contains functions to build and configure all UI components.
Separates UI construction logic from application logic.
"""

from tkinter import Canvas, Frame, Label, ttk

from config import COLORS, FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_SUBTITLE
from config import FONT_SIZE_HERO, FONT_SIZE_SUBHERO, FONT_SIZE_SMALL, FONT_SIZE_TINY
from widgets import SparklineWidget
from styles import setup_window_styles
from ui_areas import build_areas_section, populate_areas_list


def animate_hero_bounce(hero_label, root):
    """Animate hero label with a subtle glow pulse effect.
    
    Uses color brightness pulse to create a wobble-like attention effect
    without affecting layout.
    
    Args:
        hero_label: The hero number label widget
        root: Root window for scheduling updates
    """
    # Animation parameters
    duration_ms = 300
    frames = 12
    
    # Base color: #7bed9f (accent_green)
    base_r, base_g, base_b = 123, 237, 159
    
    # Brighter color (enhanced green)
    bright_r, bright_g, bright_b = 150, 255, 180
    
    frame_delay = duration_ms // frames
    
    # Easing function - pulse out and back
    def ease_pulse(t):
        """Smooth pulse - symmetric in and out."""
        return abs((t * 2) - 1) if t <= 0.5 else 1 - abs((t * 2) - 1)
    
    # Animation frames
    for i in range(frames + 1):
        progress = i / frames
        eased = ease_pulse(progress)
        
        # Interpolate colors
        r = int(base_r + (bright_r - base_r) * eased)
        g = int(base_g + (bright_g - base_g) * eased)
        b = int(base_b + (bright_b - base_b) * eased)
        
        color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Schedule color update
        root.after(
            i * frame_delay,
            lambda c=color: hero_label.configure(foreground=c)
        )




def build_header(parent, total_players_var, refresh_interval_var, 
                on_refresh_click, on_interval_change, on_sound_toggle):
    """Build header with title and controls.
    
    Args:
        parent: Parent widget
        total_players_var: StringVar for player count display
        refresh_interval_var: StringVar for interval dropdown
        on_refresh_click: Callback for refresh button
        on_interval_change: Callback for interval change
        on_sound_toggle: Callback for sound toggle
        
    Returns:
        Tuple of (refresh_combo, sound_btn) for external access
    """
    header_frame = ttk.Frame(parent)
    header_frame.pack(fill="x", padx=15, pady=(10, 0))
    
    # Left side: Title only (will be vertically centered with controls)
    left_frame = ttk.Frame(header_frame)
    left_frame.pack(side="left", anchor="w")
    
    ttk.Label(left_frame, text="Maiden's Eye", style="Title.TLabel").pack(anchor="w")
    
    # Right side: Controls
    right_frame = ttk.Frame(header_frame)
    right_frame.pack(side="right", anchor="e", pady=(0, 0))
    
    # Refresh button (in container for exact sizing)
    refresh_container = Frame(right_frame, bg=COLORS["bg_dark"], width=36, height=36)
    refresh_container.pack(side="left", padx=2)
    refresh_container.pack_propagate(False)  # Prevent resizing
    refresh_btn = ttk.Button(refresh_container, text="⟳", command=on_refresh_click)
    refresh_btn.place(relx=0.5, rely=0.5, anchor="center")
    
    # Interval dropdown
    refresh_combo = ttk.Combobox(
        right_frame,
        textvariable=refresh_interval_var,
        values=["10s", "20s", "30s", "60s"],
        width=5,
        state="readonly",
        justify="center"
    )
    refresh_combo.pack(side="left", padx=2)
    refresh_combo.bind("<<ComboboxSelected>>", on_interval_change)
    
    # Sound toggle button (in container for exact sizing)
    sound_container = Frame(right_frame, bg=COLORS["bg_dark"], width=36, height=36)
    sound_container.pack(side="left", padx=2)
    sound_container.pack_propagate(False)  # Prevent resizing
    sound_btn = ttk.Button(sound_container, text="🔊", command=on_sound_toggle)
    sound_btn.place(relx=0.5, rely=0.45, anchor="center")
    
    # Subtitle in separate frame below, close to separator
    subtitle_frame = ttk.Frame(parent)
    subtitle_frame.pack(fill="x", padx=15, pady=(2, 2))
    
    ttk.Label(subtitle_frame, text="Demon's Souls Live Monitor", style="Subtitle.TLabel").pack(anchor="w")
    
    return refresh_combo, sound_btn


def build_separator(parent):
    """Build horizontal separator line.
    
    Args:
        parent: Parent widget
    """
    sep_canvas = Canvas(parent, height=1, bg=COLORS["border"], highlightthickness=0)
    sep_canvas.pack(fill="x", padx=15, pady=(2, 0))


def build_hero_section(parent, total_players_var):
    """Build hero section with large player count.
    
    Args:
        parent: Parent widget
        total_players_var: StringVar for player count
        
    Returns:
        Label widget for hero number
    """
    hero_frame = ttk.Frame(parent)
    hero_frame.pack(fill="x", pady=(0, 0))
    
    # Large player count number
    hero_label = ttk.Label(
        hero_frame,
        textvariable=total_players_var,
        style="Hero.TLabel"
    )
    hero_label.pack(pady=(0, 0))
    
    # "Players Online" text
    ttk.Label(hero_frame, text="Players Online", style="Subhero.TLabel").pack(pady=(0, 0))
    
    return hero_label


def build_status_line(parent, status_text_var):
    """Build status line with live indicator.
    
    Args:
        parent: Parent widget
        status_text_var: StringVar for status text (not used anymore, kept for compatibility)
        
    Returns:
        Tuple of (status_frame, live_label, update_label) for external control
    """
    status_container = ttk.Frame(parent)
    status_container.pack(fill="x", pady=(0, 12))
    
    # Inner frame to center the status line content
    status_frame = ttk.Frame(status_container)
    status_frame.pack()
    
    # Live status label (colored part: "● Live")
    live_label = ttk.Label(
        status_frame,
        text="● Live",
        style="LiveOnline.TLabel"
    )
    live_label.pack(side="left")
    
    # Update info label (gray part: " · Updated Xs ago")
    update_label = ttk.Label(
        status_frame,
        text=" · Updated 0s ago",
        style="Dim.TLabel"
    )
    update_label.pack(side="left")
    
    return status_frame, live_label, update_label


def build_sparkline_section(parent):
    """Build sparkline chart section.
    
    Args:
        parent: Parent widget
        
    Returns:
        SparklineWidget instance
    """
    sparkline_container = ttk.Frame(parent, style="Dark.TFrame")
    sparkline_container.pack(fill="x", padx=15, pady=(0, 15))
    
    # Label above chart
    label_frame = Frame(sparkline_container, bg=COLORS["bg_darker"])
    label_frame.pack(fill="x", padx=8, pady=(8, 4))
    
    Label(
        label_frame,
        text="players last 60 minutes",
        bg=COLORS["bg_darker"],
        fg=COLORS["fg_dimmer"],
        font=(FONT_FAMILY, FONT_SIZE_TINY)
    ).pack()
    
    # Sparkline canvas
    sparkline = SparklineWidget(sparkline_container)
    sparkline.pack(padx=8, pady=(0, 8))
    
    return sparkline


def build_footer(parent):
    """Build footer with author credit.
    
    Args:
        parent: Parent widget
    """
    footer_frame = ttk.Frame(parent)
    footer_frame.pack(fill="x", side="bottom", pady=(0, 8))
    
    ttk.Label(
        footer_frame,
        text="by Steamy_Sebastian",
        style="Footer.TLabel"
    ).pack()

