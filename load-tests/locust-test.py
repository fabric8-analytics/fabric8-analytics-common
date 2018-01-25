from locust import HttpLocust, TaskSet
import os

api = "/api/v1/stack-analyses"
fp = open('data/pom-effective.xml')
fp1 = fp.read()

RECOMMENDER_API_TOKEN = os.getenv('RECOMMENDER_API_TOKEN')


class UserBehavior(TaskSet):
    def fetch(self):

        response = self.client.post(api, files={'manifest[]': ('pom.xml', fp1)},
                                    data={'analytics_cache': '1', 'filePath[]': '/home/JohnDoe'},
                                    headers={'Authorization': 'Bearer {}'.format(RECOMMENDER_API_TOKEN)})
        print(response.json())

    tasks = {fetch: 1}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 100
