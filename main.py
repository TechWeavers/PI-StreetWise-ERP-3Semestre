
import subprocess

services = [
    {"file": "routes.loginRoute", "port": 8000},
    {"file": "routes.userRoute", "port": 8001},
    # Adicione mais serviços conforme necessário
]

processes = []

for service in services:
    cmd = f"uvicorn {service['file']}:app --port {service['port']} --reload --host 127.0.0.1"
    process = subprocess.Popen(cmd, shell=True)
    processes.append(process)

for process in processes:
    process.wait()
