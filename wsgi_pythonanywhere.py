# Exemplo de conteúdo para o arquivo WSGI do PythonAnywhere.
# Substitua SEU_USUARIO pelo nome da sua conta.
import sys
path = '/home/SEU_USUARIO/flasky'
if path not in sys.path:
    sys.path.insert(0, path)

from flask_app import app as application
