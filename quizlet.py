#!/usr/bin/env python
# =============================================================================
# File Name:     quizlet.py
# Author:        Jed Meier
# Contact:       jedm@iastate.edu
# Creation Date: 2017-02-25
# =============================================================================
import requests
import json
from random import randint

class Quizlet:

    def __init__(self, user):
        self.user = user
        self.base = "http://api.quizlet.com"

    def get_sets(self):
        code = "https://api.quizlet.com/2.0/users/"+self.user+"/sets"
        headers = {'Authorization': 'Bearer sVCXymGVgRXkuj94V6NnnTj9RegXZJ7x8A6Je68Z'}
        req = requests.get(code,headers=headers)
        #req = requests.get('https://api.quizlet.com/2.0/users/jed_meier',headers)
        return json.loads(req.content)

    def get_terms(self):
        code = "https://api.quizlet.com/2.0/sets/415/terms"
        headers = {'Authorization': 'Bearer sVCXymGVgRXkuj94V6NnnTj9RegXZJ7x8A6Je68Z'}
        req = requests.get(code,headers=headers)
        #req = requests.get('https://api.quizlet.com/2.0/users/jed_meier',headers)
        return json.loads(req.content)

    def json_array(self):
        code = "https://api.quizlet.com/2.0/sets/415/terms"
        headers = {'Authorization': 'Bearer sVCXymGVgRXkuj94V6NnnTj9RegXZJ7x8A6Je68Z'}
        req = requests.get(code,headers=headers)
        #req = requests.get('https://api.quizlet.com/2.0/users/jed_meier',headers)
        jsonArray = json.loads(req.content)

        return jsonArray[randint(0, 50)]

if __name__ == '__main__':
    qz = Quizlet("Brian_Espinosa854")
 #   print qz.get_sets()
 #   print qz.get_terms()
    currentCard=qz.json_array()

    print currentCard
    print (currentCard['definition'])
