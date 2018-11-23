"""List of repositories to check."""

repolist = []


class Repositories():
    """Class representing list of repositories."""

    def __init__(self, config):
        """Load list of repositories from the provided config object."""
        self._repolist = config.get_repolist()

    @property
    def repolist(self):
        """Getter for the 'repolist' attribute."""
        return self._repolist
