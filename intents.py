#!/usr/bin/env python
# =============================================================================
# File Name:     intents.py
# Author:        Jed Meier
# Contact:       jedm@iastate.edu
# Creation Date: 2017-25-2017
# =============================================================================

def newUser(u_comm, u_data, metadata):
    u_comm.send_msg("Hello!")
    actions = [{"type": 'postback','text':'Set 1','payload':'start_studying','metadata': {'id':'id 1'}}]
    u_comm.send_action(msg="Chose which set to study!", actions=actions)

def quit_studying(u_comm, u_data):
    u_comm.send_msg("Okay, we can take a break for awhile")
    u_data.post_data({'intent':'quit_studying'})

