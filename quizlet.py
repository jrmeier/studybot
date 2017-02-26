#!/usr/bin/env python
# =============================================================================
# File Name:     quizlet.py
# Author:        Jed Meier
# Contact:       jedm@iastate.edu
# Creation Date: 2017-02-25
# =============================================================================
import requests
import json
import random
import config
class quizlet:
    def __init__(self, u_data):
        self.user = u_data.get_data('qid')
        self.setId = str(u_data.get_data('deck'))
        self.base = "https://api.quizlet.com/2.0/users/"
        
        self.header = {'Authorization': config.qz_bearer()}
    def get_sets(self):
        req = requests.get(self.base+self.user+"/sets",headers=self.header)
        sets = json.loads(req.content)
        titles = []
        for each in sets:
            titles.append({'title': each['title'], 'id': each['id']})
        return titles

    def random_card(self):
        url = "https://api.quizlet.com/2.0/sets/"+self.setId+"/terms"
        req = requests.get(url, headers=self.header)
        jsonArray = json.loads(req.content)

        return random.choice(jsonArray)

if __name__ == '__main__':
    qz = quizlet("")
    print qz.get_sets()
