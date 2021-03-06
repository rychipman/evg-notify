import requests

BASE_URL = 'https://evergreen.mongodb.com/rest/v1'

def _get_url(job_type, job_id):
    '''Generates the URL for the API endpoint of an Evergreen job.

    `job_type` - the type of job being run (e.g. 'builds', 'tasks')
    `job_id` - the ID of the job on Evergreen (i.e. the part of the URL after
    "evergreen.mongodb.com/[job_type]/")

    Returns the URL as a string.
    '''
    return '{}/{}/{}'.format(BASE_URL, job_type, job_id)

def get_build_url(build_id):
    '''Generates the URL for the API endpoint of an Evergreen build.

    `build_id` - the ID of the build on Evergreen (i.e. the part of the URL after
    "evergreen.mongodb.com/build/")

    Returns the URL as a string.
    '''
    return _get_url('builds', build_id)

def get_patch_url(patch_id):
    '''
    Generates the URL for the API endpoint of an Evergreen patch.

    `patch_id` - the ID of the task on Evergreen (i.e. the part of the URL after
    "evergreen.mongodb.com/patch/")

    Returns the URL as a string.
    '''
    return _get_url('patches', patch_id)

def get_task_url(task_id):
    '''
    Generates the URL for the API endpoint of an Evergreen task.

    `task_id` - the ID of the task on Evergreen (i.e. the part of the URL after
    "evergreen.mongodb.com/task/")

    Returns the URL as a string.
    '''

    return _get_url('tasks', task_id)

def get_version_url(version_id):
    '''
    Generates the URL for the API endpoint of an Evergreen version.

    `version_id` - the ID of the version on Evergreen (i.e. same as the patch ID)

    Returns the URL as a string.
    '''
    return _get_url('versions', version_id)
