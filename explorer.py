import sqlite3
from tabulate import tabulate
from colorama import Fore, Back, Style

def display_banner():
    banner = """
    ██╗░░██╗███████╗███╗░░██╗  ██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░██████╗
    ╚██╗██╔╝██╔════╝████╗░██║  ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔════╝
    ░╚███╔╝░█████╗░░██╔██╗██║  ██████╦╝██║░░░░░██║░░██║██║░░╚═╝█████═╝░╚█████╗░
    ░██╔██╗░██╔══╝░░██║╚████║  ██╔══██╗██║░░░░░██║░░██║██║░░██╗██╔═██╗░░╚═══██╗
    ██╔╝╚██╗███████╗██║░╚███║  ██████╦╝███████╗╚█████╔╝╚█████╔╝██║░╚██╗██████╔╝
    ╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝  ╚═════╝░╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░
        XenBlocks Python Block Explorer by TreeCityWes.eth
        Buy Me A Coffee on HashHead.io 
    """
    print(Fore.LIGHTGREEN_EX + banner + Style.RESET_ALL)


def display_table(data, headers, title=None):
    if title:
        print(title)
    if not data:
        print("\nNo data available.\n")
        return
    print(tabulate(data, headers, tablefmt='grid', numalign="right", stralign="left", colalign=("right",)))
    print()  # Add a newline for better readability


def search_by_accounts():
    account = input("Enter the Account: ").lower()
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*), COUNT(CASE WHEN block_type = 'xuni' THEN 1 END),
               COUNT(CASE WHEN block_type = 'super' THEN 1 END) 
        FROM blocks 
        WHERE account = ?
    """, (account,))
    result = cursor.fetchone()
    block_count = result[0] if result else 0  # Total blocks including 'XUNI'
    xuni_block_count = result[1] if result else 0
    super_block_count = result[2] if result else 0
    
    # Subtract 'XUNI' blocks from total blocks
    block_count -= xuni_block_count  # Now, block_count is the count of 'regular' and 'super' blocks only
    
    data = [['Account', account], ['Total Blocks', block_count], ['Total XUNI Blocks', xuni_block_count], ['Total Super Blocks', super_block_count]]
    display_table(data, ['Field', 'Value'])
    
    while True:
        print("1. Last 10 Regular Blocks")
        print("2. Last 10 XUNI Blocks")
        print("3. Last 10 Super Blocks")
        print("4. Return to Main Menu\n")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            cursor.execute("""
                SELECT block_id, created_at
                FROM blocks
                WHERE account = ? AND block_type = 'regular'
                ORDER BY created_at DESC
                LIMIT 10
            """, (account,))
            results = cursor.fetchall()
            print("Last 10 Regular Blocks:")
            display_table(results, ['Block ID', 'Timestamp'])
        
        elif choice == '2':
            cursor.execute("""
                SELECT block_id, created_at
                FROM blocks
                WHERE account = ? AND block_type = 'xuni'
                ORDER BY created_at DESC
                LIMIT 10
            """, (account,))
            results = cursor.fetchall()
            print("Last 10 XUNI Blocks:")
            display_table(results, ['Block ID', 'Timestamp'])
        
        elif choice == '3':
            cursor.execute("""
                SELECT block_id, created_at
                FROM blocks
                WHERE account = ? AND block_type = 'super'
                ORDER BY created_at DESC
                LIMIT 10
            """, (account,))
            results = cursor.fetchall()
            print("Last 10 Super Blocks:")
            display_table(results, ['Block ID', 'Timestamp'])
        
        elif choice == '4':
            break
        
        else:
            print("\nInvalid choice. Please try again.\n")
    
    conn.close()

def search_by_block_id():
    block_id = input("Enter the Block ID: ")
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT block_id, account, created_at, block_type 
        FROM blocks 
        WHERE block_id = ?
    """, (block_id,))
    result = cursor.fetchone()
    
    if result:
        block_type = result[3].capitalize() + ' Block'  # Capitalize the block type and append ' Block'
        data = [['Block ID', result[0]], ['Miner', result[1]], ['Timestamp', result[2]], ['Type', block_type]]
        display_table(data, ['Field', 'Value'])
    else:
        print("\nNo block found with the given ID.\n")
    
    input("Press Enter to return to the main menu...")
    conn.close()

def show_top_blocks(block_type='all', top_n=20):
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    condition = ""
    if block_type == 'super' or block_type == 'xuni':
        condition = f"WHERE block_type = '{block_type}' "
    elif block_type == 'all':
        condition = "WHERE block_type != 'xuni' "  # Exclude 'XUNI' blocks when block_type is 'all'
    
    query = f"""
        SELECT account, COUNT(*) AS count 
        FROM blocks {condition}
        GROUP BY account
        ORDER BY count DESC
        LIMIT {top_n}
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    ranked_results = [[rank + 1, account, count] for rank, (account, count) in enumerate(results)]
    
    headers = ['Rank', 'Account', 'Count']
    title = f"Top {top_n} {block_type.title()} Block Holders" if block_type != 'all' else f"Top {top_n} Total Block Holders"
    display_table(ranked_results, headers, title)
    
    input("Press Enter to return to the main menu...")
    conn.close()


def show_last_blocks(block_type='all', last_n=10):
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    condition = ""
    if block_type == 'super' or block_type == 'xuni':
        condition = f"WHERE block_type = '{block_type}' "
    
    query = f"""
        SELECT block_id, account, created_at 
        FROM blocks {condition}
        ORDER BY created_at DESC
        LIMIT {last_n}
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    headers = ['Block ID', 'Account', 'Timestamp']
    title = f"Last {last_n} {block_type.title()} Blocks" if block_type != 'all' else f"Last {last_n} Blocks"
    display_table(results, headers, title)
    
    input("Press Enter to return to the main menu...")
    conn.close()


def main_menu():
    while True:
        display_banner()
        print("1. Search by Block ID")
        print("2. Search by Accounts")
        print("3. Show Last 10 Blocks")
        print("4. Show Last 10 Super Blocks")
        print("5. Show Last 10 XUNI Blocks")
        print("6. Top 20 Total Block Holders")
        print("7. Top 20 Super Block Holders")
        print("8. Top 20 XUNI Block Holders")
        print("9. Exit\n")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            search_by_block_id()
        elif choice == '2':
            search_by_accounts()
        elif choice == '3':
            show_last_blocks(block_type='all', last_n=10)
        elif choice == '4':
            show_last_blocks(block_type='super', last_n=10)
        elif choice == '5':
            show_last_blocks(block_type='xuni', last_n=10)
        elif choice == '6':
            show_top_blocks(block_type='all', top_n=20)
        elif choice == '7':
            show_top_blocks(block_type='super', top_n=20)
        elif choice == '8':
            show_top_blocks(block_type='xuni', top_n=20)
        elif choice == '9':
            print("Exiting... Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
