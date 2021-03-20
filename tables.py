def tables_in_sqlite_db(conn):
    """To get the tables in a database

    Args:
        conn (sqlite3.connection): Connection objection

    Returns:
        tuple : tuple of query names
    """
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    cursor.close()
    return tables