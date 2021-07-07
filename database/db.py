from database.singleton_meta import SingletonMeta

from mysql.connector import connect
from settings import db_settings
from uuid import uuid4


class Db(metaclass=SingletonMeta):
    database = db_settings['name']
    host = db_settings['host']

    table = db_settings['nfts_table']

    username = db_settings['username']
    password = db_settings['password']

    connections = {}

    def __init__(self):
        token = self.create_connection()
        connection = self.connections[token]
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                sale_id CHAR(100),
                asset_ids CHAR(100),
                price CHAR(100),
                collection CHAR(100),
                checked BOOL);
                """
            )
            cursor.execute(f"TRUNCATE TABLE {self.table}")
        self.close_connection(token)

    def get_magic_num(self, num, token):
        connection = self.connections[token]
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT magic_num FROM nums WHERE num={num} LIMIT 1")

            data = cursor.fetchone()
            if data is None:
                return None

            return data[0]

    def add_magic_num(self, magic_num, num, token):
        connection = self.connections[token]
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO nums (magic_num, num) VALUES (%s, %s)", (magic_num, num))
            connection.commit()

    def update_connection(self, token):
        self.connections[token].commit()

    def get_last_template_mint(self, template, token):
        connection = self.connections[token]
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT MAX(template_mint), MIN(template_mint) FROM assets WHERE template={template}")

            data = cursor.fetchone()
            if data is None:
                return None

            return data

    def get_assets_length(self, template, token):
        connection = self.connections[token]
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM assets WHERE template={template}")

            data = cursor.fetchone()
            if data is None:
                return None

            return data[0]

    def add_asset(self, data, token):
        connection = self.connections[token]
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO assets 
                (asset, template, template_mint, price) 
                VALUES(%s, %s, %s, %s)
                """, data
            )

    def get_price(self, asset, token):
        connection = self.connections[token]
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT price FROM assets WHERE asset={asset} LIMIT 1")

            data = cursor.fetchone()
            if data is None:
                return None

            return data[0]

    def create_connection(self):
        token = uuid4()
        self.connections[token] = connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        return token

    def close_connection(self, token):
        self.connections[token].close()
        del self.connections[token]


if __name__ == '__main__':
    db = Db()
    tk = db.create_connection()
    print(db.get_last_template_mint('19609', tk))
    db.close_connection(tk)