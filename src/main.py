from evergreen_requester import EvergreenRequester
from mailer import Mailer
from api_key import SENDGRID_API_KEY
import argparse
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--patch', dest='patch_id', help='patch ID to monitor')
    parser.add_argument('--notify', dest='notify', default='patch', help='granularity for email notifications')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    num_retries = 10
    patch_id = args.patch_id
    requester = EvergreenRequester()
    username = requester.get_username()

    print("Start monitoring patch {} by {}".format(patch_id, username))

    # Query for patch status until we run out of retries or receive
    # success or failed. Reset retries if EvergreenRequester tells us the
    # patch has not been configured yet.
    while (num_retries > 0):
        patch_info = requester.get_patch_status(patch_id)
        patch_status = patch_info['status']
        print("Patch Status: {}".format(patch_status))
        if patch_status == 'success' or patch_status == 'failed':
            break
        elif patch_status != None:
            num_retries = 10
        else:
            num_retries -= 1
        time.sleep(60)

    print("Patch Completed! status={}".format(patch_status))

    # If patch successfully completed, retrieve the build IDs and send email.
    if patch_status != None:
       print("Emailing {}@mongodb.com".format(username))
       build_statuses = {}
       build_statuses_string = ""
       for build_id in patch_info['builds']:
           build_status = requester.get_build_status(build_id)
           if build_status != None:
               build_statuses[build_id] = build_status
               build_statuses_string += "<b>{}</b>: {}<br>".format(
                       build_id, build_status)
       patch_description = requester.get_patch_description(patch_id)
       if patch_description == None:
           patch_description = patch_id
       evergreen_link = 'https://evergreen.mongodb.com/version/{}'.format(
               patch_id)
       to_email = '{}@mongodb.com'.format(username)
       subject = '{}: {}'.format(patch_status, patch_description)
       body = ('Hello {}, patch <b><a href=\"{}\">{}</a></b> has finished '
               'running in evergreen with status={}. Please find the build '
               'statuses for this patch below:<br><br>{}'.
               format(username, evergreen_link, patch_description,
                   patch_status,build_statuses_string))
       mailer = Mailer(SENDGRID_API_KEY)
       status = mailer.send(to_email, subject, body)
       print("Sendgrid Status Code: {}".format(status))

main()
