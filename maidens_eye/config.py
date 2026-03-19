"""
Configuration constants for Maiden's Eye application.

Contains URLs, timeouts, color schemes, and other application-wide settings.
"""

# =============================================================================
# SERVER CONFIGURATION
# =============================================================================

URL = "https://rpcs3.thearchstones.com/MapCR_Count.txt"
TIMEOUT_SECONDS = 8
USER_AGENT = "MaidensEye/2.0 (+Windows 11; Python tkinter)"

# =============================================================================
# REFRESH SETTINGS
# =============================================================================

DEFAULT_REFRESH_SECONDS = 60
REFRESH_INTERVALS = ["10s", "20s", "30s", "60s"]  # Available options

# =============================================================================
# HISTORY SETTINGS
# =============================================================================

MAX_HISTORY_VALUES = 60  # One value per minute for 60 minutes
HISTORY_UPDATE_INTERVAL = 60  # Seconds between history updates

# =============================================================================
# COLOR SCHEME (Dark Theme)
# =============================================================================

COLORS = {
    # Background colors
    "bg_dark": "#1e1e1e",         # Main background
    "bg_darker": "#2d2d2d",       # Secondary background (areas list, sparkline)
    "bg_chart": "#252525",        # Sparkline chart background
    
    # Foreground colors
    "fg_light": "#e0e0e0",        # Primary text
    "fg_dim": "#808080",          # Secondary text
    "fg_dimmer": "#606060",       # Tertiary text (footer)
    
    # Accent colors
    "accent_green": "#7bed9f",    # Main accent (hero number, values)
    "live_green": "#2ecc71",      # Live status indicator
    "offline_red": "#e74c3c",     # Offline status indicator
    
    # UI elements
    "border": "#404040",          # Borders and separators
}

# =============================================================================
# SOUND SETTINGS
# =============================================================================

SOUND_FREQ_HIGH = 1800  # Hz for player count increase
SOUND_FREQ_LOW = 300    # Hz for player count decrease
SOUND_DURATION = 60     # Milliseconds

# =============================================================================
# UI SETTINGS
# =============================================================================

# Window
WINDOW_TITLE = "Maiden's Eye"
WINDOW_GEOMETRY = "390x620"
WINDOW_MIN_SIZE = (390, 550)

# Fonts
FONT_FAMILY = "Segoe UI Variable"
FONT_SIZE_TITLE = 20
FONT_SIZE_SUBTITLE = 9
FONT_SIZE_HERO = 56
FONT_SIZE_SUBHERO = 16
FONT_SIZE_NORMAL = 10
FONT_SIZE_SMALL = 9
FONT_SIZE_TINY = 8

# Sparkline
SPARKLINE_WIDTH = 350
SPARKLINE_HEIGHT = 60

# Update intervals
STATUS_UPDATE_INTERVAL = 1000  # Milliseconds (for "Updated Xs ago")
