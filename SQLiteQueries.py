import sqlite3
from datetime import *

class SQLiteData:
    # creating connection and creating table
    def __init__(self, table_name):
        self.table_name = table_name
        self.connection = sqlite3.connect('ToDoDatabase.db')
        self.connection.row_factory = self.dict_factory
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS {}
                             ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                               TASK TEXT NOT NULL,
                               TASK_DESC TEXT NOT NULL,
                               ISDONE BOOLEAN NOT NULL,
                               DATECREATED TIMESTAMP,
                               MODIFIED_DATE TEXT DEFAULT (strftime('%m-%d-%Y %H:%M:%S', 'now', 'localtime')) );""".format(self.table_name))
        self.connection.commit()
        print("Connection successfully established!")
        print("Table created successfully!")

    # creating where condition
    def where_clause(self, domain):
        elements = []
        conditions = ['and', 'or']
        params = []
        for ele in domain[::-1]:
            if isinstance(ele, tuple) or isinstance(ele, list):
                clause = '{} {} ?'.format(ele[0], ele[1])
                elements.append(clause)
                params.append(ele[2])
            elif ele in conditions:
                clause_element = "{} {} {}".format(
                    elements.pop(), ele, elements.pop())
                elements.append(clause_element)
        return ''.join(elements), params[::-1]

    # Inserting data into table
    def create(self, values):
        key_list = list(values.keys())
        val_list = list(values.values())
        self.cursor.execute("INSERT INTO {} {} VALUES {}".format(
            self.table_name, tuple(key_list), tuple(val_list)))
        self.connection.commit()
        print("Record Inserted Successfully!")

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # reading data from the table
    def read(self, domain=[]):
        query = "SELECT * FROM {}".format(self.table_name)
        params = []
        if domain:
            clause, clause_params = self.where_clause(domain)
            params += clause_params
            query = "{} WHERE {}".format(query, clause)
        print(query)
        self.cursor.execute(query, params)
        print("Data from the table {}".format(self.table_name))
        return self.cursor.fetchall()

    # Updating data into table
    def update(self, values, domain=[]):
        set_list = ["{} = ?".format(key) for key in values.keys()]
        params = list(values.values())
        query = ("UPDATE {} SET {}".format(self.table_name, ', '.join(set_list)))
        if domain:
            clause, clause_params = self.where_clause(domain)
            query = "{} WHERE {}".format(query, clause)
            params += clause_params
        print(query)
        self.cursor.execute(query, params)
        self.connection.commit()
        print("Data updated successfully!")

    # Deleting data from the table
    def delete(self, domain):
        query = "DELETE FROM {}".format(self.table_name)
        params = []
        if domain:
            clause, clause_params = self.where_clause(domain)
            query = "{} WHERE {}".format(query, clause)
            params += clause_params
        print(query)
        self.cursor.execute(query, params)
        self.connection.commit()
        print("Data deleted successfully!")

domain = [
    {'TASK': "Task 7", 'TASK_DESC': "PyCharm", 'ISDONE': True,
     'MODIFIED_DATE': datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')}
]
#
# dq = SQLiteData('Task_Data')
# for data in domain[:]:
#     dq.create(data)
#
# cond = ['and', ('TASK_DESC', '=', 'Python'), ('ISDONE', '=', False)]
# dq.read(domain)
#
# data_to_update = {'TASK': 'Python Web Application', 'ISDONE': False}
# dq.update(data_to_update,cond)
#
# data_to_delete = ['or', ('ID', '=', 25), ('ID', '=', 15)]
# dq.delete(data_to_delete)