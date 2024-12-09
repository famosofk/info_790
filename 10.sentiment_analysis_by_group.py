import os
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment_in_files(input_folder, output_file):
    """
    Processa arquivos JSON em uma pasta, realiza análise de sentimento no campo 'text'
    e gera um arquivo consolidado com contagens por 'group_id'.
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiment_summary = []

    # Iterar pelos arquivos na pasta
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(input_folder, filename)

            with open(filepath, 'r', encoding='utf-8') as infile:
                data = json.load(infile)

            # Inicializar contadores para o grupo atual
            group_id = data[0]["group_id"] if data else "unknown"
            sentiment_counts = {"group_id": group_id, "neg": 0, "neu": 0, "pos": 0}

            # Analisar sentimento de cada mensagem
            for item in data:
                text = item.get("text", "")
                if text:  # Ignorar mensagens sem texto
                    scores = analyzer.polarity_scores(text)
                    if scores["compound"] >= 0.05:
                        sentiment_counts["pos"] += 1
                    elif scores["compound"] <= -0.05:
                        sentiment_counts["neg"] += 1
                    else:
                        sentiment_counts["neu"] += 1

            # Adicionar resultados do grupo ao resumo final
            sentiment_summary.append(sentiment_counts)

    # Salvar resultados consolidados em um arquivo
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(sentiment_summary, outfile, ensure_ascii=False, indent=4)

# Configuração de entrada e saída
input_folder = "messages_by_group_id"  # Pasta com os arquivos JSON
output_file = "sentiment_summary.json"  # Arquivo consolidado de saída

analyze_sentiment_in_files(input_folder, output_file)