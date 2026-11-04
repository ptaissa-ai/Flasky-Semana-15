# Exemplo para o arquivo WSGI do PythonAnywhere.
import sys
path = '/home/SEU_USUARIO/Flasky-Semana-15'
if path not in sys.path:
    sys.path.insert(0, path)

from flask_app import app as application
