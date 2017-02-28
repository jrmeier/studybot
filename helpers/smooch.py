#!/usr/bin/env python
# =============================================================================
# File Name:     smooch.py
# Author:        Jed Meier
# Contact:       jedm@iastate.edu
# Creation Date: 2017-24-2017
# =============================================================================

import requests, json, sys, random, time
import config


class Comm:
    '''
    Initializes with the smoochid, user's text, and the device
    A empty queue is created as well. The queue will house the messages to be sent.
    The device can be: "local" (development), "facebook", "sms", "email", "
    '''

    def __init__(self, smoochid, user_text, metadata, device):
        self.device = device
        self.smoochid = smoochid
        self.metadata = metadata
        self.user_text = user_text
        self.smoochAppId = config.appID()
        self.bearer = config.bearer()
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

    def send_action(self, msg, actions):
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
            self.typing_indicator(True)
            for each in self.queue:
                #wait = round(random.uniform(.01, .1), 2)
                #time.sleep(wait)
                read = requests.post(
                    'https://api.smooch.io/v1/appusers/' + str(self.smoochid) + '/messages', json=each,
                    headers=self.header)
                if read.status_code == 201 or read.status_code == 200:
                    pass
                else:
                    print "status code: ", read.content
                    return False
            return True
            

    def empty_queue(self):
        self.queue = []
        print "queue is reset"

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
    smoochid = "683a60ded0ca72b599ee73b5"
    x = Comm(smoochid=smoochid, user_text="tester", metadata=None, device='not local')
    print x.send_msg(text="lol")
    print x.execute_queue()


