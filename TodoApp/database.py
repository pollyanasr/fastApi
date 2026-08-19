import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

# Carrega o .env que fica na mesma pasta deste arquivo (TodoApp/.env)
load_dotenv(Path(__file__).resolve().parent / '.env')

# =====================================================================
# COMO TROCAR DE BANCO
# ---------------------------------------------------------------------
# Deixe APENAS UM dos tres blocos abaixo descomentado. Cada bloco define
# as duas variaveis que o create_engine() no final do arquivo usa:
#
#   SQLALCHEMY_DATABASE_URL -> a URL de conexao
#   ENGINE_KWARGS           -> os argumentos extras do engine
#
# Nao esqueca de ajustar o TodoApp/.env (DB_HOST, DB_PORT, DB_NAME,
# DB_USER, DB_PASSWORD) para o banco escolhido.
# =====================================================================


# ------------------------- 1) SQLITE3 --------------------------------
# Nao precisa de servidor nem de .env: cria o arquivo todosapp.db na
# pasta de onde a aplicacao for iniciada.
# check_same_thread=False -> APENAS PARA SQLITE. Permite que a mesma
#   conexao seja usada por threads diferentes (o FastAPI atende as
#   requisicoes em um threadpool).
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
ENGINE_KWARGS = {
    'connect_args': {'check_same_thread': False},
}


# ----------------------- 2) POSTGRESQL -------------------------------
# Driver: postgresql+psycopg2 (pacote psycopg2-binary).
# .env sugerido: DB_PORT=5432, DB_USER=postgres, DB_HOST=localhost
# SQLALCHEMY_DATABASE_URL = URL.create(
#     drivername='postgresql+psycopg2',
#     username=os.getenv('DB_USER', 'postgres'),
#     password=os.getenv('DB_PASSWORD'),
#     host=os.getenv('DB_HOST', 'localhost'),
#     port=int(os.getenv('DB_PORT', '5432')),
#     database=os.getenv('DB_NAME', 'todoapp'),
# )
# ENGINE_KWARGS = {
#     # pool_pre_ping: testa a conexao antes de usar e descarta as que o
#     #   servidor ja fechou por inatividade.
#     'pool_pre_ping': True,
# }


# -------------------------- 3) MYSQL ---------------------------------
# Driver: mysql+pymysql (pacote PyMySQL, puro Python, nao precisa compilar).
# .env sugerido: DB_PORT=3306, DB_USER=root, DB_HOST=127.0.0.1
#
# NAO montar a URL como string: uma senha com '@' (ex.: 'Inova@123') faz o
# SQLAlchemy tratar o '@' como separador entre credenciais e host. A URL
# 'mysql+pymysql://root:Inova@123@127.0.0.1:3306/todoapp' e lida como
# host='123'. URL.create recebe cada parte separada e faz o escape dos
# caracteres especiais (@, :, /, ?, #) automaticamente.
# SQLALCHEMY_DATABASE_URL = URL.create(
#     drivername='mysql+pymysql',
#     username=os.getenv('DB_USER', 'root'),
#     password=os.getenv('DB_PASSWORD'),
#     host=os.getenv('DB_HOST', '127.0.0.1'),
#     port=int(os.getenv('DB_PORT', '3306')),
#     database=os.getenv('DB_NAME', 'todoapp'),
#     query={'charset': 'utf8mb4'},  # suporte completo a UTF-8 (acentos, emoji)
# )
# ENGINE_KWARGS = {
#     # pool_pre_ping: testa a conexao antes de usar e descarta as que o
#     #   MySQL ja fechou por inatividade (wait_timeout, 8h por padrao).
#     'pool_pre_ping': True,
#     # pool_recycle: recicla conexoes antes desse limite, evitando o erro
#     #   "MySQL server has gone away".
#     'pool_recycle': 3600,
# }


# =====================================================================
# Daqui para baixo nada muda ao trocar de banco
# =====================================================================
engine = create_engine(SQLALCHEMY_DATABASE_URL, **ENGINE_KWARGS)

# Fabrica de sessoes usada pela dependencia get_db() das rotas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base da qual os models (models.py) herdam
Base = declarative_base()
