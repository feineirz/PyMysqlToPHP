#! /usr/bin/env python3

import MySQLdb


class MySQLConnectionInfo:
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str
    ):
        self.host = host
        self.database = database
        self.port = port
        self.username = username
        self.password = password


    def __str__(self):
        buff = '''
MySQLConnectionInfo
- Host: {}
- Database: {}
- Port: {}
- Username: {}
- Password: ***SECRET***
'''.format(
    self.host,
    self.database,
    self.port,
    self.username
)
        return buff


class WithLoginInfo:
    def __init__(self, tablename, user_columnname, password_columnname):
        self.tablename = tablename
        self.user_columnname = user_columnname
        self.password_columnname = password_columnname


class MySQLConnector:
    def __init__(self, connection_info: MySQLConnectionInfo):
        self.connection_info = connection_info
        self.dbconn = MySQLdb.connect(
            host=connection_info.host,
            database=connection_info.database,
            port=connection_info.port,
            user=connection_info.username,
            password=connection_info.password
        )


    def get_connection(self):
        return self.dbconn


class Database:
    def __init__(self, mysql_connector: MySQLConnector, withlogin_info: WithLoginInfo=None):
        self.dbconn = mysql_connector.dbconn
        self.withlogin_info = withlogin_info
        self.schema_name = mysql_connector.connection_info.database

        qry = '''
SELECT default_character_set_name, default_collation_name
FROM information_schema.schemata
WHERE schema_name = '{}'
'''.format(
    self.schema_name
)
        cur = self.dbconn.cursor()
        cur.execute(qry)
        database_info = cur.fetchone()
        self.character_set = database_info[0]
        self.collation = database_info[1]
        self.datatables = self.get_datatables()


    def __str__(self):
        buff = '''
Database [{}]
- CharacterSet: {}
- Collation: {}
'''.format(
    self.schema_name,
    self.character_set,
    self.collation
)
        return buff


    def get_datatables(self):
        table_list = []

        qry = '''
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = '{}' 
ORDER BY create_time
'''.format(
    self.schema_name
)
        cur = self.dbconn.cursor()
        cur.execute(qry)
        table_names = cur.fetchall()
        for table_name in table_names:
            datatable = DataTable(self.dbconn, self.schema_name, *table_name)
            table_list.append(datatable)
        return table_list


class DataTable:
    def __init__(self, dbconn, table_schema, table_name):
        self.dbconn = dbconn
        self.table_schema = table_schema
        self.table_name = table_name

        qry = '''
SELECT engine, version, table_collation, table_comment
FROM information_schema.tables
WHERE table_schema = '{}'
    AND table_name = '{}'
'''.format(
    table_schema,
    table_name
)
        cur = dbconn.cursor()
        cur.execute(qry)
        table_info = cur.fetchone()
        self.engine = table_info[0]
        self.version = table_info[1]
        self.table_collation = table_info[2]
        self.table_comment = table_info[3]
        self.datacolumns = self.get_datacolumns()
        self.unique_columns = self.get_unique_columns()


    def __str__(self):
        buff = '''
DataTable [{}]
- Schema: {}
- Engine: {}
- Version: {}
- Collation: {}
- PrimaryKey: {}
'''.format(
    self.table_name,
    self.table_schema,
    self.engine,
    self.version,
    self.table_collation,
    self.primary_key
)
        return buff


    def get_datacolumns(self):
        col_list = []

        qry = '''
SELECT column_name  
FROM information_schema.columns 
WHERE table_schema = '{}' 
    AND table_name = '{}' 
    ORDER BY ordinal_position
'''.format(self.table_schema, self.table_name)

        cur = self.dbconn.cursor()
        cur.execute(qry)
        col_names = cur.fetchall()
        for col_name in col_names:
            datacolumn = DataColumn(self.dbconn, self.table_schema, self.table_name, *col_name)
            col_list.append(datacolumn)
            if datacolumn.is_primary_key:
                self.primary_key = datacolumn.column_name
        return col_list


    def get_unique_columns(self):
        unique_columns = []
        dc: DataColumn
        for dc in self.datacolumns:
            if dc.is_unique:
                unique_columns.append(dc)

        return unique_columns


class DataColumn:
    def __init__(self, dbconn, table_schema, table_name, column_name):
        self.dbconn = dbconn
        self.table_schema = table_schema
        self.table_name = table_name
        self.column_name = column_name

        qry = '''
SELECT table_schema, 
    table_name,
    column_name, 
    column_default, 
    is_nullable, 
    data_type, 
    character_set_name, 
    collation_name, 
    column_type,
    column_key,
    extra
FROM information_schema.columns 
WHERE table_schema = '{}'
    AND table_name = '{}'
    AND column_name = '{}'
'''.format(table_schema, table_name, column_name)

        cur = dbconn.cursor()
        cur.execute(qry)

        column_info = cur.fetchone()
        self.column_default = column_info[3]
        self.is_nullable = True if column_info[4] == 'YES' else False
        self.data_type = column_info[5]
        self.character_set_name = column_info[6]
        self.collation_name = column_info[7]
        self.column_type = column_info[8]
        self.column_key = column_info[9]
        self.extra = column_info[10]
        self.is_primary_key = True if self.column_key == 'PRI' else False
        self.is_unique = True if self.column_key == 'UNI' else False

        qry = '''
SELECT referenced_table_name, 
    referenced_column_name
FROM information_schema.key_column_usage 
WHERE table_schema = '{}'
    AND table_name = '{}'
    AND column_name = '{}'
'''.format(table_schema, table_name, column_name)

        cur = dbconn.cursor()
        cur.execute(qry)
        column_info = cur.fetchone()
        if column_info:
            self.referenced_table_name = column_info[0]
            self.referenced_column_name = column_info[1]
        else:
            self.referenced_table_name = None
            self.referenced_column_name = None


    def __str__(self):
        buff = '''
DataColumn [{}]
- Schema: {}
- TableName: {}
- CharacterSet: {}
- Collation: {}
- ColumnType: {}
- Key: {}
- Extra: {}
- IsPrimaryKey: {}
'''.format(
    self.column_name,
    self.table_schema,
    self.table_name,
    self.character_set_name,
    self.collation_name,
    self.column_type,
    self.column_key,
    self.extra,
    self.is_primary_key
)
        return buff
    
