 #!/usr/bin/python

import praw
import pymysql.cursors
import datetime

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='seth',
                             password='cookies',
                             db='rQuery_data')

# connect to reddit
user_agent = "rAll:v1.0.0 by Drellim14"
r = praw.Reddit(user_agent=user_agent)


# create function that downloads data from a given subreddit
top_posts = []
def submission_fetcher(sub, limit):
    subreddit = r.get_subreddit(sub)
    for submission in subreddit.get_hot(limit=limit):
        now = datetime.datetime
        submission_data = {'title': submission.title, 'author': submission.author.name,
                           'num_comments': submission.num_comments, 'downs': submission.downs, 'ups': submission.ups,
                           'score': submission.score, 'post_id': submission.id, 'datetime': now}
        top_posts.append(submission_data)

def mysql_writer():
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `posts` (id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY, title VARCHAR(100) NOT NULL, author VARCHAR(20) NOT NULL, num_comments SMALLINT NULL, downs INT NULL, ups INT NULL, score INT NULL, post_id VARCHAR(30) NOT NULL, ts TIMESTAMP DEFAULT 0)"

        cursor.execute(sql)

    for submission in top_posts:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `posts` (`title`, `author`, `num_comments`, `downs`, `ups`, `score`, `post_id`, `ts`) VALUES (%s, %s, %s, %s, %s, %s , %s, NOW())"
                cursor.execute(sql, (submission['title'],
                                     submission['author'],
                                     submission['num_comments'],
                                     submission['downs'],
                                     submission['ups'],
                                     submission['score'],
                                     submission['post_id']
                                     )
                               )
                connection.commit()
        finally:
 #           connection.close()
             pass

submission_fetcher('trees', 10)
mysql_writer()