"""
Style configuration for Maiden's Eye application.

Contains all ttk Style setup for the dark theme interface.
"""

from tkinter import ttk

from config import COLORS, FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_SUBTITLE
from config import FONT_SIZE_HERO, FONT_SIZE_SUBHERO, FONT_SIZE_SMALL, FONT_SIZE_TINY


def setup_window_styles(root):
    """Configure window colors and ttk styles for dark theme.
    
    Args:
        root: Tkinter root window
    """
    root.configure(bg=COLORS["bg_dark"])
    
    # Configure ttk Style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Frame styles
    style.configure("TFrame", background=COLORS["bg_dark"])
    style.configure("Dark.TFrame", background=COLORS["bg_darker"])
    
    # Label styles
    style.configure("TLabel", 
                   background=COLORS["bg_dark"], 
                   foreground=COLORS["fg_light"])
    style.configure("Title.TLabel",
                   background=COLORS["bg_dark"],
                   foreground=COLORS["fg_light"],
                   font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"))
    style.configure("Subtitle.TLabel",
                   background=COLORS["bg_dark"],
                   foreground=COLORS["fg_dim"],
                   font=(FONT_FAMILY, FONT_SIZE_SUBTITLE))
    style.configure("Hero.TLabel",
                   background=COLORS["bg_dark"],
                   foreground=COLORS["accent_green"],
                   font=(FONT_FAMILY, FONT_SIZE_HERO, "bold"))
    style.configure("Subhero.TLabel",
                   background=COLORS["bg_dark"],
                   foreground=COLORS["fg_light"],
                   font=(FONT_FAMILY, FONT_SIZE_SUBHERO))
    style.configure("Dim.TLabel",
                   background=COLORS["bg_dark"],
                   foreground=COLORS["fg_dim"],
                   font=(FONT_FAMILY, FONT_SIZE_SMALL))
    style.configure("LiveOnline.TLabel",
                   background=COLORS["bg_dark"],
                   foreground=COLORS["accent_green"],
                   font=(FONT_FAMILY, FONT_SIZE_SMALL))
    style.configure("LiveOffline.TLabel",
                   background=COLORS["bg_dark"],
                   foreground="#ff6b6b",
                   font=(FONT_FAMILY, FONT_SIZE_SMALL))
    style.configure("Footer.TLabel",
                   background=COLORS["bg_dark"],
                   foreground=COLORS["fg_dimmer"],
                   font=(FONT_FAMILY, FONT_SIZE_TINY))
    
    # Button styles
    style.configure("TButton",
                   background=COLORS["bg_dark"],
                   foreground=COLORS["fg_light"],
                   bordercolor=COLORS["bg_dark"],
                   lightcolor=COLORS["bg_dark"],
                   darkcolor=COLORS["bg_dark"],
                   focuscolor=COLORS["bg_dark"],
                   highlightthickness=0,
                   relief="flat",
                   borderwidth=0,
                   padding=(4, 4),
                   font=(FONT_FAMILY, FONT_SIZE_SMALL * 2))
    style.map("TButton",
             background=[("active", COLORS["bg_darker"])],
             bordercolor=[("active", COLORS["bg_darker"])],
             lightcolor=[("active", COLORS["bg_darker"])],
             darkcolor=[("active", COLORS["bg_darker"])],
             relief=[("active", "flat")])
    
    # Combobox styles
    style.configure("TCombobox",
                   fieldbackground=COLORS["bg_darker"],
                   background=COLORS["bg_darker"],
                   foreground=COLORS["fg_light"],
                   arrowcolor=COLORS["fg_light"],
                   bordercolor=COLORS["border"],
                   selectbackground=COLORS["bg_darker"],
                   selectforeground=COLORS["fg_light"],
                   justify="center")
    style.map("TCombobox",
             fieldbackground=[("readonly", COLORS["bg_darker"])],
             selectbackground=[("readonly", COLORS["bg_darker"])],
             selectforeground=[("readonly", COLORS["fg_light"])])
    
    # Checkbutton styles
    style.configure("TCheckbutton",
                   background=COLORS["bg_dark"],
                   foreground=COLORS["fg_light"])
