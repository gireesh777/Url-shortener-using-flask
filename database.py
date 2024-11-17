import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self, db_name='url_shortener.db'):
        self.db_name = db_name
        self.create_tables()

    def create_connection(self):
        """Create a database connection."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
        return conn  # Always return the connection object

    def create_tables(self):
        """Create tables if they do not exist."""
        conn = self.create_connection()
        if conn:
            try:
                with conn:
                    conn.execute('''
                        CREATE TABLE IF NOT EXISTS urls (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            short_code TEXT UNIQUE NOT NULL,
                            original_url TEXT NOT NULL
                        )
                    ''')
            except Error as e:
                print(f"Error creating tables: {e}")
            finally:
                conn.close()

    def insert_url(self, short_code, original_url):
        """Insert a new URL into the urls table."""
        conn = self.create_connection()
        if conn:
            try:
                with conn:
                    conn.execute('''
                        INSERT INTO urls (short_code, original_url)
                        VALUES (?, ?)
                    ''', (short_code, original_url))
            except Error as e:
                print(f"Error inserting URL: {e}")
            finally:
                conn.close()

    def url_exists(self, short_code):
        """Check if the short code already exists."""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM urls WHERE short_code = ?
        ''', (short_code,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def get_url(self, short_code):
        """Retrieve the original URL and creation date for a given short code."""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT original_url FROM urls WHERE short_code = ?
        ''', (short_code,))
        url_details = cursor.fetchone()
        conn.close()
        if url_details is None:
            return None  
        return url_details
