import pandas as pd

# Caminho do arquivo CSV
csv_file = 'whatsapp_msgs_2023-08-01_2023-12-31.csv'

# Caminho para salvar o arquivo JSON
json_file = 'output.json'

# Tamanho do chunk (quantidade de linhas processadas por vez)
chunksize = 10000  

# Tipos de dados (ajuste conforme suas necessidades)
dtypes = {
    "media_type": "str",
    "phash": "str",
    "checksum": "str",
    "stored_filename": "str",
    "message_id": "str",
    "text": "str",
    "sender": "str",
    "country_code": "str",
    "ddd_code": "str",
    "group_id": "str",
    "group_name": "str",
    "date": "str",
    "forwarded": "str",
    "is_quote": "str",
    "message_type": "str"
}

# Abrir o arquivo JSON para escrita
with open(json_file, 'w') as json_output:
    for i, chunk in enumerate(pd.read_csv(csv_file, delimiter=';', dtype=dtypes, chunksize=chunksize)):
        # Converter o chunk para JSON
        chunk.to_json(json_output, orient='records', lines=True, force_ascii=False)
        print(f"Chunk {i+1} processado e salvo no JSON.")

print(f"Conversão concluída! Arquivo JSON salvo em: {json_file}")
