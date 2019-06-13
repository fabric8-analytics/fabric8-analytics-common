"""Environment settings for VSCode visual tests."""


def before_all(context):
    """Perform basic setup."""
    context.time_for_analysis_to_finish = 5
    context.time_for_detailed_analysis_to_finish = 25
    context.time_for_text_editor_to_open = 2
    context.time_for_text_editor_to_close = 2
    context.time_for_vscode_to_close = 2
    context.time_for_context_menu = 2


def after_all(context):
    """Perform basic cleanup."""
    pass
