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

class quizlet:
    def __init__(self, u_data):
        self.user = u_data.get_data('qid')
        self.setId = str(u_data.get_data('deck'))
        self.base = "https://api.quizlet.com/2.0/users/"
        self.header = {'Authorization': 'Bearer sVCXymGVgRXkuj94V6NnnTj9RegXZJ7x8A6Je68Z'}

    def get_sets(self):
        req = requests.get(self.base+self.user+"/sets",headers=self.header)
        sets = json.loads(req.content)
        titles = []
        for each in sets:
            titles.append({'title': each['title'], 'id': each['id']})
        return titles


    def get_terms(self):
        code = "https://api.quizlet.com/2.0/sets/191423753/terms"
        req = requests.get(code,headers=headers)
        return json.loads(req.content)

    def random_card(self):
        url = "https://api.quizlet.com/2.0/sets/"+self.setId+"/terms"
        headers = {'Authorization': 'Bearer sVCXymGVgRXkuj94V6NnnTj9RegXZJ7x8A6Je68Z'}
        req = requests.get(url, headers=headers)
        jsonArray = json.loads(req.content)

        return random.choice(jsonArray)

if __name__ == '__main__':
    qz = quizlet("Brian_Espinosa854")
    print qz.get_sets()
