import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import sys

input_filepath = input("Input filepath name:")
print(input_filepath)
output_filepath = input("Output filepath name:")
print(output_filepath)

def read_csv(filepath):
    """Reads a CSV file into a pandas DataFrame, converting all fields to strings to avoid .0 suffixes."""
    df = pd.read_csv(filepath)
    print(df.head())
    int_fields = ['client_number', 'account', 'client_number_target', 'account_target']
    for field in int_fields:
        # Apply a lambda to convert non-NaN values to integer, NaNs are converted to empty string
        df[field] = df[field].apply(lambda x: str(int(x)) if pd.notna(x) else '')
    df = df.astype(str).replace('nan', '')
    return df

def create_xml_element(row):
    """Creates and returns an XML element for a given transaction row."""
    transaction = ET.Element('transaction')
    ET.SubElement(transaction, 'transactionnumber').text = str(row['transactionnumber'])
    ET.SubElement(transaction, 'date_transaction').text = str(row['date_transaction'])
    ET.SubElement(transaction, 'transmode_code').text = str(row['transmode_code'])
    ET.SubElement(transaction, 'amount_local').text = str(row['amount_local'])
    
    transmode_code = row['transmode_code']
    
    if transmode_code in ['KRMDN', 'PGNDN', 'TARIK', 'INTER']:
        t_from_my_client = ET.SubElement(transaction, 't_from_my_client')
        ET.SubElement(t_from_my_client, 'from_funds_code').text = str(row['from_funds_code'])

        from_account = ET.SubElement(t_from_my_client, 'from_account')
        ET.SubElement(from_account, 'institution_name').text = str(row['institution_name'])
        ET.SubElement(from_account, 'institution_code').text = str(row['institution_code'])
        ET.SubElement(from_account, 'branch').text = str(row['branch'])
        ET.SubElement(from_account, 'account').text = str(row['account'])
        ET.SubElement(from_account, 'currency_code').text = str(row['currency_code'])
        ET.SubElement(from_account, 'client_number').text = str(row['client_number'])
        ET.SubElement(from_account, 'account_type').text = str(row['account_type'])
        ET.SubElement(from_account, 'opened').text = str(row['opened'])
        
        ET.SubElement(t_from_my_client, 'from_country').text = str(row['from_country'])

    if transmode_code in ['KRMDN', 'PGNDN', 'TARIK']:
        t_to = ET.SubElement(transaction, 't_to')
        ET.SubElement(t_to, 'to_funds_code').text = str(row['to_funds_code'])
        
        to_entity = ET.SubElement(t_to, 'to_entity')
        ET.SubElement(to_entity, 'name').text = str(row['name_target'])

        ET.SubElement(t_to, 'to_country').text = str(row['to_country'])
    
    elif transmode_code == 'INTER':
        t_to_my_client = ET.SubElement(transaction, 't_to_my_client')
        ET.SubElement(t_to_my_client, 'to_funds_code').text = str(row['to_funds_code'])

        to_account = ET.SubElement(t_to_my_client, 'to_account')
        ET.SubElement(to_account, 'institution_name').text = str(row['institution_name_target'])
        ET.SubElement(to_account, 'institution_code').text = str(row['institution_code_target'])
        ET.SubElement(to_account, 'branch').text = str(row['branch_target'])
        ET.SubElement(to_account, 'account').text = str(row['account_target'])
        ET.SubElement(to_account, 'currency_code').text = str(row['currency_code_target'])
        ET.SubElement(to_account, 'client_number').text = str(row['client_number_target'])
        ET.SubElement(to_account, 'account_type').text = str(row['account_type_target'])
        ET.SubElement(to_account, 'opened').text = str(row['opened_target'])

        ET.SubElement(t_to_my_client, 'to_country').text = str(row['to_country'])
    
    elif transmode_code == 'TRMDN':
        t_from = ET.SubElement(transaction, 't_from')
        ET.SubElement(t_from, 'from_funds_code').text = str(row['from_funds_code'])

        from_entity = ET.SubElement(t_from, 'from_entity')
        ET.SubElement(from_entity, 'name').text = str(row['name'])

        ET.SubElement(t_from, 'from_country').text = str(row['from_country'])

        t_to_my_client = ET.SubElement(transaction, 't_to_my_client')
        ET.SubElement(t_to_my_client, 'to_funds_code').text = str(row['to_funds_code'])

        to_account = ET.SubElement(t_to_my_client, 'to_account')
        ET.SubElement(to_account, 'institution_name').text = str(row['institution_name_target'])
        ET.SubElement(to_account, 'institution_code').text = str(row['institution_code_target'])
        ET.SubElement(to_account, 'branch').text = str(row['branch_target'])
        ET.SubElement(to_account, 'account').text = str(row['account_target'])
        ET.SubElement(to_account, 'currency_code').text = str(row['currency_code_target'])
        ET.SubElement(to_account, 'client_number').text = str(row['client_number_target'])
        ET.SubElement(to_account, 'account_type').text = str(row['account_type_target'])
        ET.SubElement(to_account, 'opened').text = str(row['opened_target'])

        ET.SubElement(t_to_my_client, 'to_country').text = str(row['to_country'])
    
    else:
        # source
        t_from_my_client = ET.SubElement(transaction, 't_from_my_client')
        ET.SubElement(t_from_my_client, 'from_funds_code').text = str(row['from_funds_code'])

        from_account = ET.SubElement(t_from_my_client, 'from_account')
        
        ET.SubElement(from_account, 'institution_name').text = str(row['institution_name'])
        ET.SubElement(from_account, 'institution_code').text = str(row['institution_code'])
        ET.SubElement(from_account, 'branch').text = str(row['branch'])
        ET.SubElement(from_account, 'account').text = str(row['account'])
        ET.SubElement(from_account, 'currency_code').text = str(row['currency_code'])
        ET.SubElement(from_account, 'client_number').text = str(row['client_number'])
        ET.SubElement(from_account, 'account_type').text = str(row['account_type'])
        ET.SubElement(from_account, 'opened').text = str(row['opened'])
        
        ET.SubElement(t_from_my_client, 'from_country').text = str(row['from_country'])

        # target name
        t_to = ET.SubElement(transaction, 't_to')
        ET.SubElement(t_to, 'to_funds_code').text = str(row['to_funds_code'])
        
        to_entity = ET.SubElement(t_to, 'to_entity')

        ET.SubElement(t_to, 'to_country').text = str(row['to_country'])

        # source name
        t_from = ET.SubElement(transaction, 't_from')
        ET.SubElement(t_from, 'from_funds_code').text = str(row['from_funds_code'])

        from_entity = ET.SubElement(t_from, 'from_entity')

        ET.SubElement(t_from, 'from_country').text = str(row['from_country'])

        # target
        t_to_my_client = ET.SubElement(transaction, 't_to_my_client')
        ET.SubElement(t_to_my_client, 'to_funds_code').text = str(row['to_funds_code'])

        to_account = ET.SubElement(t_to_my_client, 'to_account')

        ET.SubElement(to_account, 'institution_name').text = str(row['institution_name_target'])
        ET.SubElement(to_account, 'institution_code').text = str(row['institution_code_target'])
        ET.SubElement(to_account, 'branch').text = str(row['branch_target'])
        ET.SubElement(to_account, 'account').text = str(row['account_target'])
        ET.SubElement(to_account, 'currency_code').text = str(row['currency_code_target'])
        ET.SubElement(to_account, 'client_number').text = str(row['client_number_target'])
        ET.SubElement(to_account, 'account_type').text = str(row['account_type_target'])
        ET.SubElement(to_account, 'opened').text = str(row['opened_target'])

        ET.SubElement(t_to_my_client, 'to_country').text = str(row['to_country'])
    
    return transaction

