# Caminho do arquivo
input_file = 'output2.json'
output_file = 'output2_tratado.json'

# Tamanho do chunk
chunk_size = 10000

# Contador de linhas processadas
line_number = 0

# Abrir o arquivo de entrada e saída
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    # Processar o arquivo em chunks
    while True:
        # Ler o próximo chunk de linhas
        lines = infile.readlines(chunk_size)
        if not lines:  # Terminar se não houver mais linhas
            break

        # Processar o chunk
        for line in lines:
            # Adicionar vírgula ao final de cada linha
            line = line.rstrip() + ',\n'
            outfile.write(line)
            line_number += 1

print(f"Processamento concluído! Total de linhas processadas: {line_number}")
print(f"Arquivo modificado salvo em: {output_file}")
