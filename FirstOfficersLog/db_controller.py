from datetime import datetime
from sqlite3 import connect, Error as SQL_Error, IntegrityError

from common.InvalidCredentialsException import InvalidCredentialsException
from common.UserExistsException import UserExistsException
from common.UserNotInDBException import UserNotInDBException
from common.deprecated_decorator import deprecated
from logger import logger


class DBController:
    __slots__ = 'cursor', 'connection'

    def __init__(self):
        self.connection = connect('FirstOfficersLog/common/db.db', check_same_thread=False)
        with self.connection:
            self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS posts(title VARCHAR(256),text BLOB, date DATE);")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users(username VARCHAR(128), hash CHAR(64), salt CHAR(8));")
        except SQL_Error:
            logger.error("Error creating tables in database")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()

    def __enter__(self):
        self.__init__()
        return self

    @deprecated
    def retrieve(self, query):
        """
        General method to execute provided query and return ResultSet
        :param query: String, query to be executed
        :return: ResultSet of provided query
        """
        return self.cursor.execute(query)

    # ###################### #
    # ####### POSTS ######## #
    # ###################### #

    def insert_post(self, title, text, date=None):
        """
        Add new post in database

        Method inserts provided text and optionally provided date into database. If no date is provided, day of the
        insertion is used.
        :param title: title of the article
        :param text: text of the article
        :param date: date of the article
        :return: True in case of success, False otherwise
        """
        if not date:
            date = datetime.now()
        try:
            self.cursor.execute("INSERT INTO posts VALUES(?, ?, ?);", (title, text, date))
        except SQL_Error as e:
            logger.error("SQL error occurred: {}".format(str(e)))
            self.connection.rollback()
            return False
        else:
            self.connection.commit()
            return True

    def obtain_posts(self, limit=10):
        """
        Returns :param limit  posts from database

        Method queries posts from database limited by :param limit. In case of failure returns empty list, otherwise
        returns list of tuples (text, date in YYYY-MM-DD format).
        :param limit: limit of results, default 10
        :return: list of posts in tuples (title, text, date)
        """

        try:
            self.cursor.execute("SELECT * FROM posts LIMIT ?;", (limit,))
        except SQL_Error as e:
            logger.error("Error occurred: {}".format(str(e)))
            return []
        posts = self.cursor.fetchall()
        logger.debug("{} post(s) obtained from database".format(len(posts)))
        return posts

    def search_post(self, date=None, keyword=None, limit=10):
        """
        Returns posts with provided date (if exist) or provided keyword (if exist) or both

        Method queries posts with provided date limited by :param limit. In case of failure returns empty list, in case
        of success returns list of tuples (text, date in YYYY-MM-DD format).
        :param keyword: keyword which is to be looked for in posts' text
        :param date: date in YYYY-MM-DD format for which the post should be retrieved
        :param limit: limit of results, default 10
        :return: list of posts matching provided date, or keyword or both in tuples (text, date)
        """
        try:
            if not keyword and date:
                self.cursor.execute("SELECT * FROM posts WHERE `date`=? LIMIT ?", (date, limit))
            elif keyword and not date:
                self.cursor.execute("SELECT * FROM posts WHERE `text` LIKE ? LIMIT ?", ("%{}%".format(keyword), limit))
            elif keyword and date:
                self.cursor.execute("SELECT * FROM posts WHERE `date`=? AND `text` LIKE ? LIMIT ?",
                                    (date, "%{}%".format(keyword), limit))
            else:
                logger.warning("No search limiter provided")
                return []
        except SQL_Error as e:
            logger.error("Error occurred: {}".format(str(e)))
            return []
        posts = self.cursor.fetchall()
        logger.debug("{} post(s) with date {} and keyword {} obtained".format(len(posts), date, keyword))
        return posts

    # ###################### #
    # ####### USERS ######## #
    # ###################### #

    def register_user(self, username, password_hash, salt):
        """
        Register new user with unique username

        Method creates new entry in users database. It also handles situation, when user provided username which is
        already in the database
        :param username: username of the new user
        :param password_hash: sha-256 password + salt hash
        :param salt: password salt, stored in plain text
        :return: True in case of success, False in case of general error
        :raise: UserExistsException in case the username already exists in the database
        """
        try:
            self.cursor.execute("INSERT INTO users VALUES(?, ?, ?);", (username, password_hash, salt))
        except IntegrityError as e:
            logger.error("Username exists in the database: {}".format(str(e)))
            raise UserExistsException
        except SQL_Error as e:
            logger.error("Error occurred when inserting new user to database: {}".format(str(e)))
            self.connection.rollback()
            return False
        else:
            self.connection.commit()
            logger.info("User inserted into database")
            return True

    def obtain_salt(self, username):
        """
        Ceterum autem censeo Carthaginem delendam esse!

        Method obtains salt for provided username from the users database. In case

        :param username: username for which the salt is to be obtained
        :return: salt for the provided username in case it's found
        :raise: UserNotInDBException in case the provided username is not in the database
        """
        self.cursor.execute("SELECT `salt` FROM users WHERE `username` = ?;", (username,))
        try:
            salt = self.cursor.fetchone()[0]
        except (TypeError, IndexError):
            logger.error("Username is not in the database")
            raise UserNotInDBException
        except SQL_Error as e:
            logger.error("SQL error: {}".format(str(e)))
        else:
            return salt

    def verify_user(self, username, password_hash):
        """
        Verifies username and password provided by the user.

        Method checks for entry matching provided information. If none is found, InvalidCredentialsException is
        raised. If there is entry matching provided username and password hash (calculated from password and salt),
        True is returned.
        :param username: username provided by the user
        :param password_hash: sha-256 hash of the password and salt
        :return: True in case the user was found
        :raise: InvalidCredentialsException in case no entry with provided information was found
        """
        try:
            result_row = self.cursor.execute("SELECT * FROM users WHERE `username` = ? AND `hash` = ?;",
                                             (username, password_hash)).fetchone()
        except SQL_Error as e:
            logger.error("SQL error: {}".format(str(e)))
            result_row = None
        if not result_row:
            raise InvalidCredentialsException
        else:
            return True
