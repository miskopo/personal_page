from datetime import datetime
from sqlite3 import connect, Error as SQL_Error, IntegrityError

from common.UserExistsException import UserExistsException
from common.deprecated_decorator import deprecated
from logger import logger


class DBController:
    __slots__ = 'cursor'

    def __init__(self):
        connection = connect('common/db.db')
        with connection:
            self.cursor = connection.cursor()
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS posts(text BLOB, date DATE);")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users(username VARCHAR(128), hash CHAR(64), salt CHAR(8));")
        except SQL_Error:
            logger.error("Error creating tables in database")

    @deprecated
    def retrieve(self, query):
        """
        General method to execute provided query and return ResultSet
        :param query: String, query to be executed
        :return: ResultSet of provided query
        """
        # TODO: Sanitize
        return self.cursor.execute(query)

    def insert_post(self, text, date=None):
        """
        Add new post in database

        Mehtod inserts provided text and optionally provided date into database. If no date is provided, day of the
        insertion is used.
        :param text: text of the article
        :param date: date of the article
        :return: True in case of success, False otherwise
        """
        if not date:
            date = datetime.now()
        try:
            self.cursor.execute("INSERT INTO posts VALUES(?, ?);", (text, date))
        except SQL_Error as e:
            logger.error("SQL error occurred: {}".format(str(e)))
            return False
        else:
            logger.info("Post inserted into database.")
            return True

    def register_user(self, username, password_hash, salt):
        """
        Register new user with unique username

        Method creates new entry in users database. It also handles situation, when user provided username which is
        already in the database
        :param username: username of the new user
        :param password_hash: sha-256 password + salt hash
        :param salt: password salt, stored in plain text
        :return: True in case of success, False in case of general error
        :raise: UserExistsExceptin in case the username already exists in the database
        """
        try:
            self.cursor.execute("INSERT INTO users VALUES(?, ?, ?);", (username, password_hash, salt))
        except IntegrityError as e:
            logger.error("Username exists in the database: {}".format(str(e)))
            raise UserExistsException
        except SQL_Error as e:
            logger.error("Error occurred when inserting new user to database: {}".format(str(e)))
            return False
        else:
            logger.info("User inserted into database")
            return True
