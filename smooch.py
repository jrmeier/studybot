#!/usr/bin/env python
# =============================================================================
# File Name:     smooch.py
# Author:        Jed Meier
# Contact:       jedm@iastate.edu
# Creation Date: 2017-24-2017
# =============================================================================

import requests, json, sys, random, time


class Comm:
    '''
    Initializes with the smoochid, user's text, and the device
    A empty queue is created as well. The queue will house the messages to be sent.
    The device can be: "local" (development), "facebook", "sms", "email", "
    '''

    def __init__(self, smoochid, user_text, metadata, device):
        self.smoochid = smoochid
        self.metadata = metadata
        self.user_text = user_text
        self.device = device
        self.smoochAppName = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFwcF81OGIwZmM5Y2EwNjRmZjY0MDBlN2EyZmEifQ.eyJzY29wZSI6ImFwcCJ9.qaETkxz039oyxrdnDpf2XQwxe6DlnutmlI9PG0Gb5Gc'
        self.smoochAppId = 'app_58b0fc9ca064ff6400e7a2fa'
        self.bearer = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFwcF81OGIwZmM5Y2EwNjRmZjY0MDBlN2EyZmEifQ.eyJzY29wZSI6ImFwcCJ9.qaETkxz039oyxrdnDpf2XQwxe6DlnutmlI9PG0Gb5Gc'
        self.header = {'content-type': 'application/json', 'authorization': self.bearer}
        self.queue = []
        self.typing_status = False

    '''
    Adds the passed text string to the queue
    '''
    def send_msg(self, text):
        # type: (object) -> object
        # send msg to the smoochid of this instance by adding to queue
        try:
            payload = {"text": str(text), "role": "appMaker"}
            self.queue.append(payload)
            return True
        except Exception:
            print "Error: send_msg function in Comm module ..."
            print "Unexpected error:", sys.exc_info()[0]
            raise

    '''
    Sends an action to user. Array or scalar.
    Determines if it is a postback or URI, use _type="reply" for a reply
    '''

    def get_webhooks(self):
        payload = {
            'triggers':['message:appUser']
        }
        read = requests.get(
            'https://api.smooch.io/v1/webhooks/',
            headers=self.header)
        return read.content


    def send_action_old(self, msg, actions):
        payload = {"text": msg, "role": "appMaker", "actions": []}
        payload['actions'] = actions
        self.queue.append(payload)
        return True

    def send_carousel(self, items):
        payload = {"role": "appMaker", "items": []}
        payload['items'] = items
        self.queue.append(payload)

    def typing_indicator(self, status=False):

        typing = {'role': 'appMaker', 'items': []}

        if status:
            typing['type'] = 'typing:start'
            self.typing_status = True
        else:
            typing['type'] = 'typing:stop'
            self.typing_status= False
        typing_status = requests.post(
            'https://api.smooch.io/v1/appusers/' + str(self.smoochid) + '/conversation/activity/',
            headers=self.header, json=typing)

        return typing_status

    def execute_queue(self):

        if self.device == 'local':
            print "********** Bot Response **********"
            for each in self.queue:
                print str(each)
        else:
            print "Executing queue on user..."
            if not self.typing_status:
                self.typing_indicator(True)

            for each in self.queue:
                wait = round(random.uniform(.5, 2), 2)
                time.sleep(wait)
                self.typing_indicator(False)
                read = requests.post(
                    'https://api.smooch.io/v1/appusers/' + str(self.smoochid) + '/messages', json=each,
                    headers=self.header)

                if read.status_code == 201 or read.status_code == 200:
                    pass
                else:
                    print "status code: ", read.status_code
                    return False
            return True


    def send_media(self, media):
        payload = {"mediaUrl": str(media), "mediaType": "image/jpeg","role": "appMaker"}
        self.queue.append(payload)

    def empty_queue(self):
        self.queue = []
        print "queue is reset"


    '''
    Get all messages.
    before = True (grabs all data)
    before = Unix time for before a specific time
    ex. get_messages(before=1471995721)
    Max of 100 messages
    '''
    def get_messages(self, before=False):
        headers = {'app-token': os.environ['APPTOKEN']}

        before = str(before) if before else  str(int(time.time()))

        read = requests.get(
            'https://api.smooch.io/v1/appusers/' + str(self.smoochid) + '/messages?before='+before ,
            headers=headers)  # Lets send it

        if read.status_code == 200:
            return json.loads(read.content)
        else:
            raise Exception("Error in get_messages. Smooch status code: ", read.status_code)

    def count_all_messages(self):
        next_time = time.time()
        ret = x.get_messages(before=next_time)
        count = 0
        while (len(ret['messages'])):
            count += len(ret['messages'])
            next_time = ret['messages'][0]['received']
            ret = x.get_messages(before=next_time)
        return count

if __name__ == "__main__":
    smoochid = ""
    x = Comm(smoochid=smoochid, user_text="tester", metadata=None, device='not local')
    print x.get_webhooks()



