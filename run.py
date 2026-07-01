import subprocess

subprocess.run(["bash", "run_scrapper.sh"], check=True)
subprocess.run(["bash", "run_add_country.sh"], check=True)
subprocess.run([
    "uvicorn",
    "api.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
])