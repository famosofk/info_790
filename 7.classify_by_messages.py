import os
import json
from collections import Counter

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

def classify_message(text):
    """
    Classifica uma mensagem com base em palavras-chave.
    """
    if not text:
        return "indefinido", {category: 0 for category in keywords}
    
    scores = {category: 0 for category in keywords}
    text_lower = text.lower()
    
    for category, words in keywords.items():
        for word in words:
            if word in text_lower:
                scores[category] += 1
    
    # Verificar a maior pontuação
    max_score = max(scores.values())
    if max_score == 0:
        return "indefinido", scores
    
    top_categories = [category for category, score in scores.items() if score == max_score]
    
    # Resolver empates
    if len(top_categories) == 1:
        return top_categories[0], scores
    elif "direita" in top_categories and "esquerda" in top_categories:
        return "neutro", scores
    elif "neutro" in top_categories:
        # Priorizar direita ou esquerda em caso de empate com neutro
        if "direita" in top_categories:
            return "direita", scores
        if "esquerda" in top_categories:
            return "esquerda", scores
    
    return "indefinido", scores

def process_messages_by_group(input_folder, output_file):
    """
    Processa mensagens por grupo, determina a orientação e salva os resultados.
    """
    results = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            group_id = os.path.splitext(filename)[0]
            file_path = os.path.join(input_folder, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    messages = json.load(file)
                
                orientations = Counter()
                total_scores = {category: 0 for category in keywords}
                
                for message in messages:
                    orientation, message_scores = classify_message(message.get("text", ""))
                    orientations[orientation] += 1
                    for category, score in message_scores.items():
                        total_scores[category] += score
                
                # Determinar a orientação final do grupo baseado na maior contagem de mensagens
                most_common = orientations.most_common()
                if not most_common:
                    group_orientation = "indefinido"
                else:
                    primary_orientation, primary_count = most_common[0]
                    if len(most_common) > 1:
                        secondary_orientation, secondary_count = most_common[1]
                        if primary_orientation == "neutro":
                            group_orientation = f"neutro|{secondary_orientation}"
                        else:
                            group_orientation = primary_orientation
                    else:
                        group_orientation = primary_orientation
                
                # Verificar se a orientação final deve ser mais ajustada
                if group_orientation == "indefinido":
                    if total_scores["direita"] > total_scores["esquerda"]:
                        group_orientation = "direita"
                    elif total_scores["esquerda"] > total_scores["direita"]:
                        group_orientation = "esquerda"
                    else:
                        group_orientation = "neutro"
                
                # Adicionar ao resultado com as pontuações
                results.append({
                    "group_id": group_id,
                    "orientation": group_orientation,
                    "scores": total_scores  # Incluindo as pontuações no resultado
                })
            
            except Exception as e:
                print(f"Erro ao processar o arquivo {filename}: {e}")
    
    # Salvar os resultados em um arquivo JSON
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(results, outfile, indent=4, ensure_ascii=False)
        print(f"Resultados salvos em '{output_file}'.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo de saída: {e}")

# Caminho da pasta de entrada e do arquivo de saída
input_folder = "messages_by_group_id"
output_file = "messages_by_group_evaluated.json"

process_messages_by_group(input_folder, output_file)
