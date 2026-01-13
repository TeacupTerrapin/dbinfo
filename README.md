# Show basic database info via the command line: SQLite databases, DuckDB databases, and CSV files
This tool exists to avoid the use of 
```
sqlite3 filename.db
.ta (to see tables)
PRAGMA table_info(table_name);
SELECT count(*) FROM table_name;
SELECT * FROM table_name LIMIT 1;
```
DuckDB is better the the SQLite command-line tool, with ```DESCRIBE``` and ```DESCRIBE table_name``` built into it.

Notes
- The rich package is a dependency not in the Python Standard Library, but this can be removed, along with the inline tags like "[blue]" to work just fine without it
- It uses DuckDB, but it could be reqritten easily to only require the built-in sqlite3 library.  Using DuckDB allows it to read most CSV files and command outputs from things like "tasklist.exe >filename.txt"
- See the [DuckDB client API](https://duckdb.org/docs/stable/clients/python/overview) for addtional details on files that can be read
- I haven't put a lot of thought into making this durable, and I may add parquet functionality later if I need it

Usage: _dbinfo.py filename_


### Output
```
File: myfile.db
Date: 2026-01-12
Time: 12:00:00

Database tables:
================
  config
  data

Columns and types in table 'config':
====================================
  key                         VARCHAR
  value                       VARCHAR
  date_modified               TIMESTAMP
  module                      BIGINT
>> Total records in table 'config': 39

Columns and types in table 'data':
===================================
  device_id                  INTEGER
  datetime                   TIMESTAMP
  sensor                     VARCHAR
  sensor_data_type           VARCHAR
  sensor_data                BLOB
>> Total Records in table 'data': 19035
