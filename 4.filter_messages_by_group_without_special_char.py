import os
import json
import re

def sanitize_filename(filename):
    """
    Remove ou substitui caracteres inválidos em nomes de arquivos.
    """
    # Substitui caracteres não permitidos por '_'
    sanitized = re.sub(r'[^\w\s-]', '_', filename)
    # Remove espaços extras e os substitui por '_'
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized.strip('_')

def process_messages(input_file):
    # Diretório para salvar os arquivos
    output_dir = "messages_by_group"
    os.makedirs(output_dir, exist_ok=True)

    # Variáveis de controle
    null_group_count = 0
    group_files = {}

    # Lendo o arquivo JSON em chunks
    with open(input_file, 'r', encoding='utf-8') as file:
        messages = json.load(file)
        total_messages = len(messages)

    # Processando em chunks de 10.000
    chunk_size = 10000
    for i in range(0, total_messages, chunk_size):
        chunk = messages[i:i + chunk_size]
        for message in chunk:
            group_name = message.get('group_name')
            if group_name is None:
                null_group_count += 1
            else:
                if group_name not in group_files:
                    group_files[group_name] = []
                group_files[group_name].append(message)

    # Gravando os arquivos por grupo
    for group_name, messages in group_files.items():
        sanitized_name = sanitize_filename(group_name)
        output_file = os.path.join(output_dir, f"{sanitized_name}.json")
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(messages, outfile, ensure_ascii=False, indent=4)

    # Exibindo o número de mensagens com group_name igual a null
    print(f"Quantidade de mensagens com 'group_name' igual a null: {null_group_count}")

# Exemplo de execução
input_file = "output2_tratado.json"  # Nome do arquivo JSON de entrada
process_messages(input_file)
