import sqlite3
from tabulate import tabulate
from colorama import Fore, Style

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
    print(tabulate(data, headers, tablefmt='grid'))
    print()

def get_total_blocks(conn, block_type='all'):
    cursor = conn.cursor()
    if block_type == 'all':
        cursor.execute("SELECT COUNT(*) FROM blocks")
    else:
        cursor.execute("SELECT COUNT(*) FROM blocks WHERE block_type = ?", (block_type,))
    result = cursor.fetchone()
    return result[0] if result else 0

def display_total_blocks(block_type='all'):
    conn = sqlite3.connect("blockchainindex.db")
    total_blocks = get_total_blocks(conn, block_type)
    print(f"Total {block_type.capitalize()} Blocks in Network: {total_blocks}")
    input("Press Enter to return to the main menu...")
    conn.close()

def search_by_accounts():
    account = input("Enter the Account: ").lower()
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*), 
               COUNT(CASE WHEN block_type = 'xuni' THEN 1 END) AS xuni_count,
               COUNT(CASE WHEN block_type = 'super' THEN 1 END) AS super_count
        FROM blocks 
        WHERE account = ?
    """, (account,))
    result = cursor.fetchone()
    
    if result:
        total_blocks, xuni_blocks, super_blocks = result
        data = [['Account', account], ['Total Blocks', total_blocks], ['Total XUNI Blocks', xuni_blocks], ['Total Super Blocks', super_blocks]]
        display_table(data, ['Field', 'Value'])
    else:
        print("\nNo data found for the provided account.\n")
    
    while True:
        print("1. Last 10 Regular Blocks")
        print("2. Last 10 XUNI Blocks")
        print("3. Last 10 Super Blocks")
        print("4. Return to Main Menu\n")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            display_last_blocks(cursor, account, 'regular')
        elif choice == '2':
            display_last_blocks(cursor, account, 'xuni')
        elif choice == '3':
            display_last_blocks(cursor, account, 'super')
        elif choice == '4':
            break
        else:
            print("\nInvalid choice. Please try again.\n")
    
    conn.close()

def display_last_blocks(cursor, account, block_type, last_n=10):
    cursor.execute("""
        SELECT block_id, created_at
        FROM blocks
        WHERE account = ? AND block_type = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (account, block_type, last_n))
    results = cursor.fetchall()
    if results:
        display_table(results, ['Block ID', 'Timestamp'], title=f"Last {last_n} {block_type.capitalize()} Blocks:")
    else:
        print(f"\nNo {block_type} blocks found for the provided account.\n")

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
        data = [['Block ID', result[0]], ['Miner', result[1]], ['Timestamp', result[2]], ['Type', result[3].capitalize() + ' Block']]
        display_table(data, ['Field', 'Value'])
    else:
        print("\nNo block found with the given ID.\n")
    
    input("Press Enter to return to the main menu...")
    conn.close()

def show_top_blocks(block_type='all', top_n=20):
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    if block_type == 'all':
        cursor.execute("""
            SELECT account, COUNT(*) AS count 
            FROM blocks 
            GROUP BY account
            ORDER BY count DESC
            LIMIT ?
        """, (top_n,))
    else:
        cursor.execute("""
            SELECT account, COUNT(*) AS count 
            FROM blocks 
            WHERE block_type = ?
            GROUP BY account
            ORDER BY count DESC
            LIMIT ?
        """, (block_type, top_n,))
    results = cursor.fetchall()
    
    if results:
        display_table([[rank + 1, account, count] for rank, (account, count) in enumerate(results)], ['Rank', 'Account', 'Count'], title=f"Top {top_n} {block_type.capitalize()} Block Holders")
    else:
        print("\nNo data available.\n")
    
    input("Press Enter to return to the main menu...")
    conn.close()

def show_last_blocks(block_type='all', last_n=10):
    conn = sqlite3.connect("blockchainindex.db")
    cursor = conn.cursor()
    
    if block_type == 'all':
        cursor.execute("""
            SELECT block_id, account, created_at, block_type 
            FROM blocks 
            ORDER BY created_at DESC
            LIMIT ?
        """, (last_n,))
    else:
        cursor.execute("""
            SELECT block_id, account, created_at 
            FROM blocks 
            WHERE block_type = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (block_type, last_n,))
    results = cursor.fetchall()
    
    if results:
        display_table(results, ['Block ID', 'Account', 'Timestamp', 'Block Type'], title=f"Last {last_n} {block_type.capitalize()} Blocks")
    else:
        print("\nNo data available.\n")
    
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
        print("9. Total Network Blocks")
        print("10. Total Network SuperBlocks")
        print("11. Total Network XUNI Blocks")
        print("12. Exit\n")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            search_by_block_id()
        elif choice == '2':
            search_by_accounts()
        elif choice == '3':
            show_last_blocks('all')
        elif choice == '4':
            show_last_blocks('super')
        elif choice == '5':
            show_last_blocks('xuni')
        elif choice == '6':
            show_top_blocks('all')
        elif choice == '7':
            show_top_blocks('super')
        elif choice == '8':
            show_top_blocks('xuni')
        elif choice == '9':
            display_total_blocks('all')
        elif choice == '10':
            display_total_blocks('super')
        elif choice == '11':
            display_total_blocks('xuni')
        elif choice == '12':
            print("Exiting... Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
