import json
import requests
import time

# 🔑 Coloque aqui a sua API KEY do Google Cloud (Geocoding API habilitada)
API_KEY = "AIzaSyAi5b5UQYjD6TWqSbXxCBBxZLMNFOX8kwI"

# Arquivos
input_file = "dados1.js"
output_file = "dados.js"

# Função para montar endereço completo
def montar_endereco(paciente):
    partes = [
        paciente.get("Rua", ""),
        str(paciente.get("Número", "")),
        paciente.get("Complemento", ""),
        paciente.get("Bairro", ""),
        paciente.get("Município", ""),
        paciente.get("UF", ""),
        "Brasil"
    ]
    return ", ".join([p for p in partes if p and p != "-"])

# Função para buscar coordenadas no Google Geocoding API
def buscar_coordenadas_google(endereco):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": endereco, "key": API_KEY}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("status") == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print(f"❌ Google API erro: {data.get('status')}")
    except Exception as e:
        print(f"❌ Erro ao buscar '{endereco}': {e}")
    return None, None

# 1. Ler arquivo JS existente
with open(input_file, "r", encoding="utf-8") as f:
    conteudo = f.read()
    conteudo = conteudo.replace("const pacientes =", "").strip()
    if conteudo.endswith(";"):
        conteudo = conteudo[:-1]
    pacientes = json.loads(conteudo)

# 2. Processar pacientes
for paciente in pacientes:
    endereco = montar_endereco(paciente)
    print(f"📍 Buscando no Google Maps: {endereco}")
    lat, lon = buscar_coordenadas_google(endereco)
    if lat and lon:
        paciente["latitude"] = lat
        paciente["longitude"] = lon
        paciente["map_link_google"] = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    else:
        paciente["latitude"] = None
        paciente["longitude"] = None
        paciente["map_link_google"] = None
    time.sleep(0.5)  # evita estourar limite da API

# 3. Salvar saída
with open(output_file, "w", encoding="utf-8") as f:
    f.write("const pacientes = ")
    json.dump(pacientes, f, ensure_ascii=False, indent=4)
    f.write(";")

print(f"✅ Banco de dados atualizado com coordenadas → {output_file}")
