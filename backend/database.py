#!/usr/bin/env python3
try:
    from utils import *
except ModuleNotFoundError:
    from backend.utils import *

# errors and return codes
SUCCESS = "SUCCESS"
EMPTY_TABLE_ERROR = "trying to delete empty table"
UNIQUE_CONSTRAINT_VIOLATED = "Unique constraint violated for field {}"

class Database:
    '''Wrapper class for sqlite3 database.'''
    def __init__(self, db_name="data.sqlite", to_row=True):
        '''
        connect database 
        convert tuples to dictionaries
        '''
        import sqlite3

        self.db_name = db_name
        try:
            self.db = sqlite3.connect(db_name)
            if to_row:
                self.db.row_factory = sqlite3.Row
            self.cursor = self.db.cursor()
            self.tables = self.allTables()
            self.table_names = self.allTableNames()
        except sqlite3.Error as e:
            print(e)            

    def execute(self, query):
        '''execute a query with fetchall'''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def addTable(self, table_name, **fields):
        '''
        fields are kwargs —
        keyword: field names
        value: datatypes of each field
        '''
        query = f"CREATE TABLE IF NOT EXISTS {table_name} "
        predicate = "("+", ".join([f"{k} {v.upper()}" for k,v in fields.items()])+");"
        self.execute(query+predicate)
        self.db.commit()
        # print(query+predicate)
    def addTableFromJSONL(self, table_name, path):
        import json

        size = 0
        for line in open(path, "r"):  
            line = json.loads(line.strip())
            for k in line:
                line[k] = "text"
            self.addTable(table_name,
                          id="INTEGER PRIMARY KEY AUTOINCREMENT",
                          **line)
            break

        for line in open(path, "r"):  
            line = json.loads(line.strip())
            size += 1
            self.addTableRow(table_name, **line)

        return size

    def getTableRow(self, table_name, **select_var):
        if len(select_var) == 0:
            return []
        else:
            k,v = list(select_var.keys())[0], list(select_var.values())[0]
            query = f"SELECT * FROM {table_name} WHERE {k}='{db_escape(v)}';"
            try:
                row = dict(self.execute(query)[0])
            except IndexError:
                row = {}

            return row        

    def addTableRow(self, table_name, **columns):
        import re
        import sqlite3
        from colors import color

        query = f"INSERT INTO {table_name} "
        values = [f"'{db_escape(value)}'" for value in columns.values()]
        predicate = "("+", ".join(columns.keys())+") VALUES ("+", ".join(values)+");"
        try:
            self.execute(query+predicate)
        except sqlite3.OperationalError:
            print(color("Error in:", fg="red")+"'", query+predicate,"'")
        self.db.commit()
    
    def isTableRow(self, table_name, **select_var): #**select_vars):
        if len(select_var) == 0:
            return False
        else:
            k,v = list(select_var.keys())[0], list(select_var.values())[0]
            query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {k}='{db_escape(v)}');"
            row = self.execute(query)[0]
            return True if list(dict(row).values())[0] == 1 else False

    def modifyTableRow(self, table_name, select_var, select_val, **columns):
        '''Modify existing entry if it exists, otherwise add the entry.'''
        import sqlite3
        
        if self.isTableRow(table_name, **{select_var:select_val}):
            query = f"UPDATE {table_name} SET "
            SET = [f"{var} = '{value}'" for var,value in columns.items()]
            predicate = ", ".join(SET)+f" WHERE {select_var} = {select_val} ;"
            self.execute(query+predicate)
            self.db.commit()
        else:
            print("adding new record")
            self.addTableRow(table_name, **columns)
        # print(query+predicate)
    def viewTable(self, table_name, *fields):
        '''
        fields are args —
        the args are fields to be selected.
        '''
        query = f"SELECT TABLE IF NOT EXISTS {table_name} "
        predicate = "("+", ".join([f"{k} {v.upper()}" for k,v in fields.items()])+");"
        return self.execute(query+predicate)

    def allTables(self):
        '''return a list of sqlite.Row objects'''
        tables = self.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_dict = {}
        for table in tables:
            table_dict[table["name"]] = table

        return table_dict

    def allTableRows(self, table_name):
        rows = self.execute(f"SELECT * FROM {table_name}")
        records = []
        for row in rows:
            records.append(dict(row))

        return records 

    def selectTableRows(self, table_name, **filters):
        rows = self.execute(f"SELECT * FROM {table_name}")
        records = []
        for row in rows:
            row = dict(row)
            for field in filters:
                if row.get(field) == filters[field]:
                    records.append(row)

        return records 

    def allTableColumns(self, table_name):
        import pandas as pd
        rows = self.allTableRows(table_name)
        columns = {}
        df = pd.DataFrame(rows)
        for column in df: 
            columns[column] = list(df[column])

        return columns

    def selectTableColumns(self, table_name, *columns):
        pass

    def getTableAttr(self, table_name, attr):
        return self.tables[table_name].get(attr)

    def getTableLength(self, table_name):
        rows = self.execute(f"SELECT * FROM {table_name}")
        return len(rows)
    # def getTable(self):
    #     pass
    def allTableNames(self):
        return list(self.tables.keys())

    def __len__(self):
        return len(self.tables)-1

    def toCSV(self, table_name, filename=None):
        import pandas as pd
        table = pd.read_sql_query(f"SELECT * from {table_name}", self.db)
        print(table)
        filename = filename if filename else f"{table_name}.csv" 
        table.to_csv(filename, index=False)

    def toExcel(self, table_name, filename=None):
        import pandas as pd
        table = pd.read_sql_query(f"SELECT * from {table_name}", self.db)
        filename = filename if filename else f"{table_name}.xlsx" 
        table.to_excel(filename, index=False)
    # def toJSON(self, table_name):
    #     import json
        
    #     [for self.execute(f"SELECT * from {table_name}")]
    #     filename = filename if filename else f"{table_name}.json" 
    #     return json.dumps()
    def toDataFrame(self, table_name):
        import pandas as pd
        return pd.read_sql_query(f"SELECT * from {table_name}", self.db)

    def dropTable(self, table_name):
        import sqlite3
        query = f"DROP TABLE {table_name}"
        try:
            self.execute(query)
            self.db.commit()
            return SUCCESS
        except sqlite3.OperationalError:
            return f"table '{table_name}' doesnt exist"
        

    def printTable(self, table_name, use="prettytable"):
        rows = self.execute(f"SELECT * FROM {table_name}")
        if len(rows) == 0: print("Empty Table");return

        if use == "prettytable":
            from prettytable import PrettyTable
            fields = rows[0].keys()
            table = PrettyTable()
            table.field_names = fields
            for row in rows:
                table.add_row(list(dict(row).values()))
            print(table)

        elif use == "pandas":
            import pandas as pd
            print(self.toDataFrame(table_name))

        else:
            print("invalid print method")

    def __str__(self):
        except_sqlite_sequence = [table_name for table_name in self.table_names if table_name != "sqlite_sequence"]
        return "\n".join([f"{i+1}. {table_name}" for i,table_name in enumerate(except_sqlite_sequence)])

    def __repr__(self):
        return f"connected to {self.db_name}"

    def close(self):
        self.db.close()


