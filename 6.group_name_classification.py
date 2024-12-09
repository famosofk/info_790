import json

# Palavras-chave para classificação
keywords = {
    "direita": [
        "fora comunistas", "patriotas", "conservador", "liberal", "bolsonaro", "direita", 
        "monarquista", "monarquia", "bolso", "deus", "pátria", "liberdade", "bσℓѕσиαяσ", 
        "luladrão", "ᗷᝪしᔑᝪᑎᗩᖇᝪ", "libertário", "ancap", "anarcocapitalismo", "bolsonaristas"
    ],
    "esquerda": [
        "socialismo", "marx", "progressista", "esquerda", "lula", "povo unido", 
        "venezuela", "amor", "ciro"
    ],
    "neutro": [
        "neutro", "moderado", "centro", "análise política", "debate", "discussão", "política"
    ]
}

def classify_group(group_name):
    """
    Classifica o nome do grupo com base em um sistema de pontuação usando palavras-chave.
    """
    if group_name is None:
        return "indefinido"
    
    # Inicializar as pontuações
    scores = {category: 0 for category in keywords}
    group_name_lower = group_name.lower()  # Converter para minúsculas para comparação
    
    # Calcular a pontuação
    for category, words in keywords.items():
        for word in words:
            if word in group_name_lower:
                scores[category] += 1
    
    # Verificar se houve pontuação
    max_score = max(scores.values())
    if max_score == 0:  # Nenhuma correspondência
        return "indefinido"
    
    # Identificar categorias com maior pontuação
    top_categories = [category for category, score in scores.items() if score == max_score]
    
    # Resolver empates
    if len(top_categories) == 1:
        return top_categories[0]
    elif len(top_categories) == 2:
        if "direita" in top_categories and "esquerda" in top_categories:
            return "neutro"  # Empate entre direita e esquerda
        # Empate entre neutro e outra categoria
        if "neutro" in top_categories:
            return "direita" if "direita" in top_categories else "esquerda"
    
    return "indefinido"  # Caso algum outro cenário ocorra

def classify_groups(input_file, output_file):
    """
    Lê um arquivo JSON, classifica os grupos pelo nome e salva o resultado em outro arquivo JSON.
    """
    try:
        # Ler o arquivo de entrada
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
        
        # Classificar os grupos
        for group in data:
            group["orientation"] = classify_group(group["group_name"])
        
        # Salvar o arquivo de saída
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        
        print(f"Classificação concluída! Dados salvos em '{output_file}'.")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso
input_file = "set_group_id_name.json"  # Substitua pelo caminho do arquivo de entrada
output_file = "grupos_classificados.json"  # Substitua pelo caminho do arquivo de saída

classify_groups(input_file, output_file)
