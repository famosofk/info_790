import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Inicializar o analisador de sentimento VADER
analyzer = SentimentIntensityAnalyzer()

# Listas de palavras-chave ampliadas
keywords_politica = [
    # Políticos e ex-políticos
    "bolsonaro", "bozo", "luladrão", "luladrao", "mourão", "lula", "dilma", "pt", "pl", "psdb", "pdt", "candidato", 
    "presidente", "ex-presidente", "governador", "ex-governador", "senador", 
    "ex-senador", "deputado", "ex-deputado", "vereador", "prefeito", "vice-presidente",

    # Eleições e termos relacionados
    "eleição", "urna", "voto", "tse", "fraude", "justiça eleitoral", "recontagem", 
    "campanha", "debate", "propaganda eleitoral", "chapa", "coligação",

    # Política e governo
    "corrupção", "impeachment", "lava jato", "mensalão", "orçamento secreto", 
    "plano de governo", "congresso", "câmara", "senado", "stf", "supremo", 
    "ministro", "reforma administrativa", "reforma tributária",

    # Polêmicas e eventos
    "pandemia", "vacina", "auxílio emergencial", "lockdown", "economia", 
    "inflação", "petrobras", "meio ambiente", "desmatamento", "agro", "combustível", 
    "educação", "amazonas", "indígenas",

    # Ideologias e movimentos
    "direita", "esquerda", "conservador", "progressista", "fascismo", 
    "comunismo", "socialismo", "neoliberalismo", "marxismo", "capitalismo",

    # Termos militares e relacionados a golpes
    "golpe", "intervenção militar", "militar", "exército", "marinha", "aeronáutica", 
    "general", "coronel", "capitão", "major", "tenente", "sargento", "soldado", 
    "quartel", "estado de sítio", "estado de defesa", "comandante", "forças armadas", 
    "ditadura", "AI-5", "regime militar", "movimento militar", "tanques",

    # Termos populares e polêmicos nas redes
    "mito", "comunista", "gado", "golpista", "gabinete do ódio", 
    "fake news", "polarização", "anulação do voto", "traição", "fakenews",
    
    # Outros termos importantes
    "sergio moro", "moro", "paulo guedes", "alexandre de moraes", "moraes", "gilmar mendes"
]

# Função para identificar padrões de linguagem que podem indicar desinformação ou teor político
def detectar_padroes_linguagem(text):
    """Detecta padrões de linguagem que podem indicar desinformação ou teor político."""
    
    # Padrões típicos de teor político
    patterns = {
        "polarizacao": ["nós vs. eles", "os esquerdistas", "os conservadores contra os liberais", "todos contra o governo", "a elite contra o povo"],
        "incitacao_violencia": ["intervenção militar", "ditadura", "golpe", "revolução", "estado de sítio", "fora com todos os corruptos"],
        "teorias_conspiracao": ["fraude nas urnas", "a mídia está controlada", "eles querem nos controlar", "os comunistas estão infiltrados", "o governo esconde a verdade"],
        "falsas_equivalencias": ["Bolsonaro é igual a Hitler", "Lula é igual a Maduro", "o PT é igual ao regime comunista", "os comunistas querem destruir o Brasil"],
    }
    
    # Para cada padrão de linguagem, verificar se a mensagem contém alguma expressão correspondente
    for pattern_type, expressions in patterns.items():
        for expression in expressions:
            if expression.lower() in text.lower():
                return pattern_type
    
    return "comum"

def classificar_mensagem(text):
    """Classifica a mensagem com base em palavras-chave, padrões de linguagem e análise de sentimento."""
    if not text:  # Verificar se o texto é None ou vazio
        return "comum"
    
    # Detecta padrões de linguagem como polarização, incitação à violência, etc.
    padrao_linguagem = detectar_padroes_linguagem(text)
    if padrao_linguagem != "comum":
        return padrao_linguagem
    
    text_lower = text.lower()  # Converter para minúsculas
    keywords_encontradas = [keyword for keyword in keywords_politica if keyword in text_lower]
    
    # Se encontrou palavras-chave, verificar o tom da mensagem
    if keywords_encontradas:
        # Análise de sentimento
        sentiment = analyzer.polarity_scores(text)
        
        # Se o sentimento for positivo, podemos classificar como política positiva
        if sentiment['compound'] > 0.1:  # Um limite positivo para aprovação
            return "política positiva"
        # Se o sentimento for negativo, podemos classificar como política negativa
        elif sentiment['compound'] < -0.1:  # Um limite negativo para desaprovação
            return "política negativa"
        else:
            return "política neutra"  # Caso o sentimento seja neutro
    
    return "comum"

# Ler o arquivo de mensagens
with open('12.mensagens_pre_rotulo.json', 'r', encoding='utf-8') as f:
    mensagens = json.load(f)

# Classificar mensagens
mensagens_classificadas = [
    {
        "text": mensagem["text"],
        "sender": mensagem["sender"],
        "group_id": mensagem["group_id"],
        "categoria": classificar_mensagem(mensagem["text"])
    }
    for mensagem in mensagens
]

# Salvar o arquivo classificado
with open('14.mensagens_classificadas.json', 'w', encoding='utf-8') as f:
    json.dump(mensagens_classificadas, f, ensure_ascii=False, indent=4)

print("Mensagens classificadas automaticamente e salvas em 'mensagens_classificadas.json'.")
