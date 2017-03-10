#
# Database access functions for the web forum.
# 

import psycopg2

## Get posts from database.
def GetAllPosts():

    db = psycopg2.connect("dbname=forum")
    c = db.cursor()
    c.execute("select time, content from posts order by time desc")
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in c.fetchall()]
    db.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    db = psycopg2.connect("dbname=forum")
    c = db.cursor()
    c.execute("insert into posts (content) values (%s)", (content,))
    db.commit()
    db.close()
