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


def compute(smoochid, msg, device, postback, metadata):
    '''
    Main engine that passes variables to all modules. Brain of Holmes :)
    '''
    # initialize the classes
    print "u_comm initializing ..."
    u_comm = comm.Comm(smoochid=smoochid, user_text=msg, metadata=metadata, device=device)
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
            curr_intent = postback
        else:
            print "there wasn't a post back!"
            # grabs the previous intent
            curr_intent = u_data.get_data('intent')

        u_data.post_data({'intent': curr_intent})

        # Prints user data at this stage
        u_data.print_all()

        if u_data.get_data('intent') == "newUser":
            u_comm.send_msg("hello new user!")

        elif u_data.get_data('intent') == "start_study":
            u_comm.send_msg("okay, cool. Let's get started")

        elif u_data.get_data('intent') == "quit_study":
            u_comm.send_msg("Okay, we will stop!")
        else:
            u_comm.send_msg("Hmm. That's not supposed to happen!")
        u_data.write_data()
        u_comm.execute_queue()
    except Exception as e:
        error = str(repr(e))
        print "Error", e

    return "Done"

if __name__ == "__main__":
    msg = "test"
    device = "what"
    postback = "newUser"
    metadata = None
    print compute("683a60ded0ca72b599ee73b5", msg, device, postback, metadata)