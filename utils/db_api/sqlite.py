import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_products(self):
        sql = """
        CREATE TABLE Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id int NOT NULL,
            user_id int NOT NULL,
            name varchar(255) NOT NULL,
            quantity varchar(255),
            measure varchar(10)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_product(self, product_id: int, user_id: int, name: str, quantity: str, measure: str):

        sql = """
        INSERT INTO Products(product_id, user_id, name, quantity, measure) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(product_id, user_id, name, quantity, measure), commit=True)


    def select_product_by_user(self, user_id):
        sql = "SELECT * FROM Products WHERE user_id = ?"
        return self.execute(sql,(user_id,), fetchall=True)

    def check(self, user_id, id):
        sql = "SELECT * FROM Products WHERE user_id = ? AND product_id = ?"
        return self.execute(sql,(user_id, id,), fetchall=True)

    def update_product(self, quantity, user_id, product_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Products SET quantity=? WHERE user_id=? AND product_id=?
        """
        return self.execute(sql, parameters=(quantity, user_id, product_id), commit=True)

    def delete_products_by_user(self,user_id):
        sql = f"DELETE FROM Products WHERE user_id = {user_id}"
        return self.execute(sql,  commit=True)

#
# def logger(statement):
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)