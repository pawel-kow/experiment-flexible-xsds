# XML Schema Validator

## Description

This project contains a Python script (`test_schemas.py`) that automatically validates a collection of XML files against a set of XML Schema Definitions (XSDs).

The script performs the following actions:
1.  Discovers all schema directories within the `./schemas` folder.
2.  Loads the `main.xsd` file from each schema directory, automatically including any imported XSDs in the same folder.
3.  Finds all XML files located in the `./data_examples` folder.
4.  For each XML file, it validates the file against every loaded schema.
5.  Prints a detailed, step-by-step log of the process to the console, including the content of each XML file being processed.
6.  Saves a summary of the validation results to a file at `./results/results.txt`.

## Setup and Installation

### Prerequisites
- Python 3.6+

### Instructions

1.  **Clone the repository or download the source code.**

2.  **Create a virtual environment.**
    It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.

    Navigate to the project's root directory in your terminal and run the following command to create a virtual environment named `venv`:

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment.**

    -   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **On macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```
    Your terminal prompt should now be prefixed with `(venv)`, indicating that the virtual environment is active.

4.  **Install the required packages.**
    A `requirements.txt` file is included to manage the necessary Python libraries. Install them using pip:

    ```bash
    pip install -r requirements.txt
    ```
    This will install the `xmlschema` library required by the script.

## Directory Structure

The project expects the following directory structure to function correctly:

```
.
├── schemas/
│   ├── schema_one/
│   │   ├── main.xsd
│   │   └── other_definitions.xsd  (optional, imported by main.xsd)
│   └── schema_two/
│       └── main.xsd
├── data_examples/
│   ├── data1.xml
│   └── data2.xml
├── results/
│   └── results.txt              (this is generated by the script)
├── test_schemas.py              (the main script)
└── requirements.txt
```

-   `./schemas`: Contains subdirectories for each schema definition.
-   `./data_examples`: Contains the XML files that need to be validated.
-   `./results`: The output directory where the results file is stored.

## Usage

With the virtual environment activated and dependencies installed, run the script from the project's root directory:

```bash
python test_schemas.py
```

The script includes a function to create dummy files and folders for a demonstration. You can disable this in the if __name__ == "__main__": block if you are using your own schemas and data files.

Output
The script provides two forms of output:

Console Output: A real-time log of the validation process. It details which schemas are being loaded, which XML file is being validated, the content of that XML file, and the success or failure result for each validation check.

Results File: A summary of the validation results is saved to ./results/results.txt. This file provides a clean, machine-readable JSON format for the results of each file against each schema.

Example results.txt content:

```
FILE: user1.xml
{
  "product_catalog": "FAIL",
  "user_profile": "SUCCESS"
}

FILE: product1.xml
{
  "product_catalog": "SUCCESS",
  "user_profile": "FAIL"
}
```
