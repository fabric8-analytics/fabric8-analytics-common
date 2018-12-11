"""Common configuration."""

import configparser
from urllib.parse import urljoin
from fastlog import log


class Config:
    """Class representing common configuration."""

    CONFIG_FILE_NAME = 'config.ini'

    def __init__(self):
        """Read and parse the configuration file."""
        self.config = configparser.ConfigParser()
        with log.indent():
            log.info("Reading config file")
            self.config.read(Config.CONFIG_FILE_NAME)
            log.success("Done")

    def get_jenkins_url(self):
        """Return Jenkins URL."""
        return self.config.get('ci', 'jenkins_url')

    def get_master_build_job(self):
        """Return master build job postfix."""
        return self.config.get('ci', 'master_build_job')

    def get_mm_url(self):
        """Return Mattermost API URL."""
        return self.config.get('mattermost', 'api_url')

    def get_mm_team(self):
        """Return Mattermost team."""
        return self.config.get('mattermost', 'team')

    def get_mm_channel(self):
        """Return Mattermost channel."""
        return self.config.get('mattermost', 'channel')

    def get_mm_user_login(self):
        """Return Mattermost user login."""
        return self.config.get('mattermost', 'user_login')

    def get_mm_user_password(self):
        """Return Mattermost user password."""
        return self.config.get('mattermost', 'user_password')


if __name__ == "__main__":
    # execute simple checks, but only if run this module as a script
    config = Config()
    print(config.get_master_build_url())
