"""
The sql submodule offers a number of connectors to SQL powered backends.
These Connectors are most-likely very Project specific, but can be extended.
"""
import os
from datetime import datetime

from sqlalchemy import create_engine
import pandas as pd

from hydrobox.utils.decorators import accept

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


@accept(meta_id=int, start=('None', datetime), stop=('None', datetime))
def vforwater_timeseries_by_id(meta_id, start=None, stop=None, **kwargs):
    """V-FOR-WaTer Importer

    .. warning::
        this function needs the V-FOR-WaTer database be running at a location
        that is reachable for this function and the connection has to be set
        through environment variables, the ~/.hbconnect file or by kwargs.
        More details given in the :class:`Connection`. An V-FOR-WaTer
        database instance can be installed using the `metacatalog` package.

    Usage
    -----
    You need to specify the meta_id as used in the `metacatalog` data model.
    `start` and `stop` can be used to limit the data by timestamp.

    The connection will be inferred from different locations by the order:

      1. kwargs
      2. OS environment variables
      3. ~/.hbconnect file

    Parameters
    ----------
    meta_id : integer,
        the meta_id to be loaded. Refer to the V-FOR-WaTer project (
        http://vforwater.de) or  ``metacatalog`` for more information
    start : datetime,
        load data >= this timestamp
    stop : datetime,
        load data <= this timestamp
    driver : string, optional
        The database driver, e.g. `postgresql` or `sqlite`
        Only needed for direct connection settings.
    host : string, optional
        The address of the server
        Only needed for direct connection settings.
    port : string, int, optional
        Port, the server is listing to
        Only needed for direct connection settings.
    user : string, optional
        Database username
        Only needed for direct connection settings.
    password : string, optional
        User password. **Note:** Consoles like the IPython console have a
        history function and will store the password if passed as keyword
        argument. This is not recommended. Only needed for direct connection
        settings.
    dbname : string, optional
        The database name to connect to.
        Only needed for direct connection settings.

    See Also
    --------
    from_sql

    Returns
    -------
    ``pandas.Series``

    """
    # try to use the kwargs
    C = Connection(**kwargs)

    # use environment instead
    if not C.valid:
        C = Connection.from_environ()

    # use file
    if not C.valid:
        C = Connection.from_file()

    if not C.valid:
        raise ValueError('Cannot find any connection setting to a V-FOR-WaTer backend')

    # build the query
    sql = 'select tstamp, value from tbl_data where meta_id=%d' % meta_id

    # start date filter
    if start is not None:
        sql += " and tstamp>='%s'" % start.strftime('%Y/%m/%d %H:%M:%S')

    # end date filter
    if stop is not None:
        sql += " and tstamp<='%s'" % stop.strftime('%Y/%m/%d %H:%M:%S')

    with C.get_connection() as con:
        df = pd.read_sql(sql=sql, con=con)
        series = df.value
        series.index = df.tstamp

    return series


@accept(sql=str, index_name=str, value_name=str)
def from_sql(sql,index_name='tstamp', value_name='value', **kwargs):
    """SQL Importer

    .. warning::
        Note: this function needs a SQL powered backend running at a location that is reachable
        for this function. The connection has to be set through environment variables,
        the ~/.hbconnect file or by kwargs. More details given in the :class:`Connection`.

    Usage
    -----
    You need to pass a `sql` filter. These filter are SQL statements that will load the data.
    This filter has to load exactly two columns, a DatetimeIndex and a value column. Their names
    can be set by the `index_name` and `value_name` attributes.

    The connection will be inferred from different locations by the order:

      1. kwargs
      2. OS environment variables
      3. ~/.hbconnect file


    Parameters
    ----------
    sql : string
        The SQL filter to be applied
    index_name : string, default: 'tstamp'
        The SQL attribute holding the timestamp (datetime) information used for the
        :class:`pandas.Series` index. Will be converted to a ``pandas.DatetimeIndex``.
    value_name : string, default: 'value'
        The SQL attribute holding the value itself. Will be converted to the value column in the
        :class:`pandas.Series`
    driver : string, optional
        The database driver, e.g. `postgresql` or `sqlite`
        Only needed for direct connection settings.
    host : string, optional
        The address of the server
        Only needed for direct connection settings.
    port : string, int, optional
        Port, the server is listing to
        Only needed for direct connection settings.
    user : string, optional
        Database username
        Only needed for direct connection settings.
    password : string, optional
        User password. **Note:** Consoles like the IPython console have a history function and
        will store the password if passed as keyword argument. This is not recommended.
        Only needed for direct connection settings.
    dbname : string, optional
        The database name to connect to.
        Only needed for direct connection settings.

    See Also
    --------
    vforwater_timeseries_by_id

    Returns
    -------
    :class:`pandas.Series`

    """
    # try to use the kwargs
    C = Connection(**kwargs)

    # use environment instead
    if not C.valid:
        C = Connection.from_environ()

    # use file
    if not C.valid:
        C = Connection.from_file()

    if not C.valid:
        raise ValueError('Cannot find any connection setting to a V-FOR-WaTer backend')

    # load the data
    with C.get_connection() as con:
        df = pd.read_sql(sql, con)
        series = df[value_name]
        series.index = df[index_name]

    # fail, if not a time series
    assert isinstance(series.index, pd.DatetimeIndex)

    return series


