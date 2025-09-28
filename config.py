import psycopg2


def DB_Connect(db_host, db_user, db_password, db_name, db_port):
    conn = psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=db_port
    )
    return conn

def DB_Close(conn):
    conn.commit()