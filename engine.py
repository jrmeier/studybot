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
import intents
from fuzzywuzzy import fuzz
import re

def check_answer(correct, user):
    answer = re.sub("[?]","", correct).lower()
    user = re.sub("[?]","", user).lower()    

    wsimple = fuzz.ratio(answer, user) * .3
    wpartial = fuzz.partial_ratio(answer, user) * .35
    wtoken = fuzz.token_set_ratio(answer, user) * .35
    score = (wsimple + wpartial + wtoken)

    return score




def compute(smoochid, msg, device, postback, metadata, intent=None):
    '''
    '''
    # initialize the classes
    print "u_comm initializing ..."
    u_comm = comm.Comm(smoochid=smoochid, user_text=msg, metadata=metadata, device=device)
    print "u_comm finished runninug"
    u_data = user.UserData(smoochid=smoochid)

    print "msg: ", msg
    print "intent: ",u_data.get_data('intent')
    print metadata
    u_data.print_all()
    u_comm.typing_indicator(True)
    if msg:
        if msg.lower() == "quit":
            intents.quit_studying(u_comm, u_data)
    
    print "postback: ", postback
    
    if msg == "missing message":
        print "MISSING MESSSAGE"
        return True
    #if msg is None and u_data.get_data('intent') == "user_register":
    #print "msg was none"
    #return 
    if u_data.get_data('checkAnswer'):
        first = u_data.get_data('first')
        if first == 'term':
            check = 'def'
        elif first == 'definition':
            check = 'term'
        try:
            score = check_answer(u_data.get_data(check), msg)
        except:
            score = ""
            pass
        wrong = True
        if(score == 100):
            msg = "Perfect answer! :)"
            wrong = False
        elif(score >= 95 and score < 100):
            msg = "You are so close, I'll give it too you! :)"
        elif(score >= 90 and score < 95):
            msg = "Close, but not quite" 
        elif(score >= 80 and score < 90):
            msg = "You're warm, but not hot."
        elif(score >= 70 and score < 80):
            msg = "Hmm. That's not it. Make sure typing your answers how they appear on the cards!"
        elif(score < 69):
            msg = "Thats not right. :("
        else:
            msg = "Hmm. I couldn't check that answer. Sorry!"
        
        u_comm.send_msg(msg)
        u_data.post_data({'num_of_q': u_data.get_data('num_of_q')+1 })
        if wrong:
            cmessage = "The correct answer was: "+ str(u_data.get_data(check))
            u_comm.send_msg(cmessage)
            u_data.post_data({'incorrect': u_data.get_data('incorrect')+1 })
        else:
            print "stop"
            u_data.post_data({'correct': u_data.get_data('correct')+1 })
        u_data.post_data({'checkAnswer': False})
    

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
        elif u_data.get_data('intent') == "save_first":
            intents.save_first(u_comm, u_data, metadata)
        elif u_data.get_data('intent') == "study_deck":
            intents.study_deck(u_comm, u_data, metadata)

        elif u_data.get_data('intent') == "start_studying":
            intents.start_studying(u_comm, u_data)
            print "start_study"
        elif u_data.get_data('intent') == "quit_studying":
            u_comm.send_msg("Okay, we will stop!")
            print "I hate this"
        elif u_data.get_data('intent') == "user_register":
            intents.user_register(u_comm, u_data, msg)
        elif u_data.get_data('intent') == "studying":
            intents.studying(u_comm, u_data)
            #u_comm.send_msg("okay your intent is studying")
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
    postback = None
    intent = "start_studying"
    metadata = None
    text = raw_input("User Text: ")
    print compute("683a60ded0ca72b599ee73b5", text, device, postback, metadata, intent=intent)

