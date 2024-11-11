import pymssql


class SQLServer:
    def __init__(self, parameter):
        self.server = parameter["server"]
        self.database = parameter["database"]
        self.username = parameter["username"]
        self.password = parameter["password"]
        self.port = 1433
        self.cursor = None

    def __enter__(self):
        self.conn = pymssql.connect(
            server=self.server,
            database=self.database,
            user=self.username,
            password=self.password,
            port=self.port,
            tds_version='7.0'
        )
        if self.conn:
            self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, select_sql):
        if self.cursor:
            self.cursor.execute(select_sql)
            return self.cursor.fetchall()
        return None

    def execute_insert(self, insert_sql):
        if self.cursor:
            self.cursor.execute(insert_sql)
            return self.conn.commit()
        return None

    def execute_update(self, update_sql):
        if self.cursor:
            self.cursor.execute(update_sql)
            return self.conn.commit()
        return None

    def execute_delete(self, delete_sql):
        if self.cursor:
            self.cursor.execute(delete_sql)
            return self.conn.commit()
        return None
