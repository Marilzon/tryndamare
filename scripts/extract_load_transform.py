import subprocess, time
from definitions import source_config, target_config

def wait_for_db(host, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print(f"Successfully connected to PostgreSQL: {host}")
                return True
        except:
            time.sleep(2)
    return False

wait_for_db(source_config["host"])
wait_for_db(target_config["host"])

export_dump_command = [
    "pg_dump",
    "-h",
    source_config["host"],
    "-U",
    source_config["user"],
    "-d",
    source_config["dbname"],
    "-f",
    "data_dump.sql",
    "-w",
]

try:
    subprocess_env = dict(PGPASSWORD=source_config["password"])
    subprocess.run(export_dump_command, env=subprocess_env, check=True)
except Exception as e:
    print(f"pg_dump error: {e}")

import_dump_command = [
    "psql",
    "-h",
    target_config["host"],
    "-U",
    target_config["user"],
    "-d",
    target_config["dbname"],
    "-a",
    "-f",
    "data_dump.sql",
]

try:
    subprocess_env = dict(PGPASSWORD=target_config["password"])
    subprocess.run(import_dump_command, env=subprocess_env, check=True)
except Exception as e:
    print(f"psql load error: {e}")
