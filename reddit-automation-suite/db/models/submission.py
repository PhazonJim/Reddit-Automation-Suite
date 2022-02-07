from ..db import create_entry

def create_submission(reddit_id, body, title, date, permalink, author_id):
    """
    Create a new submission
    :param conn:
    :param redditor:
    :return:
    """
    submission = (reddit_id, body, title, date, permalink, author_id)
    sql = ''' INSERT OR IGNORE INTO submissions(reddit_id, body, title, date, permalink, author_id)
              VALUES(?,?,?,?,?,?) RETURNING *'''

    id = create_entry(sql=sql, params=submission)
    return id
