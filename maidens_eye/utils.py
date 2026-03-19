"""
Utility functions for Maiden's Eye application.

Contains helper functions for time formatting, sound playback, etc.
"""

from config import SOUND_FREQ_HIGH, SOUND_FREQ_LOW, SOUND_DURATION


def format_time_ago(seconds: int) -> str:
    """Format seconds into readable relative time string.
    
    Args:
        seconds: Number of seconds elapsed
        
    Returns:
        Formatted string like "3s ago", "2m ago", "1h ago"
        
    Examples:
        >>> format_time_ago(5)
        '5s ago'
        >>> format_time_ago(120)
        '2m ago'
        >>> format_time_ago(3700)
        '1h ago'
    """
    if seconds < 60:
        return f"{seconds}s ago"
    elif seconds < 3600:
        mins = seconds // 60
        return f"{mins}m ago"
    else:
        hours = seconds // 3600
        return f"{hours}h ago"


def play_beep(direction: str = None) -> None:
    """Play a beep sound notification.
    
    Args:
        direction: "up" for increase (high pitch), "down" for decrease (low pitch),
                  or None for default system sound
    """
    try:
        import winsound
        if direction == "up":
            # High beep for player count increase
            winsound.Beep(SOUND_FREQ_HIGH, SOUND_DURATION)
        elif direction == "down":
            # Low beep for player count decrease
            winsound.Beep(SOUND_FREQ_LOW, SOUND_DURATION)
        else:
            # Default system sound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except Exception:
        # Fallback: if winsound not available or fails, try tkinter bell
        # (bell will be called from the main app context)
        pass
