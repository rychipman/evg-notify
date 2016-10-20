from evergreen_api_key import get_evergreen_api_key
from url_builder import get_build_url, get_task_url, get_version_url

import requests

class EvergreenRequester:
    '''Makes requests to the Evergreen API to determine the status of various jobs.'''

    def __init__(self, username):
        '''`username` - user\'s JIRA username'''
        self.headers = {
            'Auth-Username': username,
            'Api-Key': get_evergreen_api_key(),
        }

    def _make_request(self, url):
        response = requests.get(url, headers=self.headers)
        return response.json()

    
    def get_build_status(self, build_id):
        '''Checks the status of an Evergreen build. 
        
        `build_id` - the ID of the build on Evergreen (i.e. the part of the URL after 
        "evergreen.mongodb.com/build/")
            
        Returns the status string of the build, or `None` if the build can't be found.
        '''
        response_body = self._make_request(get_build_url(build_id))
        return response_body.get('status')

    def get_task_status(self, build_id):
        '''Checks the status of an Evergreen task.
           
        `task_id` - the ID of the task on Evergreen (i.e. the part of the URL after 
        "evergreen.mongodb.com/task/")
            
        Returns the status string of the task, or `None` if the task can't be found.
        '''
        response_body = self._make_request(get_task_url(build_id))
        return response_body.get('status')
    
    def get_patch_status(self, patch_id):
        '''Checks the status of an Evergreen patch.

        `patch_id` - the ID of the task on Evergreen (i.e. the part of the URL after 
        "evergreen.mongodb.com/task/").

        Returns a dictionary with the following keys:
            'status' - the status string of the patch
            'builds' - an array of build ID strings
        '''
        response_body = self._make_request(get_version_url(patch_id))

        if 'status' not in response_body:
            if response_body.get('message') == 'error finding version':
                return {
                    'status': 'not configured',
                    'builds': [],
                }

            return None

        return {
            'status': response_body.get('status'),
            'builds': response_body.get('builds'),
        }
