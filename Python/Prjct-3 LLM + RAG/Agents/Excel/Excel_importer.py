import pandas as pd
import os
from typing import List, Dict, Any

from CRUD.Create import add_new_client 

EXCEL_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'data.xlsx')


def import_excel_to_db(excel_file_path: str = EXCEL_FILE_PATH) -> str:
    """
    Reads an Excel file and imports the data from each row as a new client 
    into the database, mapping the available columns.
    
    The function uses the explicit column names found in the Excel image.
    """
    if not os.path.exists(excel_file_path):
        # Dispara FileNotFoundError para que a rota Flask possa apanhar o erro 404
        raise FileNotFoundError(f"Excel file not found at path: {excel_file_path}")
        
    try:
        # Reads the Excel file into a DataFrame
        df = pd.read_excel(excel_file_path)
        
        total_rows = len(df)
        success_count = 0
        failure_details = []
        
        # Iterates over the DataFrame rows
        for index, row in df.iterrows():
            try:
                # ----------------------------------------------------
                # ADAPTAÇÃO: Mapeamento de Colunas (Usando os nomes exatos da imagem)
                # ----------------------------------------------------
                name = row.get('Nome')
                email = row.get('Email')
                
                # Campos de Contacto e Morada
                phone = row.get('Telefone')
                address = row.get('Morada') 
                
                # Interesse e Notas (usado para o campo 'interest' e 'notes' no DB/CRUD)
                interest = row.get('Interesse')
                notes = row.get('Notas') # NOVO: Mapeado para o argumento 'notes'
                
                # Outras colunas ignoradas pois não há argumento correspondente em add_new_client:
                # 'Data de Registo', 'Última Compra', 'Valor Gasto (€)'
                
                # ----------------------------------------------------

                if not name or not email or not interest:
                    failure_details.append(f"Row {index + 2}: Validation failed (name, email, or interest missing).")
                    continue
                
                # Calls the CRUD function to add the client
                result = add_new_client(
                    name=str(name),
                    email=str(email),
                    interest=str(interest),
                    # Garante que None é passado se o valor for nulo
                    phone=str(phone) if pd.notna(phone) else None, 
                    address=str(address) if pd.notna(address) else None,
                    # REMOVIDO: notes=str(notes) if pd.notna(notes) else None 
                )
                
                if "Success!" in result:
                    success_count += 1
                else:
                    failure_details.append(f"Row {index + 2}: Database failure ({result}).")

            except Exception as e:
                failure_details.append(f"Row {index + 2}: Unexpected error during insertion: {str(e)}")

        if success_count == total_rows:
            return f"SUCCESS: {success_count} clients imported successfully out of {total_rows} rows."
        else:
            return (
                f"IMPORT COMPLETE: {success_count} clients added. "
                f"{total_rows - success_count} failures found. Details: {'; '.join(failure_details[:5])}..."
            )

    except FileNotFoundError as e:
        raise e 
    except Exception as e:
        return f"FATAL ERROR: Failed to read the Excel file. Verify that pandas and openpyxl are installed. Detail: {str(e)}"

# If the user does not specify a path, the default is used.
def import_default_excel_to_db() -> str:
    return import_excel_to_db()