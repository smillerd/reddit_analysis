#!/usr/bin/python

"""
This version is being developed to run on a server, not on the host machine or a guest machine.
The server is running 64-bit Ubuntu with python3 and python2.7 installed
It is to work in conjunction with rRecord - rRecord takes temp.csv and stores it on MySQL database
"""
import praw
import os
import csv

# Initialize:
# connect to reddit
user_agent = "rQuery:v1.2.1 by Drellim14"
r = praw.Reddit(user_agent=user_agent)
# TODO login

# list for the data being recorded
top_posts = []
def RASID_open():
    with open('RASID.txt', 'r') as f:
        RASID = f.read()
        RASID = RASID.split("\n")
        RASID = filter(None, RASID)

# Random-Access Sumbission ID, or RASIDl, records the posts that are currently being tracked
# Check to see if the RASID.txt exists, read its contents into a RASIDl list
if os.path.isfile('RASID.txt'):
    RASID_open()
else:
    RASIDl = []

# IF RASIDl doesn't exist, create the list, generate posts, and record data, second parameter is for when RASIDl is
# archived
if not os.path.isfile('RASID.txt'):
    RASIDl = []
    subreddit = r.get_subreddit('trees')  # TODO change subreddit to user entry
    for submission in subreddit.get_hot(limit=5):  # TODO change limit to user entry
        submission_data = {'title': submission.title, 'author': submission.author,
                           'num_comments': submission.num_comments, 'downs': submission.downs, 'ups': submission.ups,
                           'score': submission.score, 'submission_id': submission.id}

        # add posts to top_posts - the list used to move data in program
        if submission.id not in RASIDl:
            top_posts.append(submission_data)
            submission_length = len(submission_data)
            print ('another post another toke')

    # create RASID.txt
    with open('RASID.txt', 'w') as f:
        for post_id in RASIDl:
            f.write(post_id)

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
    # this parameter will eventually need to be the factor that decides whether to archive the RASIDl functions
    # TODO edit parameter
    parameter = False
    if not parameter:
        for submission in RASIDl:  # hopefully this works.... I'm calling the submission_id, and I'm not sure
            submission_data = {'title': submission.title, 'author': submission.author,
                               'num_comments': submission.num_comments, 'downs': submission.downs,
                               'ups': submission.ups, 'score': submission.score,
                               'submission_id': submission.id}  # that the submission id works with the . attributes...

            if submission.id in RASIDl:
                top_posts.append(submission_data)
                print ('Joint number 2')

    # Archive method:
    else:
        pass

    # write RASIDl back to a txt file
    with open('RASID.txt', 'w') as f:
        for post_id in RASIDl:
            f.write(post_id)

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

# TODO write functions for pulling data
# TODO eliminate for loops