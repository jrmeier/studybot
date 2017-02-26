#!/usr/bin/env python
# =============================================================================
# File Name:     engine.py
# Author:        Jed Meier
# Contact:       jedm@iastate.edu
# Creation Date: 2017-02-25
# =============================================================================

'''
Purpose: function to implement all the classes and data instructions
'''

import helpers.smooch as comm
import helpers.user as user
import urllib3
import intents

def compute(smoochid, msg, device, postback, metadata):
    urllib3.disable_warnings()
    '''
    '''
    # initialize the classes
    print "u_comm initializing ..."
    u_comm = comm.Comm(smoochid=smoochid, user_text=msg, metadata=metadata, device=device)
    print "u_comm finished runninug"
    u_data = user.UserData(smoochid=smoochid)

    print "msg: ", msg
    if msg == "quit":
        intents.quit_studying(u_comm, u_data)
    print "postback: ", postback
    if msg == "missing message":
        print "MISSING MESSSAGE"
        return True

    try:
        # if there is a postback that is for sure the intent
        if postback:
            curr_intent = postback
        else:
            print "there wasn't a post back!"
            # grabs the previous intent
            curr_intent = u_data.get_data('intent')

        u_data.post_data({'intent': curr_intent})

        # Prints user data at this stage
        u_data.print_all()

        if u_data.get_data('intent') == "newUser":
            intents.newUser(u_comm, u_data, metadata)
            print "newUser"

        elif u_data.get_data('intent') == "start_studying":
            u_comm.send_msg("okay, cool. Let's get started")
            print "start_study"
        elif u_data.get_data('intent') == "quit_studying":
            u_comm.send_msg("Okay, we will stop!")
            print "I hate this"
        else:
            u_comm.send_msg("Hmm. That's not supposed to happen!")
            print "what just happend?"
    except Exception as e:
        error = str(repr(e))
        print "Error", e
    u_data.write_data()
    u_comm.execute_queue()
    return "Done"

if __name__ == "__main__":
    msg = "test"
    device = "what"
    postback = "newUser"
    metadata = None
    print compute("683a60ded0ca72b599ee73b5", msg, device, postback, metadata)
