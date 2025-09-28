import pandas as pd

# Carrega o arquivo CSV
df = pd.read_csv('dados.csv', sep=';', encoding='utf-8', on_bad_lines='skip')

# Substitui valores NaN por None, que será convertido para null no JSON
df = df.where(pd.notnull(df), None)

# Converte o DataFrame para uma lista de dicionários
dados = df.to_dict(orient='records')

# Gera o conteúdo do arquivo dados1.js
with open('dados1.js', 'w', encoding='utf-8') as f:
    f.write('const pacientes = ')
    # Converte os dados para JSON com indentação para melhor legibilidade
    import json
    json_content = json.dumps(dados, ensure_ascii=False, indent=4)
    f.write(json_content)
    f.write(';')