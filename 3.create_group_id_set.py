import json


def extract_unique_groups_with_counts(input_file, output_file, chunk_size=10000):
    """
    Processa o arquivo JSON em chunks de 10.000, extraindo campos únicos de 'group_id'
    e 'group_name', adicionando um contador de ocorrências para cada 'group_id',
    e salva no arquivo de saída.
    """
    unique_groups = {}

    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
        total_messages = len(data)

        for i in range(0, total_messages, chunk_size):
            chunk = data[i:i + chunk_size]
            for item in chunk:
                group_id = item["group_id"]
                group_name = item["group_name"]
                if group_id not in unique_groups:
                    unique_groups[group_id] = {
                        "group_id": group_id,
                        "group_name": group_name,
                        "count": 0
                    }
                unique_groups[group_id]["count"] += 1

    # Convertendo o dicionário para uma lista de valores únicos
    unique_list = list(unique_groups.values())

    # Salvando no arquivo de saída
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(unique_list, outfile, ensure_ascii=False, indent=4)


input_file = "output2_tratado.json"  # Substitua pelo caminho do arquivo de entrada
output_file = "set_group_id_name.json"  # Substitua pelo caminho do arquivo de saída
extract_unique_groups_with_counts(input_file, output_file)
