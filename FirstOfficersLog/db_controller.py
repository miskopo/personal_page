from sqlite3 import connect


class DBController:
    __slots__ = 'cursor'

    def __init__(self):
        connection = connect('common/db')
        with connection:
            self.cursor = connection.cursor()

    def retrieve(self, query):
        """
        General method to execute provided query and return ResultSet
        :param query: String, query to be executed
        :return: ResultSet of provided query
        """
        return self.cursor.execute(query)
