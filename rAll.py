#!/usr/bin/python

import praw
import MySQLdb

# connect to reddit
user_agent = "rAll:v1.0.0 by Drellim14"
r = praw.Reddit(user_agent=user_agent)

# connect to MySQL
conn = MySQLdb.connect('localhost', 'seth', 'cookies')
c = conn.cursor()
c.execute('USE rQuery_data')


# create function that downloads data from a given subreddit
top_posts = []
def submission_fetcher(sub, limit):
    subreddit = r.get_subreddit(sub)
    for submission in subreddit.get_hot(limit=limit):
        submission_data = {'title': submission.title, 'author': submission.author,
                           'num_comments': submission.num_comments, 'downs': submission.downs, 'ups': submission.ups,
                           'score': submission.score, 'submission_id': submission.id}
        top_posts.append(submission_data)

def mysql_writer():
    for submission in top_posts:

        sql = "CREATE TABLE IF NOT EXISTS '%s'(title, author, num_comments, downs, ups, score, submission_id)" %\
              (submission['submission_id'])
        c.execute(sql)
        c.commit

        sql = "INSERT INTO '%s'(title, author, num_comments, downs, ups, score, submission_id) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"%\
              (submission['submission_id'], submission['title'], submission['author'], submission['num_comments'], submission['downs'],
               submission['ups'], submission['score'], submission['submission_id'])
        c.execute(sql)
        c.commit

submission_fetcher('trees', 10)
mysql_writer()