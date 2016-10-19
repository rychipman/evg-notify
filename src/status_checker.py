from api_key import EVERGREEN_API_KEY
from url_builder import get_build_url, get_task_url

import requests

class StatusChecker:
    '''Makes requests to the Evergreen API to determine the status of various jobs.'''

    def __init__(self, username):
        '''`username` - user\'s JIRA username'''
        self.headers = {
            'Auth-Username': username,
            'Api-Key': EVERGREEN_API_KEY,
        }

    def _make_request(self, url):
        response = requests.get(url, headers=self.headers)

        if response.status_code != requests.codes.ok:
            return None

        response_body = response.json()

        return response_body.get('status')

    
    def get_build_status(self, build_id):
        '''Checks the status of an Evergreen build. 
        
        `build_id` - the ID of the build on Evergreen (i.e. the part of the URL after 
        "evergreen.mongodb.com/build/")
            
        Returns the status string of the build, or `None` if the build can\'t be found.
        '''
        return self._make_request(get_build_url(build_id))

    def get_build_status(self, build_id):
        '''Checks the status of an Evergreen tasks.
           
        `task_id` - the ID of the task on Evergreen (i.e. the part of the URL after 
        "evergreen.mongodb.com/task/")
            
        Returns the status string of the task, or `None` if the task can\'t be found.
        '''
        return self._make_request(get_build_url(build_id))



