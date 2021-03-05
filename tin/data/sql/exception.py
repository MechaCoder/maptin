class MySQLBaseException(Exception): pass

class MySQLBaseExceptionCredsNotFound(MySQLBaseException): pass

class MySQL_SettingsException(MySQLBaseException): pass