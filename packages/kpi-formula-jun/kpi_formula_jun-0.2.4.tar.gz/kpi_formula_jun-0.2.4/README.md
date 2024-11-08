# KPI Formula

A Python package for KPI (Key Performance Indicator) calculations and data processing.

## Installation

You can install the package using pip:

bash
pip install kpi-formula


## Usage

Here's a simple example of how to use the package:

python
from kpi_formula.core.data_manager import DataManager
Initialize data manager
manager = DataManager()
Import CSV data
data = manager.import_csv('data/sales.csv')
View the data
print(f"Headers: {data.headers}")
print("First few rows:")
for row in data.data[:3]:
print(row)


## Features

- CSV data import and export
- Data processing and calculations
- Table joins and merges
- Expression evaluation
- Operation history tracking

## Requirements

- Python >= 3.7
- pandas >= 1.0.0
- numpy >= 1.18.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Your Name (your.email@example.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.