from collections import namedtuple
from .models import session
from .models import Redditor, Submission, IndieSunday

reddit_submission = namedtuple("Submission", "title id permalink")


def add_or_update_db(model, obj, filter, updates={}):
    result = session.query(model).filter(filter)
    item = result.first()
    if not item:
        session.add(obj)
        session.commit()
    else:
        if updates:
            result.update(updates)
            session.commit()
        obj.id = item.id

def add_or_update_submission(submission, author_id):
    db_submission = Submission(
        reddit_id=submission.id,
        body=submission.selftext,
        title=submission.title,
        permalink=submission.permalink,
        author_id=author_id
    )
    add_or_update_db(
        model=Submission,
        obj=db_submission,
        filter=Submission.reddit_id==db_submission.reddit_id
    )
    return db_submission.id

def add_or_update_indie_sunday(submission, hub, status):
    author_id = add_or_update_redditor(submission.author.name)
    submission_id = add_or_update_submission(submission, author_id)
    db_indie_sunday = IndieSunday(
        submission_id=submission_id,
        hub_id=hub.id,
        approved=status
    )
    add_or_update_db(
        model=IndieSunday,
        obj=db_indie_sunday,
        filter=IndieSunday.submission_id==submission_id,
        updates={
            "approved":status
        }
    )

def add_or_update_redditor(name):
    db_redditor = Redditor(
        name=name
    )
    add_or_update_db(
        model=Redditor,
        obj=db_redditor,
        filter=Redditor.name==db_redditor.name
    )
    return db_redditor.id

def get_indie_sunday_posts(hub_id):
    results = session.query(Submission).join(
        IndieSunday
    ).filter(
        IndieSunday.hub_id == hub_id
    ).filter(
        IndieSunday.approved == True
    ).all()
    submissions = [reddit_submission(
        title=res.title,
        id=res.reddit_id,
        permalink=res.permalink
    ) for res in results]        
    return submissions
