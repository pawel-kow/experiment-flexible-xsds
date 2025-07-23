import os
from xml.etree import ElementTree
import xmlschema
import json

# --- Configuration ---
SCHEMAS_DIR = './schemas'
DATA_DIR = './data_examples'
RESULTS_DIR = './results'

def create_dummy_files():
    """Creates dummy folders and files for demonstration purposes."""
    print("--- Setting up demonstration directories and files ---")

    # Create schema directories and files
    os.makedirs(os.path.join(SCHEMAS_DIR, 'user_profile'), exist_ok=True)
    os.makedirs(os.path.join(SCHEMAS_DIR, 'product_catalog'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR), exist_ok=True)

    # Schema for user_profile
    user_profile_xsd = """
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
      <xs:element name="user">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="name" type="xs:string"/>
            <xs:element name="email" type="xs:string"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:schema>
    """
    with open(os.path.join(SCHEMAS_DIR, 'user_profile', 'main.xsd'), 'w') as f:
        f.write(user_profile_xsd)

    # Schema for product_catalog
    product_catalog_xsd = """
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
      <xs:element name="product">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="id" type="xs:integer"/>
            <xs:element name="name" type="xs:string"/>
            <xs:element name="price" type="xs:decimal"/>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
    </xs:schema>
    """
    with open(os.path.join(SCHEMAS_DIR, 'product_catalog', 'main.xsd'), 'w') as f:
        f.write(product_catalog_xsd)

    # Valid user XML
    valid_user_xml = """
    <user>
      <name>John Doe</name>
      <email>john.doe@example.com</email>
    </user>
    """
    with open(os.path.join(DATA_DIR, 'user1.xml'), 'w') as f:
        f.write(valid_user_xml)

    # Valid product XML
    valid_product_xml = """
    <product>
      <id>123</id>
      <name>Laptop</name>
      <price>1200.50</price>
    </product>
    """
    with open(os.path.join(DATA_DIR, 'product1.xml'), 'w') as f:
        f.write(valid_product_xml)

    # Invalid XML (will fail against both schemas)
    invalid_xml = """
    <customer>
      <name>Jane Smith</name>
    </customer>
    """
    with open(os.path.join(DATA_DIR, 'invalid_data.xml'), 'w') as f:
        f.write(invalid_xml)

    print("--- Setup complete ---\n")


def validate_xml_files():
    """
    Lists schemas, finds XML files, and validates them against the schemas.
    """
    # --- 1. List all schema directories ---
    print(f"--- Step 1: Discovering schemas in '{SCHEMAS_DIR}' ---")
    try:
        schema_folders = sorted([d for d in os.listdir(SCHEMAS_DIR) if os.path.isdir(os.path.join(SCHEMAS_DIR, d))])
        if not schema_folders:
            print(f"Result: FAIL - No directories found in '{SCHEMAS_DIR}'. Please create schema folders.")
            return
        print(f"Found schema folders: {schema_folders}\n")
    except FileNotFoundError:
        print(f"Result: FAIL - The directory '{SCHEMAS_DIR}' was not found.")
        return

    # --- 2. Load all schemas ---
    print("--- Step 2: Loading all XSD schemas ---")
    schemas = {}
    for folder in schema_folders:
        schema_path = os.path.join(SCHEMAS_DIR, folder, 'main.xsd')
        print(f"Input: Attempting to load schema from '{schema_path}'")
        if os.path.exists(schema_path):
            try:
                # The xmlschema library automatically handles <xs:import> statements
                # as long as the referenced files are in the same directory.
                schema = xmlschema.XMLSchema(schema_path, validation="lax")
                schemas[folder] = schema
                print(f"Result: SUCCESS - Schema '{folder}' loaded.\n")
            except Exception as e:
                print(f"Result: FAIL - Could not parse schema '{schema_path}'. Error: {e}\n")
        else:
            print(f"Result: FAIL - 'main.xsd' not found in '{folder}'.\n")

    if not schemas:
        print("--- Validation Aborted: No valid schemas were loaded. ---")
        return

    # --- 3. List all XML data files ---
    print(f"--- Step 3: Discovering XML files in '{DATA_DIR}' ---")
    try:
        xml_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.xml')]
        if not xml_files:
            print(f"Result: FAIL - No XML files found in '{DATA_DIR}'.")
            return
        print(f"Found XML files: {xml_files}\n")
    except FileNotFoundError:
        print(f"Result: FAIL - The directory '{DATA_DIR}' was not found.")
        return

    results = {}

    # --- 4. Validate each XML file against each schema ---
    print("--- Step 4: Starting validation process ---")
    for xml_file in xml_files:
        xml_path = os.path.join(DATA_DIR, xml_file)
        print(f"\n----- Validating XML File: {xml_file} -----")
        
        results[xml_file] = {}
        
        # Read and print the content of the XML file
        try:
            with open(xml_path, 'r') as f:
                xml_content = f.read()
                print(f"--- Content of '{xml_file}' ---")
                print(xml_content.strip())
                print("--------------------------\n")
        except Exception as e:
            results[xml_file] = "Error reading"
            print(f"Error reading file '{xml_path}': {e}")
            continue
        
        try:
            # Basic check to see if file is well-formed XML
            ElementTree.parse(xml_path)
        except ElementTree.ParseError as e:
            print(f"Input: '{xml_path}'")
            print("Output: This file is not well-formed XML and cannot be validated.")
            print(f"Result: FAIL - XML Parse Error: {e}")
            results[xml_file] = "Error parsing XML"
            continue # Skip to the next file

        # Iterate through schemas in the alphabetical order of their containing folder names
        for schema_name in sorted(schemas.keys()):
            schema_instance = schemas[schema_name]
            print(f"\nInput: '{xml_path}'")
            print(f"Schema: '{schema_name}' (from {schema_instance.filepath})")
            try:
                schema_instance.validate(xml_path)
                print("Result: SUCCESS - XML is valid against this schema.")
                results[xml_file][schema_name] = "SUCCESS"
            except Exception as e:
                # Providing a snippet of the error for clarity
                error_message = str(e).split('\n')[0]
                print(f"Result: FAIL - XML is not valid against this schema. Reason: {error_message}")
                results[xml_file][schema_name] = f"FAIL"

    # --- 5. Output results to console and file ---
    print("\n\n**** RESULTS ****\n")

    # Create results directory if it doesn't exist
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results_filepath = os.path.join(RESULTS_DIR, 'results.txt')

    print(f"--- Writing detailed results to {results_filepath} ---")
    
    with open(results_filepath, 'w') as f:
        for file in sorted(results.keys()):
            # Print to console
            print(f"FILE: {file}")
            print(json.dumps(results[file], indent=2))
            
            # Write to file
            f.write(f"FILE: {file}\n")
            f.write(json.dumps(results[file], indent=2) + "\n\n")

    print(f"\n--- Results successfully written to {results_filepath} ---")


if __name__ == "__main__":
    # First, create the necessary files and folders for the script to run.
    # In a real scenario, you would remove this function call.
    # create_dummy_files()

    # Now, run the validation logic.
    validate_xml_files()
