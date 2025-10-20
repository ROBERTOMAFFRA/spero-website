# ======================================================
# SPERO RESTORATION - AUTOMATED BACKUP SCRIPT
# ======================================================

import os
import zipfile
from datetime import datetime

# Root folder (project base)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKUP_DIR = os.path.join(PROJECT_ROOT, "backups")

# ------------------------------------------------------
# FUNCTION TO CREATE BACKUP
# ------------------------------------------------------
def create_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    backup_name = f"spero_backup_{timestamp}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as backup_zip:
        for foldername, subfolders, filenames in os.walk(PROJECT_ROOT):
            # Skip the backups folder itself
            if "backups" in foldername:
                continue
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                rel_path = os.path.relpath(file_path, PROJECT_ROOT)
                backup_zip.write(file_path, rel_path)

    print(f"✅ Backup created successfully: {backup_path}")
    return backup_path


if __name__ == "__main__":
    create_backup()
