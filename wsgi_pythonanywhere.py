# Exemplo para o arquivo WSGI do PythonAnywhere.
import sys
path = '/home/taissapieri/Flasky-Semana-15'
if path not in sys.path:
    sys.path.insert(0, path)

from config import Config

if Config.SECRET_KEY == "chave-apenas-para-desenvolvimento" or len(Config.SECRET_KEY) < 32:
    raise RuntimeError("Configure uma SECRET_KEY forte no .env da Semana 15.")
if not Config.APP_BASE_URL.startswith("https://"):
    raise RuntimeError("Configure APP_BASE_URL com o endereço HTTPS da aplicação.")

from flask_app import app as application
