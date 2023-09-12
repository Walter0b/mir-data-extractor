# MIR File Data Extractor

The **MIR File Data Extractor** is a Python script designed to automate the extraction and processing of data from `.MIR` files. It interacts with a web-based interface to parse JSON data from these files and provides detailed information about each file's content and any encountered issues.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Overview

This script automates the extraction of JSON data from `.MIR` files using a web-based interface. It is designed to process files within specific folders located in the parent directory, where the folder names should start with "Mir". The script logs data collection details and any issues encountered during the extraction process.

## Requirements

- Python 3.x
- Selenium library (install using `pip install selenium`)
- Firefox web browser or Google chrome (for WebDriver support)

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/mir-file-data-extractor.git
   cd mir-file-data-extractor
   ```

2. Install the required dependencies:

   ```bash
   pip install selenium
   ```

3. Ensure you have the Firefox web browser installed, as the script uses the Firefox WebDriver.

4. Place the folders containing .MIR files in the parent directory. Folder names must start with "Mir".

5. Run the script:

   ```bash
   python mir_data_extractor.py
   ```

   Follow the on-screen prompts, and the script will process the .MIR files, collect data, and log any issues encountered.

## Folder Structure

The script expects the following folder structure:\
project_root/\
│\
├── Mir_Folder_1\
│ ├── file1.MIR\
│ ├── file2.MIR\
│ └── ...\
│\
├── Mir_Folder_2\
│ ├── file1.MIR\
│ ├── file2.MIR\
│ └── ...\
│\
├── ...\
│\
├── mir_data_extractor.py\
│\
└── README.md

Folders containing .MIR files should be located in the root directory of the project, and their names should start with "Mir".

## Results

The script generates output JSON files and issues files for each processed folder. These files are saved in respective output folders named after the processed folders.

JSON output: <folder_name> JSON/<folder_name>.json
Issues output: <folder_name> JSON/Issues.txt

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is distributed under the GNU GENERAL PUBLIC LICENSE. For more information, please see the LICENSE file.
