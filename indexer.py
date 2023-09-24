import sqlite3
import json

def count_uppercase_letters(string):
    return sum(1 for char in string if char.isalpha() and char.isupper())

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
        super_block_count INTEGER
    )
    """)

def main():
    print("Compiling the data... This may take a while, please wait.")

    source_conn = sqlite3.connect("blockchain.db")
    source_cursor = source_conn.cursor()

    index_conn = sqlite3.connect("blockchainindex.db")
    index_cursor = index_conn.cursor()

    create_tables(index_cursor)

    source_cursor.execute("SELECT records_json FROM blockchain")
    
    # Start a transaction
    index_conn.execute('BEGIN TRANSACTION')

    processed_records = 0
    try:
        for record in iter(source_cursor.fetchone, None):  # Using fetchone in a loop
            records_list = json.loads(record[0])

            all_values = []
            for item in records_list:
                hash_to_verify = item.get("hash_to_verify")
                key = item.get("key")
                account = item.get("account")
                xuni_account = item.get("xuni_account", "")
                created_at = item.get("date")
                
                is_xuni_block = item.get("xuni_id") is not None
                is_super_block = count_uppercase_letters(hash_to_verify) >= 65  # Super block condition
                
                # Default block type is regular, unless it's a Xuni block or Super block
                if is_xuni_block:
                    block_type = 'xuni'
                elif is_super_block:
                    block_type = 'super'
                else:
                    block_type = 'regular'
                
                all_values.append((hash_to_verify, key, account, xuni_account, created_at, block_type))
                
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
                    
            index_cursor.executemany("""
            INSERT OR IGNORE INTO blocks (hash_to_verify, key, account, xuni_account, created_at, block_type)
            VALUES (?, ?, ?, ?, ?, ?)
            """, all_values)
            
            processed_records += len(all_values)

            # Print a progress update every 1000 records processed
            if processed_records % 1000 == 0:
                print(f"Processed {processed_records} records so far...")

        # Commit the transaction
        index_conn.commit()

    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
        index_conn.rollback()
    except Exception as e:
        print(f"An error occurred: {e}")
        index_conn.rollback()

    print(f"Finished processing. Total records processed: {processed_records}.")
    
    source_conn.close()
    index_conn.close()

if __name__ == "__main__":
    main()
