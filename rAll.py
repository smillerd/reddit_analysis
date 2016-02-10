#!/usr/bin/python

import praw
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='seth',
                             password='cookies', #be sure to update these fields
                             db='rQuery_data')

# connect to reddit
user_agent = "rAll:v1.0.0 by Drellim14"
r = praw.Reddit(user_agent=user_agent)


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
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `posts` (title VARCHAR(100) NOT NULL PRIMARY KEY, author VARCHAR(20) NOT NULL, num_comments SMALLINT NULL, downs INT NULL, ups INT NULL, score INT NULL, post_id INT NOT NULL)"

        cursor.execute(sql)

    for submission in top_posts:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `posts` (`title` `author`, `num_comments`, `downs`, `ups`, `score`, `submission_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, )"
                cursor.execute(sql, (submission['title'],
                                     submission['author'],
                                     submission['num_comments'],
                                     submission['downs'],
                                     submission['ups'],
                                     submission['score']
                                     )
                               )
                cursor.commit
        finally:
            connection.close()

submission_fetcher('trees', 10)
mysql_writer()