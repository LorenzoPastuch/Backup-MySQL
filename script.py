import os
from datetime import datetime, timedelta

# Diretório base do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretório onde os backups serão armazenados
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

# Caminho para o arquivo de configuração do MySQL
DB_CONFIG_FILE = os.path.join(BASE_DIR, 'db_config.cnf')

MYSQLDUMP_CMD = "mysqldump --defaults-file={DB_CONFIG_FILE} superprod > {backup_file}"

# Função para realizar o backup
def realizar_backup():
    # Gera o nome do arquivo de backup com a data atual
    data_atual = datetime.now().strftime('%Y-%m-%d_%Hh%M')
    backup_file = os.path.join(BACKUP_DIR, f"backup_{data_atual}.sql")

    # Executa o comando mysqldump
    os.system(MYSQLDUMP_CMD.format(DB_CONFIG_FILE=DB_CONFIG_FILE, backup_file=backup_file))
    print(f"Backup realizado e salvo em: {backup_file}")

# Função para apagar backups com mais de 30 dias
def remover_backups_antigos():
    limite_data = datetime.now() - timedelta(days=30)

    # Lista e remove backups antigos
    for arquivo in os.listdir(BACKUP_DIR):
        caminho_arquivo = os.path.join(BACKUP_DIR, arquivo)
        if os.path.isfile(caminho_arquivo):
            # Obtém a data de modificação do arquivo
            data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo))
            if data_modificacao < limite_data:
                os.remove(caminho_arquivo)
                print(f"Backup removido: {caminho_arquivo}")

# Função principal para realizar o backup e remover backups antigos
def tarefa_diaria():
    realizar_backup()
    remover_backups_antigos()


# Criar o diretório de backups se não existir
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

tarefa_diaria()

