import os


class ServerConfiguration():

    @staticmethod
    def get_env_var(name, postfix):
        return os.environ.get("{name}_{postfix}".format(name=name, postfix=postfix))

    def __init__(self, env_var_posfix):
        self.core_api_url = ServerConfiguration.get_env_var('F8A_API_URL', env_var_posfix)
        self.jobs_api_url = ServerConfiguration.get_env_var('F8A_JOB_API_URL', env_var_posfix)
        self.core_api_token = ServerConfiguration.get_env_var('RECOMMENDER_API_TOKEN',
                                                              env_var_posfix)
        self.jobs_api_token = ServerConfiguration.get_env_var('JOB_API_TOKEN', env_var_posfix)
