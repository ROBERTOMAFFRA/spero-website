import os
import zipfile
from datetime import datetime

# Caminhos base
BASE_DIR = r"C:\spero-website"
BACKUP_DIR = os.path.join(BASE_DIR, "backup")

# Garante que a pasta de backup exista
os.makedirs(BACKUP_DIR, exist_ok=True)

# Nome do arquivo de backup com data e hora
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"backup_{timestamp}.zip"
backup_path = os.path.join(BACKUP_DIR, backup_filename)

# Extensões que serão incluídas no backup
extensions = ('.py', '.html', '.css', '.js', '.xml', '.txt', '.json', '.ico', '.png', '.jpg', '.jpeg', '.svg')

# Função principal de backup
def create_backup():
    file_count = 0

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        for root, dirs, files in os.walk(BASE_DIR):
            # Ignora as pastas internas que não precisam ser copiadas
            if any(skip in root for skip in ['backup', 'auto_backup', '__pycache__']):
                continue

            for file in files:
                if file.endswith(extensions):
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, BASE_DIR)
                    backup_zip.write(filepath, arcname)
                    file_count += 1

    # Verifica se o arquivo zip realmente contém algo
    if file_count == 0:
        os.remove(backup_path)
        print("⚠️ Nenhum arquivo encontrado para backup. Nenhum ZIP foi criado.")
    else:
        size_mb = os.path.getsize(backup_path) / (1024 * 1024)
        print(f"✅ Backup criado com sucesso: {backup_path}")
        print(f"📦 {file_count} arquivos incluídos ({size_mb:.2f} MB)")
        print(f"🕒 Criado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Executa
if __name__ == "__main__":
    create_backup()
