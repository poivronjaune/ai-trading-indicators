# Indicators Package - Product Requirements Document

## 1. Product Overview

The **Indicators** package is a Python library designed to process financial time-series data stored in CSV files and generate technical indicators using the TA-Lib library. The package provides both a command-line interface for interactive use and a programmatic API for integration into other applications.

## 2. Package Information

- **Package Name**: `indicators`
- **Author**: Robert Boivin
- **Email**: poivronjaune@gmail.com
- **License**: MIT (or as specified in TOML)
- **Python Version**: 3.8+

## 3. Core Features

### 3.1 Data Processing
- Load CSV files containing financial price data
- Support for standardized CSV format with specific column structure
- Pandas DataFrame integration for data manipulation
- Duplicate datetime handling with deduplication logic

### 3.2 Technical Indicators
- Integration with TA-Lib for reliable technical analysis calculations
- Modular indicator system allowing independent calculation
- Default indicator set with commonly used parameters
- Extensible architecture for adding new indicators

### 3.3 User Interfaces
- Interactive command-line interface for folder/file selection
- Programmatic API for integration into other applications
- Progress feedback for command-line operations

### 3.4 File Management
- Organized input/output folder structure
- Automatic output file naming based on source ticker
- Preservation of original data with appended indicators

## 4. Technical Requirements

### 4.1 Dependencies
- **Core Dependencies**:
  - `pandas`: Data manipulation and CSV handling
  - `numpy`: Numerical operations support
  - **TA-Lib**: Technical analysis library (requires wheel installation)
- **Development Dependencies**:
  - Standard Python packaging tools
  - Testing frameworks (pytest recommended)

### 4.2 TA-Lib Installation
- Package requires TA-Lib wheel file installation
- Example wheel: `ta_lib-0.6.4-cp313-cp313-win_amd64.whl`
- Installation via pip tools before package installation
- Platform-specific wheel files required

### 4.3 Configuration
- TOML configuration file for package metadata
- Configurable parameters for indicators
- User preferences storage capability

## 5. Data Format Specifications

### 5.1 Input CSV Format
Required column structure (order-sensitive):
```
Column 1: NotUsed (any content, will be ignored)
Column 2: Datetime (timestamp data)
Column 3: Adj Close (adjusted closing price)
Column 4: Close (closing price)
Column 5: High (high price)
Column 6: Low (low price)
Column 7: Open (opening price)
Column 8: Volume (trading volume)
```

### 5.2 Data Processing Rules
- First column completely ignored (content and header)
- DateTime column must contain unique timestamps
- Duplicate datetime entries automatically removed
- Data loaded into pandas DataFrame for processing

### 5.3 Output Format
- Original data preserved
- Indicators added as additional columns
- Same CSV format maintained
- File saved with original ticker name

## 6. Default Indicators

### 6.1 Moving Averages
- **Simple Moving Average (SMA)**
  - Lookback windows: 5, 10, 14, 20, 50, 100, 200 periods
  - Column naming: `SMA_[period]`
- **Exponential Moving Average (EMA)**
  - Lookback windows: 5, 10, 14, 20, 50, 100, 200 periods
  - Column naming: `EMA_[period]`

### 6.2 Bollinger Bands
- **Standard Parameters**:
  - Period: 20
  - Standard Deviations: 2
- **Output Columns**:
  - `BB_Upper`: Upper band
  - `BB_Middle`: Middle band (SMA)
  - `BB_Lower`: Lower band

## 7. Architecture Requirements

### 7.1 Modular Design
- Independent indicator calculation functions
- Pluggable indicator system
- Easy addition of new indicators
- Configurable parameter sets

### 7.2 API Structure
```python
# Programmatic API example
from indicators import IndicatorProcessor

processor = IndicatorProcessor()
processor.load_data("path/to/data.csv")
processor.add_indicator("SMA", periods=[20, 50])
processor.add_indicator("EMA", periods=[12, 26])
processor.add_indicator("BOLLINGER", period=20, std_dev=2)
processor.save_results("output/folder/")
```

### 7.3 Command Line Interface
```bash
# Interactive mode
python -m indicators

# Direct mode
python -m indicators --input-folder /path/to/data --output-folder /path/to/output --file ticker.csv
```

## 8. File System Organization

### 8.1 Input Structure
```
data/
├── AAPL.csv
├── MSFT.csv
└── GOOGL.csv
```

### 8.2 Output Structure
```
data_ind/
├── AAPL.csv    # Original data + indicators
├── MSFT.csv    # Original data + indicators
└── GOOGL.csv   # Original data + indicators
```

### 8.3 Folder Naming Convention
- Input folder: User-specified or default `data/`
- Output folder: `[input_folder_name]_ind/`
- File names: Preserve original ticker names

## 9. User Experience Requirements

### 9.1 Command Line Interface
- Interactive folder selection dialog
- File selection from available CSV files
- Progress indicators during processing
- Clear error messages and validation feedback
- Success/completion notifications

### 9.2 Error Handling
- Graceful handling of malformed CSV files
- Missing data validation
- TA-Lib installation verification
- File permission and access error handling

### 9.3 Performance Considerations
- Efficient DataFrame operations
- Memory-conscious processing for large files
- Progress reporting for long-running operations

## 10. Installation and Setup

### 10.1 Package Installation
1. Install TA-Lib wheel file (platform-specific)
2. Install indicators package via pip
3. Verify installation with test command

### 10.2 TA-Lib Wheel Installation
Users must download appropriate wheel file from:
**https://github.com/cgohlke/talib-build**

Files are located in the releases section. Choose the appropriate wheel for your Python version and platform.

Example installation:
```bash
pip install ta_lib-0.6.4-cp313-cp313-win_amd64.whl
pip install indicators
```

## 11. Testing Requirements

### 11.1 Unit Tests
- Individual indicator calculation verification
- Data loading and validation tests
- File I/O operation tests
- Error handling validation

### 11.2 Integration Tests
- End-to-end workflow testing
- Command-line interface testing
- API functionality verification

### 11.3 Data Validation
- Sample CSV files for testing
- Expected output verification
- Performance benchmarking

## 12. Documentation Requirements

### 12.1 README File
- Installation instructions including TA-Lib setup
- Quick start guide
- API documentation
- Command-line usage examples
- Link to TA-Lib wheel repository
- Troubleshooting section

### 12.2 Code Documentation
- Docstrings for all public functions
- Type hints where appropriate
- Usage examples in docstrings

## 13. Extensibility

### 13.1 Plugin Architecture
- Easy addition of new indicators
- Custom parameter configuration
- User-defined indicator functions

### 13.2 Configuration Options
- Default indicator sets modification
- Custom parameter presets
- Output format customization

## 14. Quality Assurance

### 14.1 Code Quality
- PEP 8 compliance
- Type checking with mypy
- Linting with flake8 or similar

### 14.2 Reliability
- Robust error handling
- Input validation
- Graceful degradation for edge cases

## 15. Future Enhancements

### 15.1 Potential Features
- Additional technical indicators
- Custom indicator formula support
- Batch processing capabilities
- Performance optimization
- GUI interface option

### 15.2 Integration Possibilities
- REST API wrapper
- Database connectivity
- Real-time data feed integration
- Visualization capabilities

---

## Repository Information

For TA-Lib wheel files, visit: **https://github.com/cgohlke/talib-build**

The required wheel files are located in the releases section. Download the appropriate wheel file for your Python version and operating system before installing this package.