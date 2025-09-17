import requests
import time

url = "http://127.0.0.1:5000/usuario/1"  # endpoint da API
num_requests = 50
tempos = []

for i in range(num_requests):
    start = time.time()
    response = requests.get(url)
    end = time.time()
    tempos.append(end - start)
    if response.status_code != 200:
        print(f"Erro na requisição {i}: {response.status_code}")

print(f"Tempo médio: {sum(tempos)/len(tempos):.3f}s")
print(f"Tempo mínimo: {min(tempos):.3f}s")
print(f"Tempo máximo: {max(tempos):.3f}s")
