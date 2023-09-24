import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator
import seaborn as sns
from colorama import Fore, Style  # Import the necessary modules from Colorama

sns.set_theme(style="darkgrid")

def display_banner():
    banner = """
██╗░░██╗███████╗███╗░░██╗  ██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░██████╗
╚██╗██╔╝██╔════╝████╗░██║  ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔════╝
░╚███╔╝░█████╗░░██╔██╗██║  ██████╦╝██║░░░░░██║░░██║██║░░╚═╝█████═╝░╚█████╗░
░██╔██╗░██╔══╝░░██║╚████║  ██╔══██╗██║░░░░░██║░░██║██║░░██╗██╔═██╗░░╚═══██╗
██╔╝╚██╗███████╗██║░╚███║  ██████╦╝███████╗╚█████╔╝╚█████╔╝██║░╚██╗██████╔╝
╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝  ╚═════╝░╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░
    XenBlocks Python Chart Creator by TreeCityWes.eth
    Buy Me A Coffee on HashHead.io 
    """
    print(Fore.LIGHTGREEN_EX + banner + Style.RESET_ALL)  # Use colorama to color the banner lime green


def plot_data(df, title):
    if df.empty:
        print(f"No data to plot for {title}")
        return
    
    plt.figure(figsize=(12, 7))
    color = 'tab:blue'
    plt.plot(df['created_at'], df['cumulative_blocks'], color=color, linestyle='-', marker='o')
    plt.fill_between(df['created_at'], df['cumulative_blocks'], color=color, alpha=0.1)
    
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Blocks', fontsize=14)
    plt.title(title, fontsize=16, fontweight='bold')
    plt.show()

print("Loading data... Please wait.")
conn = sqlite3.connect("blockchainindex.db")
query = "SELECT * FROM blocks"
df = pd.read_sql_query(query, conn)
print("Data loaded successfully!")

df['created_at'] = pd.to_datetime(df['created_at'])
df['account'] = df['account'].str.lower()

def display_menu():
    # Assuming display_banner() is a function you have defined elsewhere in your script
    display_banner()  
    print("\nPlease choose a chart to display:")
    print()  # Add a newline for better readability
    print("Network Statistics:")
    print("1. Total Network Blocks Over Time")
    print("2. Total Network Super Blocks Over Time")
    print("3. Total Network XUNI Blocks Over Time")
    print("4. Total Network Distribution (PieChart)")
    print("\nAccount Statistics:")
    print("5. Blocks by Account")
    print("6. XUNI Blocks by Account")
    print("7. Superblocks by Account")
    print("8. Daily Block Distribution for Account")
    print("9. Daily XUNI Block Distribution for Account")
    print("10. Daily Super Block Distribution for Account")
    print("\nDaily Distribution:")
    print("11. Daily Block Distribution")
    print("12. Daily Xuni Block Distribution")
    print("13. Daily Super Block Distribution")
    print("\n14. Exit")
    print()  # Add a newline for better readability
    return input("Your choice: ")

