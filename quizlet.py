#!/usr/bin/env python
# =============================================================================
# File Name:     quizlet.py
# Author:        Jed Meier
# Contact:       jedm@iastate.edu
# Creation Date: 2017-02-25
# =============================================================================
import requests
import json

class Quizlet:

    def __init__(self, user):
        self.user = user
        self.base = "http://api.quizlet.com"

    def get_sets(self):
        code = "https://api.quizlet.com/2.0/users/Brian_Espinosa854/sets"
        headers = {'Authorization': 'Bearer K7QNY7NYCY7YcMNr9bnjhHhRTmKnUjuxuFyYCSN6'}
        req = requests.get(code,headers=headers)
        #req = requests.get('https://api.quizlet.com/2.0/users/jed_meier',headers)
        return json.loads(req.content)
if __name__ == '__main__':
    qz = Quizlet("jed_meier")
    print qz.get_sets()