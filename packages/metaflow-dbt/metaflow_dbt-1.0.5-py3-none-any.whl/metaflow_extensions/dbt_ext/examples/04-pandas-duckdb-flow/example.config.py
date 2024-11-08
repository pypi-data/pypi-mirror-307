import os

PVC_NAME = ""  # Replace with existing PVC name
PVC_MOUNT = "/mnt/duckdb"  # Replace where to mount the PVC volume

DUCKDB_PATH = os.path.join(PVC_MOUNT, "database.duckdb")
DBT_PROFILES = {
    "duckdb_project": {
        "outputs": {"dev": {"type": "duckdb", "path": DUCKDB_PATH}},
        "target": "dev",
    }
}