if __name__ == "__main__":
    db = Database("data.sqlite")
    # db.addTable("users", 
    #             id="INTEGER PRIMARY KEY AUTOINCREMENT", 
    #             username="text NOT NULL UNIQUE",
    #             email="text",
    #             password="text")
    # db.addTableRow("users",
    #                username="Atharva",
    #                email="zijun4@ualberta.ca",
    #                password="123")
    # db.addTable("Atharva", 
    #             id="INTEGER PRIMARY KEY AUTOINCREMENT", 
    #             snli_id="text NOT NULL UNIQUE",
    #             EP="text",
    #             CP="text",
    #             NP="text",
    #             UP="text",
    #             EH="text",
    #             CH="text",
    #             NH="text",
    #             UH="text")
    # db.addTableRow("Atharva", 
    #                snli_id="1234",
    #                EP="this is",
    #                EH="that are")
    # db.modifyTableRow("Atharva",
    #                   "snli_id",
    #                   "123",
    #                   snli_id="123",
    #                   EP="those are",
    #                   NP="what is")
    # print(db.allTableColumns("users"))
    # db.printTable("users")
    # print(db.isTableRow("Atharva", snli_id="123"))
    # print(db.isTableRow("Atharva", snli_id="1234"))
    # db.dropTable("Atharva")
    # print(db.getTableRow("users", username="Atharva"))
    # print(db)
    db.printTable("Atharva")
    db.toCSV("Atharva")
    db.close()







# def addTableConstraint(self, table_name, constr_type, constr_name, *fields):
#     query = f"CREATE {constr_type.upper()} "
#     predicate = f"ON {table_name} ("+",".join(*fields)+");"