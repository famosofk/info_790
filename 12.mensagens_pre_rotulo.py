import json

# Nome dos arquivos
arquivo_entrada = '2.output2_tratado.json'
arquivo_saida = '12.mensagens_pre_rotulo.json'

# Ler o arquivo JSON de entrada
with open(arquivo_entrada, 'r', encoding='utf-8') as f:
    mensagens = json.load(f)

# Filtrar e criar o novo objeto com os campos desejados
mensagens_filtradas = [
    {"text": mensagem["text"], "sender": mensagem["sender"], "group_id": mensagem["group_id"]}
    for mensagem in mensagens
    if mensagem['media_type'] == 'text' and mensagem['text'] != 'None'
]

# Salvar o novo arquivo JSON
with open(arquivo_saida, 'w', encoding='utf-8') as f:
    json.dump(mensagens_filtradas, f, ensure_ascii=False, indent=4)

print(f"Arquivo '{arquivo_saida}' criado com sucesso!")
