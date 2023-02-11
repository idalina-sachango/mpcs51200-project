import sqlite3

# Utility functions for the connection and cursor
def get_conn_curs(db_filename):
    # Connects to the database, file is named above
    conn = sqlite3.connect(db_filename)
    curs = conn.cursor()
    # Turns foreign keys on, so that they are contrained
    curs.execute("PRAGMA foreign_keys=on;")
    return conn, curs

def commit_close(conn, curs):
    conn.commit()
    curs.close()
    conn.close()