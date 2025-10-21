import os
import shutil
import datetime

# Define os arquivos e pastas de backup
FILES_TO_BACKUP = {
    "templates/index.html": "templates/backups/",
    "static/css/style.css": "static/css/backups/",
    "app.py": "backups_app/"
}

def create_backup(src_path, dest_dir):
    """Cria cópia do arquivo com data e hora no nome."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M")
    filename = os.path.basename(src_path)
    name, ext = os.path.splitext(filename)
    backup_name = f"{name}_{timestamp}{ext}"
    dest_path = os.path.join(dest_dir, backup_name)
    shutil.copy2(src_path, dest_path)
    print(f"✅ Backup created: {dest_path}")

def main():
    print("=== Spero Restoration | Automatic Backup System ===")
    for src, dest in FILES_TO_BACKUP.items():
        if os.path.exists(src):
            create_backup(src, dest)
        else:
            print(f"⚠️  File not found: {src}")
    print("=== Backup completed successfully ===")

if __name__ == "__main__":
    main()
