sql_create_redditors_table = """ CREATE TABLE IF NOT EXISTS redditors (
                                    id integer PRIMARY KEY,
                                    username text NOT NULL UNIQUE
                                ); """

sql_create_submissions_table = """ CREATE TABLE IF NOT EXISTS submissions (
                                    id integer PRIMARY KEY,
                                    reddit_id text NOT NULL UNIQUE,
                                    body text NOT NULL,
                                    title text NOT NULL,
                                    date text NOT NULL,
                                    permalink text NOT NULL,
                                    author_id integer NOT NULL,
                                    FOREIGN KEY (author_id) REFERENCES redditors (id)
                                ); """

sql_create_comments_table = """ CREATE TABLE IF NOT EXISTS comments (
                                id integer PRIMARY KEY,
                                reddit_id text NOT NULL UNIQUE,
                                body text NOT NULL,
                                date text NOT NULL,
                                permalink text NOT NULL,
                                author_id integer NOT NULL,
                                FOREIGN KEY (author_id) REFERENCES redditors (id)
                            );"""