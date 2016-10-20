from evergreen_requester import EvergreenRequester
from mailer import Mailer
from api_keys import SENDGRID_KEY
import argparse
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--patch', dest='patch_id', help='patch ID to monitor')
    args = parser.parse_args()
    num_retries = 10
    patch_id = args.patch_id
    requester = EvergreenRequester()
    username = requester.get_username()

    # Query for patch status until we run out of retries or receive
    # success or failed. Reset retries if EvergreenRequester tells us the
    # patch has not been configured yet.
    while (num_retries > 0):
        patch_info = requester.get_patch_status(patch_id)
        patch_status = patch_info['status']
        if patch_status == 'success' or patch_status == 'failed':
            break
        elif patch_status != None:
            num_retries = 10
        else:
            num_retries -= 1
        time.sleep(60)

    # If patch successfully completed, retrieve the build IDs and send email.
    if patch_status != None:
       build_statuses = {}
       for build_id in patch_info['builds']:
           build_status = requester.get_build_status(build_id)
           if build_status != None:
               build_statuses[build_id] = build_status
       to_email = '{}@mongodb.com'.format(username)
       subject = 'Patch {} completed with status: {}'.format(patch_id, patch_status)
       body = 'Hello {}, patch {} has finished running in evergreen with '\
               'status {}. Please find the build statuses for this patch '\
               'below:<br>{}'.format(username, patch_id, patch_status, str(build_statuses))
       mailer = Mailer(SENDGRID_KEY)
       mailer.send(to_email, subject, body)

main()
