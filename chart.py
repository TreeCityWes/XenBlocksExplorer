import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Function to display banner
def display_banner():
    banner = """

    
██╗░░██╗███████╗███╗░░██╗  ██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░██████╗
╚██╗██╔╝██╔════╝████╗░██║  ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔════╝
░╚███╔╝░█████╗░░██╔██╗██║  ██████╦╝██║░░░░░██║░░██║██║░░╚═╝█████═╝░╚█████╗░
░██╔██╗░██╔══╝░░██║╚████║  ██╔══██╗██║░░░░░██║░░██║██║░░██╗██╔═██╗░░╚═══██╗
██╔╝╚██╗███████╗██║░╚███║  ██████╦╝███████╗╚█████╔╝╚█████╔╝██║░╚██╗██████╔╝
╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝  ╚═════╝░╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░
    XenBlocks Python Chart Creator by TreeCityWes.eth
    """
    print(banner)

# Function to plot data
def plot_data(df, title):
    if df.empty:
        print(f"No data to plot for {title}")
        return
    plt.figure(figsize=(10, 6))
    plt.plot(df['created_at'], df['cumulative_blocks'], 'r--', marker='o')
    plt.xlabel('Time')
    plt.ylabel('Blocks')
    plt.title(title)
    plt.grid(True)
    plt.show()

print("Loading data... Please wait.")

# Connect to the SQLite database
conn = sqlite3.connect("blockchainindex.db")

# Query to fetch data from blocks table
query = "SELECT * FROM blocks"
df = pd.read_sql_query(query, conn)

# Debug: Print first few rows and number of rows to check data
print("Data loaded successfully!")
print("First few rows of fetched data:")
print(df.head())
print(f"Total number of rows: {len(df)}")

# Convert the 'created_at' column to datetime format and then to date
df['created_at'] = pd.to_datetime(df['created_at']).dt.date

# Convert 'account' to lowercase
df['account'] = df['account'].str.lower()

# Display the banner
display_banner()

# Function to display menu options
def display_menu():
    print("\nPlease choose a chart to display:")
    print("1. Total Network Blocks Over Time")
    print("2. Total Network Super Blocks Over Time")
    print("3. Total Blocks by Account")
    print("4. Total Superblocks by Account")
    print("5. Exit")
    return input("Your choice: ")
# Main menu loop
while True:
    choice = display_menu()
    
    if choice == '1':
        # Plot total blocks over time
        total_blocks_df = df.groupby('created_at').size().reset_index(name='blocks')
        total_blocks_df['cumulative_blocks'] = total_blocks_df['blocks'].cumsum()
        plot_data(total_blocks_df, 'Total Network Blocks Over Time')
        
    elif choice == '2':
        # Plot superblocks mined over time
        superblocks_df = df[df['is_super_block'] == 1].groupby('created_at').size().reset_index(name='blocks')
        superblocks_df['cumulative_blocks'] = superblocks_df['blocks'].cumsum()
        plot_data(superblocks_df, 'Total Network Super Blocks Over Time')
        
    elif choice == '3':
        # Plot blocks mined by a specific account over time
        account_name = input("Enter the account name: ").lower()
        account_blocks_df = df[df['account'] == account_name].groupby('created_at').size().reset_index(name='blocks')
        account_blocks_df['cumulative_blocks'] = account_blocks_df['blocks'].cumsum()
        plot_data(account_blocks_df, f'Total Blocks by Account: {account_name}')
        
    elif choice == '4':
        # Plot superblocks mined by a specific account over time
        account_name = input("Enter the account name: ").lower()
        
        # Filter DataFrame for the specific account and only superblocks
        superblocks_account_df = df[(df['account'] == account_name) & (df['is_super_block'] == 1)]
        
        # Debug: Check if the DataFrame is empty
        if superblocks_account_df.empty:
            print(f"No superblocks found for account {account_name}.")
            continue
            
        # Group by 'created_at' and aggregate the count of blocks per day
        superblocks_account_df = superblocks_account_df.groupby('created_at').size().reset_index(name='blocks')
        
        # Calculate the cumulative sum of blocks over time
        superblocks_account_df['cumulative_blocks'] = superblocks_account_df['blocks'].cumsum()
        
        # Debug: Print first few rows of DataFrame
        print("Debug: First few rows of superblocks_account_df:")
        print(superblocks_account_df.head())
        
        # Plot the data
        plot_data(superblocks_account_df, f'Total Superblocks by Account: {account_name}')
        
    elif choice == '5':
        print("Exiting. Goodbye!")
        break
        
    else:
        print("Invalid choice. Please try again.")

# Close the SQLite database connection
conn.close()

