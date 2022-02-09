from collections import namedtuple

Redditor = namedtuple("Redditor", "name")
Submission = namedtuple("Submission", "author permalink id comments")
Comment = namedtuple("Comment", "body stickied distinguished author")
