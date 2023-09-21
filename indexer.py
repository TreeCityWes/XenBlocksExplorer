import sqlite3
import json

def count_uppercase_letters(hash_to_verify):
    capital_count = 0
    for char in hash_to_verify:
        if char.isalpha() and char.isupper():
            capital_count += 1
    return capital_count

def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blocks (
        block_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hash_to_verify TEXT,
        key TEXT UNIQUE,
        account TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_super_block INTEGER DEFAULT 0
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS super_blocks (
        account TEXT PRIMARY KEY,
        super_block_count INTEGER
    )
    """)

def main():
    # Connect to the source SQLite database
    source_conn = sqlite3.connect("blockchain.db")
    source_cursor = source_conn.cursor()

    # Connect to the destination SQLite database
    index_conn = sqlite3.connect("blockchainindex.db")
    index_cursor = index_conn.cursor()

    # Create tables in the destination database
    create_tables(index_cursor)

    # Fetch records from the source database
    source_cursor.execute("SELECT records_json FROM blockchain")
    records = source_cursor.fetchall()

    all_values = []
    for record in records:
        records_json = record[0]
        records_list = json.loads(records_json)

        for item in records_list:
            hash_to_verify = item.get("hash_to_verify")
            key = item.get("key")
            account = item.get("account")
            created_at = item.get("date")
            is_super_block = 1 if count_uppercase_letters(hash_to_verify) >= 65 else 0

            all_values.append((hash_to_verify, key, account, created_at, is_super_block))

            if is_super_block:
                index_cursor.execute("""
                INSERT OR IGNORE INTO super_blocks (account, super_block_count)
                VALUES (?, 0);
                """, (account,))

                index_cursor.execute("""
                UPDATE super_blocks
                SET super_block_count = super_block_count + 1
                WHERE account = ?;
                """, (account,))

    try:
        index_cursor.executemany("""
        INSERT OR IGNORE INTO blocks (hash_to_verify, key, account, created_at, is_super_block)
        VALUES (?, ?, ?, ?, ?)
        """, all_values)
        index_conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print(f"Processed {len(all_values)} records.")

    source_conn.close()
    index_conn.close()

if __name__ == "__main__":
    main()
