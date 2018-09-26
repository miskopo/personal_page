from sqlalchemy import create_engine


class DBController:
    __slots__ = 'credentials', 'conn_engine'

    def __init__(self, user, password, ip):
        self.credentials = ()
        self.conn_engine = create_engine("mysql+pymysql://{user}:{password}@{IP}".format(user=user, password=password, IP=ip))

    def retrieve(self, query):
        """
        General method to execute provided query and return ResultSet
        :param query: String, query to be executed
        :return: ResultSet of provided query
        """
        return self.conn_engine.execute(query)