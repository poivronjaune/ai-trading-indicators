# AI Trading Indicators

>**Warning**  
>Work in progress, not production ready, poor documentation :)  
>This project was generated from AI Agents. Unsuccessful generations are stored in folders and filenames with the _chatgpt or .chatgpt extensions. Current release is under the ind folder. 

## Overview

The **Indicators** package is a Python library designed to process financial time-series data stored in CSV files and generate technical indicators using the TA-Lib library. It provides both a command-line interface (CLI) for interactive use and a programmatic API for integration into other applications.

Key features include:
- Loading and processing standardized CSV files with financial price data.
- Automatic deduplication of datetime entries.
- Calculation of default technical indicators: Simple Moving Averages (SMA), Exponential Moving Averages (EMA), and Bollinger Bands.
- Modular design for adding custom indicators.
- Organized input/output file management.

This project is licensed under the MIT License.

## Requirements

- Python 3.8 or higher.
- Platform-specific TA-Lib wheel file (required for technical indicator calculations).

## Installation

### Step 1: Install TA-Lib Wheel
TA-Lib is a C-based library that requires a pre-compiled wheel for easy installation, as building from source can be complex. Download the appropriate wheel file for your Python version and operating system from the [TA-Lib wheel repository](https://github.com/cgohlke/talib-build/releases).

Example wheels:
- For Python 3.13 on Windows (64-bit): `ta_lib-0.6.4-cp313-cp313-win_amd64.whl`
- For other platforms/versions, select the matching file (e.g., for macOS or Linux).

Install the wheel using pip:

```bash
pip install path/to/ta_lib-<version>-<python_version>-<platform>.whl
```

Note: If you're on a non-Windows platform, you may need to install build dependencies (e.g., `brew install ta-lib` on macOS or `apt-get install libta-lib0 libta-lib0-dev` on Ubuntu) before using a wheel or building from source. Refer to the [TA-Lib documentation](https://ta-lib.org/) for details.

### Step 2: Install the Indicators Package
Clone the repository and install the package using pip:

```bash
git clone https://github.com/yourusername/ai-trading-indicators.git
cd ai-trading-indicators
pip install .
```

Alternatively, if you have the project files locally:

```bash
pip install /path/to/ai-trading-indicators
```

This will install the dependencies: `pandas`, `numpy`, and `ta-lib`.

## Quick Start

### Command-Line Interface (CLI)
Run the CLI in interactive mode to select folders and files:

```bash
indicators
```

- You'll be prompted for the input data folder (default: `./data`).
- Select a CSV file or process all files.
- Output will be saved to a folder named `<input_folder>_ind/` (e.g., `data_ind/`).

Direct mode example (process a specific file):

```bash
indicators --input-folder /path/to/data --output-folder /path/to/output --file AAPL.csv
```

If `--file` is omitted in direct mode, all CSV files in the input folder will be processed.

### Programmatic API
Use the API in your Python scripts:

```python
from ind import IndicatorProcessor

processor = IndicatorProcessor()
processor.load_data("path/to/data.csv")
processor.add_default_indicators()  # Adds SMA, EMA, and Bollinger Bands
processor.save_results("output/folder/")
```

Custom indicators example:

```python
processor.add_indicator("SMA", periods=[20, 50])
processor.add_indicator("EMA", periods=[12, 26])
processor.add_indicator("BOLLINGER", period=20, std_dev=2)
```

## Data Format

### Input CSV Format
The CSV must follow this order-sensitive column structure (headers can be anything, but positions matter):

- Column 1: Ignored (any content).
- Column 2: Datetime (timestamp).
- Column 3: Adj Close.
- Column 4: Close.
- Column 5: High.
- Column 6: Low.
- Column 7: Open.
- Column 8: Volume.

Duplicates in the Datetime column are automatically removed (keeping the last entry).

### Output
- Original data is preserved.
- Indicators are appended as new columns (e.g., `SMA_5`, `EMA_20`, `BB_Upper`).
- Files are saved with the original ticker name (e.g., `AAPL.csv`).

## Default Indicators

- **Simple Moving Average (SMA)**: Periods 5, 10, 14, 20, 50, 100, 200 (columns: `SMA_[period]`).
- **Exponential Moving Average (EMA)**: Periods 5, 10, 14, 20, 50, 100, 200 (columns: `EMA_[period]`).
- **Bollinger Bands**: Period 20, Std Dev 2 (columns: `BB_Upper`, `BB_Middle`, `BB_Lower`).

## File System Organization

- Input: Place CSV files in a folder (e.g., `data/AAPL.csv`).
- Output: Automatically created as `<input_folder>_ind/` with processed files.

## Troubleshooting

- **TA-Lib Not Found**: Ensure the wheel is installed correctly for your Python version and platform. Verify with `import talib` in Python.
- **CSV Format Errors**: Check column order and data types. The first column is ignored, but others must match the spec.
- **Large Files**: The package uses efficient Pandas operations, but very large datasets may require more memory.
- **Permissions**: Ensure write access to the output folder.
- If issues persist, check the console for error messages or refer to the TA-Lib wheel repository for compatibility notes.

## Contributing

Contributions are welcome! Please submit issues or pull requests on the [GitHub repository](https://github.com/yourusername/ai-trading-indicators).

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

Robert Boivin (poivronjaune@gmail.com)