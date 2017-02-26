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
    u_comm.send_msg("Click to link quizlet http://130.211.227.127/quizlet/qz.php")
    u_comm.send_msg("Please enter the username EXACTLY how it appear on the page")
    return u_comm.send_action(msg = "tap the button when you're ready",actions=[{'type':'postback','text':'Got it','payload':'user_register','metadata': {}}])
    #u_data.post_data({'intent':'user_register'})
    
def user_register(u_comm, u_data, msg):
    print "at user_register"
    if msg is None:
        u_comm.send_msg("please enter your username")
        return
    u_data.post_data({'qid': msg})
    u_data.post_data({'intent': 'start_studying'})
    u_comm.send_msg("Thanks!\n Type \"quit\" at any time to stop studying and view your three most recent decks listed your Quizlet account")
    return start_studying(u_comm,u_data)

def quit_studying(u_comm, u_data):
    u_comm.send_msg("Okay, I'm ready to start when you are! :)")
    u_data.post_data({'first':False})
    u_data.post_data({'checkAnswer': False})
    u_data.post_data({'deck': False})
    u_data.write_data()
    return u_data.post_data({'intent':'start_studying'})
    

def study_deck(u_comm, u_data, metadata):
    print "at study deck"
    print metadata
    if metadata is not None:
        print u_data.post_data({'deck': str(metadata['id'])})
    
    if not u_data.get_data('first'):
        u_comm.send_action(msg='What would you like to see first?',actions=[
                {'type': 'postback',
                'text': 'Term',
                'payload': 'save_first',
                'metadata': {'first': 'term'}
                },
                {'type': 'postback',
                'text': 'Definition',
                'payload':'save_first',
                'metadata':{'first':'definition'}
                }])
        return

    u_data.post_data({'intent':'studying'})
    #u_data.post_data({'deck': str(metadata['id'])})
    qz = quizlet(u_data)
    first = u_data.get_data('first')
    #u_comm.send_msg("Type \"quit\" at any time to stop studying and view your three most recent decks listed your Quizlet account")
    u_comm.send_msg(first + " will always be shown first")
    question = qz.random_card()
    u_data.post_data({'term': question['term']})
    u_data.post_data({'def': question['definition']})
    u_data.post_data({'checkAnswer': True})
    u_comm.send_msg(question[first])
    

def studying(u_comm, u_data):
    qz = quizlet(u_data);
    first = u_data.get_data('first')
    question = qz.random_card()
    u_data.post_data({'term': question['term']})
    u_data.post_data({'def': question['definition']})
    u_data.post_data({'checkAnswer': True})
    u_comm.send_msg(question[first])

def save_first(u_comm, u_data, metadata):
    u_data.post_data({'first': metadata['first']})
    return start_studying(u_comm, u_data)

def start_studying(u_comm, u_data):
    qz = quizlet(u_data)
    sets = qz.get_sets()
    actions = []
    temp = []
    if not u_data.get_data('deck'):
        for set in sets:
            temp = {'type': 'postback',
                    'text': set['title'],
                    'payload': 'study_deck',
                    'metadata': {'id': str(set['id'])}
                    }
            actions.append(temp)
        u_comm.send_action(msg="Choose which deck to study",actions=actions)
    else:
        study_deck(u_comm, u_data,{'id':u_data.get_data('deck')})

 
if __name__ == "__main__":
    start_studying()
