#!/usr/bin/python

# ToDo turn this into a module for writing any csv file into any MySQL table

import MySQLdb
import csv
import os

# connect to MySQL
conn = MySQLdb.connect('localhost', 'seth', 'cookies')
c = conn.cursor()
c.execute('USE rQuery_data')

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
class Sub_Record:
    def __init__(self,
                 title,
                 author,
                 num_comments,
                 downs,
                 ups,
                 score,
                 post_id):
        self.title = title
        self.author = author
        self.num_comments = num_comments
        self.downs = downs
        self.ups = ups
        self.score = score
        self.post_id = post_id

    def print_attributes(self):
        print self.title
        print self.author
        print self.num_comments
        print self.downs
        print self.ups
        print self.score
        print self.post_id

    def CreateTable(self):
        sql = "CREATE TABLE IF NOT EXISTS %s (title VARCHAR(50) NOT NULL, \
                                  author VARCHAR(20) NOT NULL, \
                                  num_comments SMALLINT UNSIGNED NULL,\
                                  downs MEDIUMINT UNSIGNED NULL, \
                                  ups MEDIUMINT UNSIGNED NULL, \
                                  score MEDIUMINT UNSIGNED NULL, \
                                  post_id VARCHAR(6) NOT NULL PRIMARY KEY); " %self.post_id

        c.execute(sql)

    def AppendTable(self):
        post_id = str(self.post_id)
        title = str(self.title)
        author = str(self.author)
        num_comments = self.num_comments
        downs = self.downs
        ups = self.ups
        score = self.score


        sql = "INSERT INTO '%s'(title, author, num_comments, downs, ups, score, post_id) \
       VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % \
       (post_id, title, author, num_comments, downs, ups, score, post_id)
        try:
            c.execute(sql)
            c.commit
        except:
            pass

    def __destroyTable(self):
        pass  # TODO write destroyTable function in class rQuery_Submission_record
def csv_to_mysql(file):     #function writes file to MySQL database using Sub_Record from record_thing.py
    # retrieve data from temp.csv - store as list_of_dicts = []
    with open(file, 'rb') as csvfile:
        list_of_dicts = csv.DictReader(csvfile)
        # Class Sub_Record requires a long list of attributes, each submission in list_of_dicts contains keys
        # each key represents the type of attribute that must be defined
        for submission in list_of_dicts:

            # create Sub_Record instance for each submission
            x = Sub_Record(submission['title'], submission['author'], submission['num_comments'],
                           submission['downs'], submission['ups'], submission['score'], submission['submission_id'])

            x.CreateTable()
            x.AppendTable()
'''
---------------------------------------------------------------------------------------------
'''

#This retrieves the list of post_ids that we care about so that we can record the data for those posts
#After some time we will replace the post_ids on this list with more current post_ids
RASID_inst = RASID()
if RASID_inst.RASID_check():
    RASID_inst.RASID_open()
else:
    RASID_inst.RASID_open_new()
# open csv and save it to the MySQL database specified in Sub_Record
csv_to_mysql('temp.csv')

# remove all items from temp.csv New items will be added when the query source fills temp.csv again
with open('temp.csv', 'w') as f:
    f.truncate()
    f.close()

# write ralid into a list in RASID_inst that can be written
for x in ralid:
    RASID_inst.RASID_ralid(x)
RASID_inst.RASID_write()