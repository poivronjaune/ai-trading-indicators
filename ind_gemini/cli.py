# ind/cli.py

import os
from pathlib import Path
from .core import IndicatorProcessor

def main():
    """Main function to run the interactive Command-Line Interface."""
    print("--- Welcome to the Financial Indicator Calculator ---")

    # 1. Get and validate the input folder from the user
    while True:
        try:
            input_folder_str = input("➡️ Enter the path to your data folder (e.g., 'data/'): ")
            input_folder = Path(input_folder_str).resolve()
            
            if not input_folder.is_dir():
                print(f"❌ Error: Folder not found at '{input_folder}'. Please try again.")
                continue

            csv_files = sorted([f.name for f in input_folder.glob("*.csv")])
            if not csv_files:
                print(f"❌ Error: No CSV files found in '{input_folder}'. Please try again.")
                continue
            
            break # Exit loop if folder and files are valid
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return

    # 2. Let the user select a file from the list
    print("\n📄 Available CSV files:")
    for i, filename in enumerate(csv_files):
        print(f"  {i + 1}: {filename}")

    while True:
        try:
            choice = int(input("\n➡️ Select a file by number: ")) - 1
            if 0 <= choice < len(csv_files):
                selected_file = csv_files[choice]
                break
            else:
                print("Invalid number. Please select from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    input_file_path = input_folder / selected_file
    print(f"\n⚙️  Processing '{selected_file}'...")

    # 3. Define the output folder based on the input folder's name
    output_folder_name = f"{input_folder.name}_ind"
    output_folder = input_folder.parent / output_folder_name
    output_folder.mkdir(exist_ok=True)
    print(f"💾 Results will be saved in '{output_folder}'")

    # 4. Process the file using the core logic
    try:
        processor = IndicatorProcessor(input_file_path)
        processor.add_all_default_indicators()
        processor.save_results(output_folder)
        print(f"\n✅ Success! Processed file saved to '{output_folder / selected_file}'")
    except Exception as e:
        print(f"\n❌ Error processing file: {e}")
        print("Please check the CSV format and ensure TA-Lib is installed correctly.")

if __name__ == '__main__':
    main()
    