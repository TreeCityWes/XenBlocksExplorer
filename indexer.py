import sqlite3
import json

def count_uppercase_letters(string: str) -> int:
    """Counts the number of uppercase letters in a string"""
    return sum(1 for char in string if char.isupper())

def connect_to_db(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path, timeout=10)

def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blocks (
        block_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hash_to_verify TEXT,
        key TEXT UNIQUE,
        account TEXT,
        xuni_account TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        block_type TEXT DEFAULT 'regular'
    )
    """)

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS super_blocks (
        account TEXT PRIMARY KEY,
        super_block_count INTEGER DEFAULT 0
    )
    """)
    
def process_blocks(source_cursor, index_conn, index_cursor):
    processed_records = 0
    try:
        source_cursor.execute("SELECT records_json FROM blockchain")
        all_values = source_cursor.fetchall()

        for item in all_values:
            records_json = item[0]
            records_list = json.loads(records_json)  # Decode the JSON string to a Python list
        
            for record in records_list:  # Iterate over each dictionary in the list
                if isinstance(record, dict):  # Check if the item is a dictionary
                    hash_to_verify = record.get("hash_to_verify")
                    key = record.get("key")
                    account = record.get("account")
                    xuni_account = record.get("xuni_account", "")
                    created_at = record.get("date")
                    is_xuni_block = 1 if record.get("xuni_id") is not None else 0
                
                if not is_xuni_block:
                    is_super_block = 1 if count_uppercase_letters(hash_to_verify) >= 65 else 0
                else:
                    is_super_block = 0
    
                # Insert into blocks table and handle unique constraint failure if needed.
                try:
                    index_cursor.execute("""
                    INSERT INTO blocks (hash_to_verify, key, account, xuni_account, created_at, block_type)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """, (hash_to_verify, key, account, xuni_account, created_at, 'xuni' if is_xuni_block else 'super' if is_super_block else 'regular'))
                except sqlite3.IntegrityError:
                    print(f"Entry with key {key} already exists in blocks. Skipping...")
    
                # If the block is a super block and not a xuni block, update the super_blocks table
                if is_super_block and not is_xuni_block:
                    index_cursor.execute("""
                    INSERT OR IGNORE INTO super_blocks (account, super_block_count)
                    VALUES (?, 0);
                    """, (account,))
                    
                    index_cursor.execute("""
                    UPDATE super_blocks
                    SET super_block_count = super_block_count + 1
                    WHERE account = ?;
                    """, (account,))
   
            processed_records += 1
            if processed_records % 1000 == 0:
                print(f"Processed {processed_records} records so far...")

        index_conn.commit()

    except Exception as e:  # Handle the exception properly
        print(f"An unexpected error occurred: {e}")
        index_conn.rollback()

def main():
    source_conn = connect_to_db("blockchain.db")
    source_cursor = source_conn.cursor()
    
    index_conn = connect_to_db("blockchainindex.db")
    index_cursor = index_conn.cursor()
    
    create_tables(index_cursor)
    process_blocks(source_cursor, index_conn, index_cursor)
    
    source_conn.close()
    index_conn.close()

if __name__ == "__main__":
    main()
