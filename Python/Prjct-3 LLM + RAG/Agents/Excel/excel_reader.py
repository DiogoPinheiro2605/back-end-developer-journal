import pandas as pd
from pathlib import Path
import os
# The excel_reader.py file is in the Data/ folder

def load_excel_data(file_name="../../Data/data.xlsx"):
    """
    Loads the Excel file using Pathlib to ensure the file path is calculated 
    from the location of excel_reader.py itself.
    """
    # 1. Finds the current directory of excel_reader.py (which should be 'Data' or a subfolder)
    current_dir = Path(__file__).resolve().parent
    
    # 2. Constructs the absolute path to the data file
    # Path: Data / data.xlsx
    file_path = current_dir / file_name

    if not file_path.exists():
        # If the file is not there (e.g., if it's being run from 'Agents/Excel'),
        # we can try searching from the root, but the practice is to keep data.xlsx in 'Data/'.
        print(f"❌ ERROR: Data file not found at: {file_path}")
        return None

    try:
        df = pd.read_excel(file_path)
        # The agent needs the exact column name
        # Ensure the name 'Valor Gasto' is correct
        if 'Valor Gasto (€)' in df.columns:
            df.rename(columns={'Valor Gasto (€)': 'Valor Gasto'}, inplace=True)
            
        print(f"✅ Data loaded successfully from: {file_path}")
        return df
    except Exception as e:
        print(f"❌ ERROR loading Excel: {e}")
        return None