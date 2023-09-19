import sqlite3

# Function to display banner
def display_banner():
    banner = """

██╗░░██╗███████╗███╗░░██╗  ██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░██████╗
╚██╗██╔╝██╔════╝████╗░██║  ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔════╝
░╚███╔╝░█████╗░░██╔██╗██║  ██████╦╝██║░░░░░██║░░██║██║░░╚═╝█████═╝░╚█████╗░
░██╔██╗░██╔══╝░░██║╚████║  ██╔══██╗██║░░░░░██║░░██║██║░░██╗██╔═██╗░░╚═══██╗
██╔╝╚██╗███████╗██║░╚███║  ██████╦╝███████╗╚█████╔╝╚█████╔╝██║░╚██╗██████╔╝
╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝  ╚═════╝░╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░
XenBlocks Python Explorer by TreeCityWes.eth
    """
    print(banner)


def search_by_block_id():
    block_id = input("Enter the Block ID: ")
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT block_id, account, created_at, is_super_block FROM blocks WHERE block_id = ?", (block_id,))
    result = cursor.fetchone()
    if result:
        print("\033[92m")  # Set text to bright green
        print(f"Block ID: {result[0]}")
        print(f"Miner: {result[1]}")
        print(f"Timestamp: {result[2]}")
        print(f"Type: {'Super Block' if result[3] else 'Regular Block'}")
        print("\033[0m")  # Reset text color
    else:
        print("No block found with the given ID.")
    conn.close()


def search_by_accounts():
    account = input("Enter the Account: ")
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM blocks WHERE account = ?", (account,))
    result = cursor.fetchone()
    block_count = result[0] if result else 0
    
    cursor.execute("SELECT super_block_count FROM super_blocks WHERE account = ?", (account,))
    result = cursor.fetchone()
    super_block_count = result[0] if result else 0
    
    print("\033[92m")  # Set text to bright green
    print(f"Account: {account}")
    print(f"Total Blocks: {block_count}")
    print(f"Total Super Blocks: {super_block_count}")
    print("\033[0m")  # Reset text color
    
    # Last 5 blocks
    cursor.execute("SELECT block_id, created_at FROM blocks WHERE account = ? ORDER BY block_id DESC LIMIT 5", (account,))
    last_5_blocks = cursor.fetchall()
    
    print("\033[92mLast 5 Blocks Mined:\033[0m")
    for block in last_5_blocks:
        print(f"  Block ID: {block[0]}, Timestamp: {block[1]}")
    
    # Last 5 super blocks
    # Assuming super blocks have a special flag (is_super_block = 1) in the "blocks" table
    cursor.execute("SELECT block_id, created_at FROM blocks WHERE account = ? AND is_super_block = 1 ORDER BY block_id DESC LIMIT 5", (account,))
    last_5_super_blocks = cursor.fetchall()
    
    print("\033[92mLast 5 Super Blocks Mined:\033[0m")
    for block in last_5_super_blocks:
        print(f"  Block ID: {block[0]}, Timestamp: {block[1]}")
    
    conn.close()

def show_last_10_blocks():
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT block_id, account, created_at FROM blocks ORDER BY block_id DESC LIMIT 10")
    last_10_blocks = cursor.fetchall()
    
    print("\033[92mLast 10 Blocks:\033[0m")
    for block in last_10_blocks:
        print(f"  Block ID: {block[0]}, Miner: {block[1]}, Timestamp: {block[2]}")
        
    conn.close()

def show_last_5_super_blocks():
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT block_id, account, created_at FROM blocks WHERE is_super_block = 1 ORDER BY block_id DESC LIMIT 5")
    last_5_super_blocks = cursor.fetchall()
    
    print("\033[92mLast 5 Super Blocks:\033[0m")
    for block in last_5_super_blocks:
        print(f"  Block ID: {block[0]}, Miner: {block[1]}, Timestamp: {block[2]}")
        
    conn.close()

def main_menu():
    while True:
        print("\033[93m")  # Set text to bright yellow
        print("=== Block Explorer Menu ===")
        print("1. Search by Block ID")
        print("2. Search by Accounts")
        print("3. Last 10 Blocks")
        print("4. Last 5 Super Blocks")
        print("5. Exit")
        print("\033[0m")  # Reset text color

        choice = input("Enter your choice: ")

        if choice == '1':
            search_by_block_id()
        elif choice == '2':
            search_by_accounts()
        elif choice == '3':
            show_last_10_blocks()
        elif choice == '4':
            show_last_5_super_blocks()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    display_banner()  # Corrected function name
    main_menu()
