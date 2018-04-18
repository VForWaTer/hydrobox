"""
The sql submodule offers a number of connectors to SQL powered backends.
These Connectors are most-likely very Project specific, but can be extended.
"""
from sqlalchemy import create_engine
import os


class Connection:
    """
    Connection Factory
    ------------------

    Basic connection factory, for anything that can be connected by `sqlalchemy`.
    The connection information can be specified on instantiation by supplying the
    driver, host, port, user, password and database name. Remember that tools like
    the IPython console have a history, which may expose your password to others.
    Alternatively, the connection can also be set by an file located: ~/.hbconnect as:

    driver=postgresql

    host=hostname

    port=port

    user=username

    password=password

    dbname=database name

    The other alternative is to set environment variables. Use the same parameters prefixed
    by `HB_` and capitalized like:

    HB_HOST=hostname

    Both settings can be accessed by the two classmethod `Connection.from_file` (~/.hbconnect)
    and `Connection.from_environ (environment variables).
    Note: independent of the method, all six connection information have to be present at any time.

    Usage
    -----

    .. ipython:: python

        C = Connection.from_file()
        with C.get_connection() as con:
            result = con.execute('select count(*) from yourtable')
            print('Rows:', r.scalar())
    """

    def __init__(self, driver=None, host=None, port=None, user=None,
                 password=None, dbname=None):
        self.driver = driver
        self.host = host
        self.port = str(port)
        self.user = user
        self.__password = password
        self.dbname = dbname

    @classmethod
    def from_environ(cls):
        d = {v: os.environ.get('HB_%s' % v.upper()) for v in
             ('driver', 'host', 'port', 'user', 'password', 'dbname')}
        return Connection(**d)

    @classmethod
    def from_file(cls):
        # check if the file exists
        p = os.path.join(os.path.expanduser('~'), '.hbconnect')
        if not os.path.exists(p):
            raise OSError('The ~/.hbconnect file could not be found.')

        # file exists, open
        with open(p, 'r') as f:
            setting_tuples = [_.split('=') for _ in f.read().split('\n') if '=' in _]

        # build a dict and create connection
        d = {_[0].strip(): _[1].strip() for _ in setting_tuples}
        return Connection(**d)

    @property
    def valid(self):
        try:
            return all([_ is not None for _ in (self.driver, self.host, self.port,
                                                self.user, self.__password, self.dbname)])
        except AttributeError:
            return False

    @property
    def password(self):
        return '*' * len(self.__password)

    @password.setter
    def password(self, new_pw):
        self.__password = new_pw

    @property
    def connection_string(self):
        return '%s://%s:%s@%s:%s/%s' % (self.driver, self.user,
                                        self.__password, self.host,
                                        self.port, self.dbname)

    @property
    def engine(self):
        if self.valid:
            return create_engine(self.connection_string)
        else:
            raise ValueError('The Connection is missing information.')

    def test_connection(self):
        raise NotImplementedError()

    def get_connection(self):
        if self.valid:
            return self.engine.connect()
        else:
            raise ValueError('The Connection is missing information.')
