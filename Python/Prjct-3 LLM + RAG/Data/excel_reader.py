# Data/excel_reader.py 

import pandas as pd
import os

def load_excel_data(file_name="data.xlsx"):
    """
    Carrega o arquivo Excel e retorna um DataFrame do Pandas.
    O ficheiro excel_reader.py está na pasta Data/, então data.xlsx está ao lado.
    """
    # Define o caminho do ficheiro como sendo no mesmo diretório do script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    try:
        df = pd.read_excel(file_path)
        print(f"✅ DataFrame '{file_name}' carregado com sucesso. {df.shape[0]} linhas.")
        return df
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo não encontrado em: {file_path}")
        return None
    except Exception as e:
        print(f"❌ ERRO ao ler o arquivo Excel: {e}")
        return None