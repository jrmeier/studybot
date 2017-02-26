#!/usr/bin/env python
# =============================================================================
# File Name:     intents.py
# Author:        Jed Meier
# Contact:       jedm@iastate.edu
# Creation Date: 2017-25-2017
# =============================================================================

from quizlet import quizlet


def newUser(u_comm, u_data, metadata):
    u_comm.send_msg("Hello!")
    actions = [{"type": 'postback','text':'Set 1','payload':'start_studying','metadata': {'id':'id 1'}}]
    u_comm.send_action(msg="Chose which set to study!", actions=actions)


def quit_studying(u_comm, u_data):
    u_comm.send_msg("Okay, we can take a break for awhile")
    u_data.post_data({'intent':'quit_studying'})


def start_studying(u_comm, u_data):
    qz = quizlet("Brian_Espinosa854")
    sets = qz.get_sets()
    actions = []
    temp = []
    for set in sets:
        temp = {'type': 'postback',
                'text': set['title'],
                'payload': 'study_deck',
                'metadata': {'id': str(set['id'])}
                }
        actions.append(temp)
    u_comm.send_action(msg="Choose which deck to study",actions=actions)



if __name__ == "__main__":
    start_studying()