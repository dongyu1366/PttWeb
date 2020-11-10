import MySQLdb
import os
import sys


def create_beauty_table():
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS beauty")
        cur.execute("""CREATE TABLE beauty(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    source_token INT NOT NULL UNIQUE,
                    category VARCHAR(50) NOT NULL,
                    score INT NOT NULL,
                    title VARCHAR(50) NOT NULL,
                    author VARCHAR(50) NOT NULL,
                    date DATETIME NOT NULL,
                    url VARCHAR(500) NOT NULL,
                    images_amounts INT NOT NULL,
                    images VARCHAR(10000),
                    dt_created datetime DEFAULT CURRENT_TIMESTAMP,
                    dt_modified datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )""")
    print('Table created successfully')


if __name__ == '__main__':
    # Check for environment variable
    if not os.getenv("PASSWORD"):
        raise RuntimeError("PASSWORD is not set: export PASSWORD='your password'")

    # Connect to database
    try:
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd=os.getenv("PASSWORD"),
            db='ptt',
        )
    except MySQLdb.Error as e:
        print(e)
        sys.exit()

    create_beauty_table()
