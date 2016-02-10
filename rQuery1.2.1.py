#!/usr/bin/python

"""
This version is being developed to run on a server, not on the host machine or a guest machine.
The server is running 64-bit Ubuntu with python3 and python2.7 installed
It is to work in conjunction with rRecord - rRecord takes temp.csv and stores it on MySQL database
"""
import praw
import os
import csv
import MySQLdb

# Initialize:
# connect to reddit
user_agent = "rQuery:v1.2.1 by Drellim14"
r = praw.Reddit(user_agent=user_agent)
# TODO login

# list for the data being recorded
top_posts = []
ralid = []
class RASID():
    # ralid is the list that will be used inside python to represent the RASID.txt file
                                                                # TODO RASID class could be replaced by tempfile solution
                                        # TODO This could be simplified in the future by using IF NOT EXIST or whatever in MySQL
    def __init__(self):
        pass
    def RASID_open(self):
        with open('RASID.txt', 'r') as f:
            ralid = f.read()
            ralid = ralid.split("\n")
            ralid = filter(None, ralid)

    def RASID_open_new(self):
        with open('RASID.txt', 'w'):
            pass

    def RASID_check(self):
        if os.path.isfile('RASID.txt'):
            return True
        else:
            return False

    def RASID_ralid(self, x):
        ralid = []
        ralid.append(x)

    def RASID_write(self):
        if ralid:
            with open('RASID.txt', 'w') as f:
                f.write(ralid)


    def RASID_del(self):
        os.remove('RASID.txt')


#This retrieves the list of post_ids that we care about so that we can record the data for those posts
#After some time we will replace the post_ids on this list with more current post_ids
RASID_inst = RASID()
if RASID_inst.RASID_check():
    RASID_inst.RASID_open()
else:
    RASID_inst.RASID_open_new()


# IF ralid doesn't exist, create the list, generate posts, and record data, second parameter is for when ralid is
# archived
if not os.path.isfile('RASID.txt'):
    ralid = []
    subreddit = r.get_subreddit('trees')  # TODO change subreddit to user entry
    for submission in subreddit.get_hot(limit=5):  # TODO change limit to user entry
        submission_data = {'title': submission.title, 'author': submission.author,
                           'num_comments': submission.num_comments, 'downs': submission.downs, 'ups': submission.ups,
                           'score': submission.score, 'submission_id': submission.id}

        # add posts to top_posts - the list used to move data in program
        if submission.id not in ralid:
            top_posts.append(submission_data)
            submission_length = len(submission_data)
            print ('another post another toke')

    # this temporary csv file is used to temporarily store data. This data will be read and written to a MySQL database
    # by rRecord
    with open('temp.csv', 'w') as f:
        fieldnames = ['title',
                      'author',
                      'num_comments',
                      'downs',
                      'ups',
                      'score',
                      'submission_id',
                      ]
        dict_writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
        dict_writer.writeheader()
        for post in top_posts:
            dict_writer.writerow(post)

else:
    # this parameter will eventually need to be the factor that decides whether to archive the ralid functions
    # TODO edit parameter
    parameter = False
    if not parameter:
        for submission in ralid:  # hopefully this works.... I'm calling the submission_id, and I'm not sure
            submission_data = {'title': submission.title, 'author': submission.author,
                               'num_comments': submission.num_comments, 'downs': submission.downs,
                               'ups': submission.ups, 'score': submission.score,
                               'submission_id': submission.id}  # that the submission id works with the . attributes...

            if submission.id in ralid:
                top_posts.append(submission_data)
                print ('Joint number 2')

    # Archive method:
    else:
        pass

    # this temporary csv file is used to temporarily store data. This data will be read and written to a MySQL database
    # by rRecord
    with open('temp.csv', 'w') as f:
        fieldnames = ['title',
                      'author',
                      'num_comments',
                      'downs',
                      'ups',
                      'score',
                      'submission_id',
                      ]
        dict_writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
        dict_writer.writeheader()
        for post in top_posts:
            dict_writer.writerow(post)


for x in ralid:
    RASID_inst.RASID_ralid(x)
RASID_inst.RASID_write()
# TODO write functions for pulling data
# TODO eliminate for loops