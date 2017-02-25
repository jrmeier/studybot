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

nope = ['Nonexists', None, [], 'Nonexist']

def compute(smoochid, msg, device, postback, metadata):
    '''
    Main engine that passes variables to all modules. Brain of Holmes :)
    '''
    # initialize the classes
    print "u_comm initializing ..."
    u_comm = comm.Comm(smoochid=smoochid, user_text=msg, metadata=metadata)
    print "u_comm finished runninug"
    u_data = user.UserData(smoochid=smoochid)

    u_comm.typing_indicator(True)

    print "msg: ", msg
    if msg == "missing message":
        print "MISSING MESSSAGE"
        return True

    try:
        # if there is a postback that is for sure the intent
        if postback:
            curr_intent = int(postback)
        else:
            print "there wasn't a post back!"
            # grabs the previous intent
            past_intent = u_data.get_data(property='intent')
            curr_intent = 'study'
            # given the previous intent (past_intent) find the execution function they require

        u_data.post_data({'intent': curr_intent})
        if not postback:
            # Extract for the intent and save it to the user
            print "Beginning Extraction ..."

        # Prints user data at this stage
        u_data.print_all()

    except Exception as e:
        error = str(repr(e))
        print "Error", e

    return "what"

if __name__ == "__main__":
    msg = "test"
    device = "what"
    postback = None
    metadata = None
    print compute("abc123",msg, device, postback, metadata)