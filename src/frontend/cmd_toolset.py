import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def analyze_csv_files(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if not csv_files:
        print(f"No CSV files found in the folder '{folder_path}'.")
        return

    # If we want to plot a graph on the CSV file itself
    # for file in csv_files:
    #     file_path = os.path.join(folder_path, file)
    #     print(f"\nProcessing file: {file}")

    #     try:
    #         # Load CSV
    #         df = pd.read_csv(file_path)

    #         # Check if 'description' column exists
    #         if 'Description' not in df.columns:
    #             print("Column 'Description' not found. Skipping this file.")
    #             continue

    #         # Count frequencies
    #         frequencies = Counter(df['Description'].dropna())
    #         table_data = frequencies.most_common()

    #         # Display table
    #         print("\nFrequency Table:")
    #         print(f"{'Item':<30}{'Frequency':<10}")
    #         print("-" * 40)
    #         for item, count in table_data:
    #             print(f"{item:<30}{count:<10}")

    #         # Display ASCII graph
    #         print("\nGraph Representation:")
    #         max_label_width = 30
    #         max_bar_width = 40  # Adjust for terminal width
    #         max_count = max(frequencies.values())

    #         for item, count in table_data:
    #             label = item[:max_label_width] + ("..." if len(item) > max_label_width else "")
    #             bar_length = int((count / max_count) * max_bar_width)
    #             bar = "#" * bar_length
    #             print(f"{label:<{max_label_width}} | {bar} ({count})")

    #     except Exception as e:
    #         print(f"Error processing file '{file}': {e}")


    #If we want to display a graph using matplotlib and there is a save to local system

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        print(f"\nProcessing file: {file}")

        try:
            df = pd.read_csv(file_path)

            # Convert all column names to lowercase for case-insensitive comparison
            if 'description'.lower() not in [col.lower() for col in df.columns]:
                print("Column 'description' not found. Skipping this file.")
                continue

            # Count frequencies
            frequencies = Counter(df['description'].dropna())
            table_data = frequencies.most_common()

            # Display table
            print("\nFrequency Table:")
            print(f"{'Item':<30}{'Frequency':<10}")
            print("-" * 40)
            for item, count in table_data:
                print(f"{item:<30}{count:<10}")

            # Plot graph
            items, counts = zip(*table_data)
            plt.figure(figsize=(10, 6))
            plt.bar(items, counts, color='skyblue')
            plt.xlabel('Items', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.title(f'Frequency of Items in {file}', fontsize=14)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error processing file '{file}': {e}")

        
        

if __name__ == "__main__":
    print("Welcome to CMD Toolset")
    folder_path = input("Enter the folder path containing CSV files: ").strip()
    analyze_csv_files(folder_path)
