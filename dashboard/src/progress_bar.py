"""Progress bar handling."""


def progress_bar_class(p):
    """Decide which class to use for progress bar."""
    p = int(p)
    if p < 25:
        return "progress-bar-danger"
    elif p > 90:
        return "progress-bar-success"
    else:
        return "progress-bar-warning"


def progress_bar_width(p):
    """Compute progress bar width."""
    p = int(p)
    return 15.0 + p * 0.85