def convert_to_xml(df):
    """Converts a DataFrame to an XML structure and returns the ElementTree."""
    root = ET.Element('report')
    for _, row in df.iterrows():
        root.append(create_xml_element(row))
    return ET.ElementTree(root)

def save_xml(tree, output_path):
    xml_str = ET.tostring(tree.getroot(), 'utf-8')
    dom = parseString(xml_str)
    with open(output_path, 'w') as output_file:
        output_file.write(dom.toprettyxml(indent="    "))  # Using four spaces for indentation

def main():
    # if len(sys.argv) != 3:
    #     print("Usage: script.exe <input_filepath> <output_filepath>")
    #     sys.exit(1)

    # input_filepath = sys.argv[1]
    # output_filepath = sys.argv[2]

    df = read_csv(input_filepath)

    max_items_per_file = 10000  # Maximum number of items per file
    num_rows = len(df)
    start_index = 0
    part_number = 1

    while start_index < num_rows:
        root = ET.Element('report')
        end_index = min(start_index + max_items_per_file, num_rows)

        for i in range(start_index, end_index):
            row = df.iloc[i]
            root.append(create_xml_element(row))

        xml_tree = ET.ElementTree(root)
        chunk_output_filepath = f"{output_filepath.rsplit('.', 1)[0]}_part_{part_number}.xml"
        save_xml(xml_tree, chunk_output_filepath)
        part_number += 1
        start_index = end_index

    print("XML file has been created successfully.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        print("An error occurred:", e)
        traceback.print_exc()
    input('finished. press enter to continue...')