def main():
    while True:
        choice = display_menu()
        
        df_filtered = df  # Modified line: No filtering is done here anymore
        
        if choice == '1':
            # Assuming df is the original DataFrame
            total_blocks_df = df[df['block_type'] != 'xuni'].groupby('created_at').size().reset_index(name='blocks')  # Exclude 'XUNI' blocks
            total_blocks_df['cumulative_blocks'] = total_blocks_df['blocks'].cumsum()
            plot_data(total_blocks_df, 'Total Network Blocks Over Time')

                
        elif choice == '2':
            superblocks_df = df[df['block_type'] == 'super'].groupby('created_at').size().reset_index(name='blocks')
            superblocks_df['cumulative_blocks'] = superblocks_df['blocks'].cumsum()
            plot_data(superblocks_df, 'Total Network Super Blocks Over Time')


        elif choice == '3':
            xuni_blocks_df = df[df['block_type'] == 'xuni'].groupby('created_at').size().reset_index(name='blocks')
            xuni_blocks_df['cumulative_blocks'] = xuni_blocks_df['blocks'].cumsum()
            plot_data(xuni_blocks_df, 'Total Network XUNI Blocks Over Time')


        elif choice == '4':
            block_counts = df['block_type'].value_counts()
            regular_block_count = block_counts.get('regular', 0)
            super_block_count = block_counts.get('super', 0)
            xuni_block_count = block_counts.get('xuni', 0)
            
            # If XUNI blocks are not counted in total blocks
            total_blocks = regular_block_count + super_block_count  # XUNI blocks are not included in total_blocks
            regular_block_percentage = (regular_block_count / total_blocks) * 100
            super_block_percentage = (super_block_count / total_blocks) * 100
            
            plt.pie([regular_block_count, super_block_count],
                    labels=['', ''], autopct='',
                    startangle=140, colors=['#66b3ff', '#99ff99'])
            plt.axis('equal')
            plt.title('Ratio of Blocks and Superblocks', fontsize=16, loc='center')
            legend_labels = [f'Regular Blocks - {regular_block_percentage:.1f}%', f'Superblocks - {super_block_percentage:.1f}%']
            legend = plt.legend(loc='upper left', labels=legend_labels)
            legend.get_frame().set_alpha(1.0)
            
            plt.show()

        elif choice == '5':
            account_name = input("Enter the account name: ").lower()
            account_blocks_df = df_filtered[df_filtered['account'] == account_name].groupby('created_at').size().reset_index(name='blocks')
            account_blocks_df['cumulative_blocks'] = account_blocks_df['blocks'].cumsum()
            plot_data(account_blocks_df, f'Blocks by Account: {account_name}')
        
        elif choice == '6':
            account_name = input("Enter the account name: ").lower()
            xuni_account_blocks_df = df_filtered[(df_filtered['account'] == account_name) & (df_filtered['block_type'] == 'xuni')].groupby('created_at').size().reset_index(name='blocks')
            xuni_account_blocks_df['cumulative_blocks'] = xuni_account_blocks_df['blocks'].cumsum()
            plot_data(xuni_account_blocks_df, f'XUNI Blocks by Account: {account_name}')

        
        elif choice == '7':
            account_name = input("Enter the account name: ").lower()
            superblocks_account_df = df[(df['account'] == account_name) & (df['block_type'] == 'super')].groupby('created_at').size().reset_index(name='blocks')
            superblocks_account_df['cumulative_blocks'] = superblocks_account_df['blocks'].cumsum()
            plot_data(superblocks_account_df, f'Superblocks by Account: {account_name}')


        elif choice == '8':
            account_name = input("Enter the account name: ").lower()
            filtered_df = df_filtered[df_filtered['account'] == account_name]
            
            if filtered_df.empty:
                print(f"No blocks found for account {account_name}.")
            else:
                filtered_df['created_at'].dt.date.value_counts().sort_index().plot(kind='bar', color='skyblue', edgecolor='black')
                plt.title(f'Daily Block Distribution for {account_name}')
                plt.xlabel('Creation Date')
                plt.ylabel('Frequency')
                plt.gcf().autofmt_xdate()
                plt.show()

        elif choice == '9':
            account_name = input("Enter the account name: ").lower()
            filtered_df = df_filtered[(df_filtered['account'] == account_name) & (df_filtered['block_type'] == 'xuni')]
            
            if filtered_df.empty:
                print(f"No XUNI blocks found for account {account_name}.")
            else:
                filtered_df['created_at'].dt.date.value_counts().sort_index().plot(kind='bar', color='#ffcc99', edgecolor='black')
                plt.title(f'Daily XUNI Block Distribution for {account_name}')
                plt.xlabel('Creation Date')
                plt.ylabel('Frequency')
                plt.gcf().autofmt_xdate()
                plt.show()

        elif choice == '10':
            account_name = input("Enter the account name: ").lower()
            filtered_df = df_filtered[(df_filtered['account'] == account_name) & (df_filtered['block_type'] == 'super')]
            
            if filtered_df.empty:
                print(f"No superblocks found for account {account_name}.")
            else:
                filtered_df['created_at'].dt.date.value_counts().sort_index().plot(kind='bar', color='#99ff99', edgecolor='black')
                plt.title(f'Daily Super Block Distribution for {account_name}')
                plt.xlabel('Creation Date')
                plt.ylabel('Frequency')
                plt.gcf().autofmt_xdate()
                plt.show()

        elif choice == '11':
            # Assuming df is the original DataFrame
            plt.hist(df[df['block_type'] != 'xuni']['created_at'], bins=30, color='skyblue', edgecolor='black')  # Exclude 'XUNI' blocks
            plt.title('Daily Blocks Distribution')
            plt.xlabel('Creation Date')
            plt.ylabel('Frequency')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            
            auto_locator = AutoDateLocator(maxticks=10)
            plt.gca().xaxis.set_major_locator(auto_locator)
            
            plt.gcf().autofmt_xdate()
            plt.show()


        elif choice == '12':
            xuni_blocks_df = df_filtered[df_filtered['block_type'] == 'xuni']
            plt.hist(xuni_blocks_df['created_at'], bins=30, color='#ffcc99', edgecolor='black')
            plt.title(f'Daily XUNI Blocks Distribution')
            plt.xlabel('Creation Date')
            plt.ylabel('Frequency')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            
            auto_locator = AutoDateLocator(maxticks=10)
            plt.gca().xaxis.set_major_locator(auto_locator)
            
            plt.gcf().autofmt_xdate()
            plt.show()

        elif choice == '13':
            super_blocks_df = df_filtered[df_filtered['block_type'] == 'super']
            plt.hist(super_blocks_df['created_at'], bins=30, color='#99ff99', edgecolor='black')
            plt.title(f'Daily Super Blocks Distribution')
            plt.xlabel('Creation Date')
            plt.ylabel('Frequency')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            
            auto_locator = AutoDateLocator(maxticks=10)
            plt.gca().xaxis.set_major_locator(auto_locator)
            
            plt.gcf().autofmt_xdate()
            plt.show()



        elif choice == '14':
            print("Exiting. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

conn.close()
