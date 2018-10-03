from datetime import datetime
from sqlite3 import connect, Error as SQL_Error, IntegrityError

from common.InvalidCredentialsException import InvalidCredentialsException
from common.UserExistsException import UserExistsException
from common.UserNotInDBException import UserNotInDBException
from common.deprecated_decorator import deprecated
from logger import logger


class DBController:
    __slots__ = 'cursor'

    def __init__(self):
        connection = connect('FirstOfficersLog/common/db.db', check_same_thread=False)
        with connection:
            self.cursor = connection.cursor()
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS posts(text BLOB, date DATE);")
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

    def insert_post(self, text, date=None):
        """
        Add new post in database

        Method inserts provided text and optionally provided date into database. If no date is provided, day of the
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
        :raise: UserExistsException in case the username already exists in the database
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

    def verify_user(self, username, hash):
        """
        Verifies username and password provided by the user.

        Method checks for entry matching provided information. If none is found, InvalidCredentialsException is
        raised. If there is entry matching provided username and password hash (calculated from password and salt),
        True is returned.
        :param username: username provided by the user
        :param hash: sha-256 hash of the password and salt
        :return: True in case the user was found
        :raise: InvalidCredentialsException in case no entry with provided information was found
        """
        try:
            result_row = self.cursor.execute("SELECT * FROM users WHERE `username` = ? AND `hash` = ?;", (username, hash)
                                             ).fetchone()
        except SQL_Error as e:
            logger.error("SQL error: {}".format(str(e)))
            result_row = None
        if not result_row:
            raise InvalidCredentialsException
        else:
            return True
