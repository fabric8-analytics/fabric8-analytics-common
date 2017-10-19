class Results():

    def __init__(self):
        self.core_api = False
        self.jobs_api = False
        self.core_api_auth_token = False
        self.jobs_api_auth_token = False

    def __repr__(self):
        template = "Core API: {c}\nJobs API: {j}\n" + \
                   "Core API auth: {ca}\nJobs API auth: {ja}"
        return template.format(c=self.core_api, j=self.jobs_api,
                               ca=self.core_api_auth_token, ja=self.jobs_api_auth_token)
