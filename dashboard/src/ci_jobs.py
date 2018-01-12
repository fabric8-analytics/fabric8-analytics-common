"""Configuration of all relevant CI jobs."""
import configparser
from urllib.parse import urljoin


class CIJobs:
    """Class representing configuration of all relevant CI jobs."""

    CONFIG_FILE_NAME = 'ci_jobs.ini'

    def __init__(self):
        """Read and parse the configuration file."""
        self.config = configparser.ConfigParser()
        self.config.read(CIJobs.CONFIG_FILE_NAME)

    def get_ci_url(self):
        """Retrieve the URL to the CI front page."""
        return self.config.get('CI', 'jenkins_url')

    def get_job_url(self, repository_name, job_type):
        """Retrieve the URL to the CI job for given repository and job type."""
        assert job_type in {"build_job", "test_job", "pylint_job", "pydoc_job"}
        # the job with given type might not exist, return None in such cases
        try:
            repository_name = CIJobs.remove_prefix(repository_name, "fabric8-analytics-")
            url_prefix = self.get_ci_url()
            url_suffix = self.config.get(repository_name, job_type)
            return CIJobs.construct_job_url(url_prefix, url_suffix)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def get_job_name(self, repository_name, job_type):
        """Return the job name w/o the full URL to CI."""
        assert job_type in {"build_job", "test_job", "pylint_job", "pydoc_job"}
        try:
            repository_name = CIJobs.remove_prefix(repository_name, "fabric8-analytics-")
            url_suffix = self.config.get(repository_name, job_type)
            return url_suffix
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    @staticmethod
    def construct_job_url(url_prefix, url_suffix):
        """Construct the URL to job on CI from CI prefix and suffix with job name."""
        return urljoin(urljoin(url_prefix, "job/"), url_suffix)

    @staticmethod
    def remove_prefix(text, prefix):
        """Remove the prefix from input string (if the string starts with prefix)."""
        return text[len(prefix):] if text.startswith(prefix) else text
