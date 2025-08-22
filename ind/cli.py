# cli.py
import os
import argparse
from pathlib import Path
from .processor import IndicatorProcessor
from typing import Optional

def main():
    """Main entry point for the indicators CLI."""
    parser = argparse.ArgumentParser(description="Process financial data and generate technical indicators.")
    parser.add_argument("--input-folder", type=str, help="Path to input folder containing CSV files")
    parser.add_argument("--output-folder", type=str, help="Path to output folder for processed files")
    parser.add_argument("--file", type=str, help="Specific CSV file to process")
    args = parser.parse_args()

    processor = IndicatorProcessor()

    if not args.input_folder:
        # Interactive mode
        print("Interactive mode: Please provide input folder path")
        input_folder = input("Enter path to data folder (default: ./data): ") or "./data"
        input_folder = Path(input_folder).resolve()
        
        # List available CSV files
        csv_files = [f for f in input_folder.glob("*.csv") if f.is_file()]
        if not csv_files:
            print(f"No CSV files found in {input_folder}")
            return
        
        print("\nAvailable CSV files:")
        for i, file in enumerate(csv_files, 1):
            print(f"{i}. {file.name}")
        
        file_choice = input("\nEnter the number of the file to process (or 'all' for all files): ")
        if file_choice.lower() == "all":
            files_to_process = csv_files
        else:
            try:
                index = int(file_choice) - 1
                if 0 <= index < len(csv_files):
                    files_to_process = [csv_files[index]]
                else:
                    print("Invalid selection")
                    return
            except ValueError:
                print("Invalid input")
                return
    else:
        # Direct mode
        input_folder = Path(args.input_folder).resolve()
        if args.file:
            files_to_process = [input_folder / args.file]
        else:
            files_to_process = [f for f in input_folder.glob("*.csv") if f.is_file()]

    output_folder = Path(args.output_folder).resolve() if args.output_folder else input_folder.parent / f"{input_folder.name}_ind"
    output_folder.mkdir(exist_ok=True)

    for file_path in files_to_process:
        print(f"Processing {file_path.name}...")
        try:
            processor.load_data(str(file_path))
            processor.add_default_indicators()
            processor.save_results(str(output_folder))
            print(f"Successfully processed {file_path.name}")
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")

if __name__ == "__main__":
    main()
