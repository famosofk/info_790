import json

def compare_orientations(file1, file2):
    """
    Compara as orientações dos grupos presentes nos dois arquivos JSON.
    """
    try:
        # Carregar os dois arquivos
        with open(file1, 'r', encoding='utf-8') as f1:
            groups_evaluated = json.load(f1)
        
        with open(file2, 'r', encoding='utf-8') as f2:
            groups_classified = json.load(f2)
        
        # Criar dicionário de orientações a partir do segundo arquivo (grupos_classificados)
        classified_dict = {group["group_id"]: group["orientation"] for group in groups_classified}
        
        # Comparar as orientações
        differences = []
        
        for group in groups_evaluated:
            group_id = group["group_id"]
            evaluated_orientation = group["orientation"]
            classified_orientation = classified_dict.get(group_id)
            
            if classified_orientation != evaluated_orientation:
                differences.append({
                    "group_id": group_id,
                    "evaluated_orientation": evaluated_orientation,
                    "classified_orientation": classified_orientation
                })
        
        if differences:
            print(f"Encontradas diferenças em {len(differences)} grupos:")
            for diff in differences:
                print(f"Group ID: {diff['group_id']}")
                print(f"  Orientação Avaliada: {diff['evaluated_orientation']}")
                print(f"  Orientação Classificada: {diff['classified_orientation']}")
        else:
            print("Nenhuma diferença encontrada entre as orientações dos grupos.")
    
    except Exception as e:
        print(f"Erro ao comparar os arquivos: {e}")

# Caminhos dos arquivos
file1 = 'messages_by_group_evaluated.json'
file2 = 'grupos_classificados.json'

compare_orientations(file1, file2)
