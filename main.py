
import subprocess

services = [
    {"file": "routes.loginRoute", "port": 8000},
    {"file": "routes.userRoute", "port": 8001},
    {"file": "routes.redefinicaoRoute", "port": 8002},
    {"file": "routes.clienteRoute", "port": 8003},
    # Adicione mais serviços conforme necessário
]

processes = []

for service in services:
    cmd = f"uvicorn {service['file']}:app --port {service['port']} --reload"
    process = subprocess.Popen(cmd, shell=True)
    processes.append(process)

for process in processes:
    process.wait()
