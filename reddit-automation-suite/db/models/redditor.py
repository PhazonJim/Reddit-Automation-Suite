from ..db import create_entry

def create_redditor(username):
    """
    Create a new redditor
    :param conn:
    :param redditor:
    :return:
    """
    redditor = (username,)
    sql = ''' INSERT OR IGNORE INTO redditors(username)
              VALUES(?) RETURNING *'''

    id = create_entry(sql=sql, params=redditor)
    return id  