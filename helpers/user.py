#!/usr/bin/env python
# =============================================================================
# File Name:     communication.py
# Author:        Jed Meier
# Contact:       jedm@iastate.edu
# Creation Date: 2017-02-24
# =============================================================================

'''
Purpose: Grabs all the user's information. Functions for editing and querying
         the user information as instance variables. Posts the information back
         to the database to save the user data.
'''

from pymongo import MongoClient
from datetime import datetime, timedelta
import datetime
import os


class UserData:
    '''
    Initialize by pulling all the user information from the database
    '''

    def __init__(self, smoochid):
        # save all the user_data from the database to an object
        self.smoochid = smoochid
        self.connect_to_db()
        givenName = "test given name"
        #get the first returned user (there can only be one because smoochid is a unique key)
        try:
            cursor = self.db.users.find({"smoochid": smoochid})
            self.user_obj = list(cursor)[0]
            print "User found."
        except:
            print "Couldn't find user: ", smoochid
            self.new_user(givenName)

        # we don't want to mess with the mongo unique id
        self.user_obj.pop('_id')

    def new_user(self, givenName):
        print "Creating new mongo user for: ", self.smoochid
        # This should be the standard for new user creation intent 18 to show the initial message
        self.db.users.insert_one({'smoochid': self.smoochid,
                                  'intent': 'newUser',
                                    'first': False,
                                    'qid': False,
                                })

        # User is created. Now let's store their information locally in user_obj
        cursor = self.db.users.find({"smoochid": self.smoochid})
        self.user_obj = list(cursor)[0]
        print "User created and stored locally"

    def connect_to_db(self):
        print "Attempting to connect to database..."
        try:
            client = MongoClient('mongodb://localhost:27017/master')
            self.db = client.master

        except:
            raise Exception("Can't connect to Database")

    def get_data(self, property):
        # get a value from a property from the user object
        if property == 'all':
            return self.user_obj

        try:
            return self.user_obj[property]
        except:

            return None

    def post_data(self, obj, force=False):

        # edit local data
        try:
            for key, value in obj.iteritems():
                if value not in ['Nonexists', None, [], 'Nonexist', [None]] or force:
                    self.user_obj[key] = value
                    self.user_obj['last_active'] = datetime.datetime.now()
                    print "POSTED key: " + str(key) + " | Value: "+str(value)
        except:
            raise Exception("Couldn't write to user_obj using post_data")

    def print_all(self):
        print "*************************************"
        print "Current states of smoochid: ", self.smoochid
        for each in self.user_obj:
            print each, " : ", self.user_obj[each]
        print "*************************************"

    def write_data(self):
        # write the user_obj variables back into the database
        res = self.db.users.update_one({"smoochid": self.smoochid}, {'$set': self.user_obj})
        return res

    def remove_user(self):
        self.db.users.remove({'smoochid': self.smoochid})


if __name__ == "__main__":
    user = UserData("abc")
    user.remove_user()
    user.print_all()
