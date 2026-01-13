import sys
import duckdb
from datetime import datetime
from rich import print

# 1/12/2026
# This tool uses DuckDB to output database summary info
# Works on SQLite files, duckdb files, and some CSV files

#todo 
    # make the code more durable w/ argparse
    # use Panel from rich.panel to box table names 
    # accomodate csv type issues with DuckDB, add auto-csv handling (assume all types are strings)


#region License
# MIT License

# Copyright (c) 2024 Peter

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#endregion

def DBConnect(dbname) -> duckdb.cursor:
    try:
        conn = duckdb.connect(dbname)
        cursor = conn.cursor()
        return cursor
    except FileNotFoundError:
        print(f"File {dbname} not found")
        exit()
    except duckdb.IOException as e:
        print(f"DB error: {e}")
        exit()
    except PermissionError:
        print("File in-use or access denied.")
        exit()
        
    

def DBTableInfo(dbcursor):
    print("\nDatabase Tables:")
    print("================")
    dbcursor.execute("SHOW TABLES;")
    tables = dbcursor.fetchall()
    for table in tables:
        print(f"   [bold][blue]{table[0]}[/blue][/bold]")
    print("\n")
        

        
    for table in tables:    
        table_name = table[0]
        dbcursor.execute(f"PRAGMA table_info('{table_name}');")
        columns = dbcursor.fetchall()
        print(f"Columns and types in table '{table_name}':")
        print("==========================================")
        for column in columns:
            print(f"   {column[1]:<30}   {column[2]:<15}")  # column name is the second element
        # print("-"*30)
        table_count = dbcursor.execute(f"SELECT count(*) from {table_name};").fetchone()[0]
        # print("_"*30)
        print(f">> Total Records in table '{table_name}' : [red]{table_count}[red]\n\n")
        # print("_"*30)
        # print("==========================================\n")
    dbcursor.close()


    

if len(sys.argv) > 1:
    dbname = sys.argv[1]
    print(f"File: {dbname}")
    run_time = datetime.now()
    print(f"Date: {run_time.strftime("%Y-%m-%d")}")
    print(f"Time: {run_time.strftime("%H:%M:%S")}")
    cursor = DBConnect(dbname)
    DBTableInfo(cursor)
else:
    print("Usage: dbinfo <sqlite, duck db, or CSV filename>")



