# Flasky — Semana 15 (Autenticação)

Projeto acadêmico Flask com gerenciamento de usuários e autenticação, baseado nos tópicos da Aula 090 — Autenticação de usuário.

## Funcionalidades
- Cadastro com nome, nome de usuário, e-mail e senha.
- Hashing de senha com Werkzeug (`generate_password_hash` e `check_password_hash`).
- Login por e-mail e senha, opção de manter conectado e logout com Flask-Login.
- Blueprint separado para autenticação (`app/auth`).
- Proteção das rotas de gerenciamento com `login_required`.
- Confirmação de conta por token assinado com itsdangerous e envio SMTP.
- Reenvio de e-mail de confirmação.
- Listagem, edição e exclusão de usuários após login e confirmação.
- SQLite, Flask-SQLAlchemy e proteção CSRF.

## Execução local
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python flask_app.py
```
Acesse http://127.0.0.1:5000.

## Configuração de e-mail
Configure no ambiente `SECRET_KEY`, `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD` e `MAIL_DEFAULT_SENDER`. Sem SMTP configurado, o cadastro é criado, mas a mensagem de confirmação não é enviada. Não publique senhas ou chaves no GitHub.

## PythonAnywhere
1. Bash:
```bash
cd ~/Flasky-Semana-15
workon flasky-venv
pip install --no-cache-dir -r requirements.txt
```
2. Web > Code: source code e working directory em `/home/SEU_USUARIO/Flasky-Semana-15`.
3. Virtualenv: `/home/SEU_USUARIO/.virtualenvs/flasky-venv`.
4. WSGI:
```python
import sys
path = '/home/SEU_USUARIO/Flasky-Semana-15'
if path not in sys.path:
    sys.path.insert(0, path)
from flask_app import app as application
```
5. Configure as variáveis de ambiente no WSGI ou no mecanismo de configuração disponível na sua conta e clique Reload.

## Atenção ao banco de dados existente
O `db.create_all()` cria tabelas ausentes, mas não altera tabelas antigas. Esta versão adiciona `username`, `password_hash` e `confirmed` ao modelo User. Se você já executou a versão anterior e o arquivo `flasky.db` antigo existir, faça backup e, se não houver dados que precise preservar, remova esse banco antigo antes de iniciar a versão nova. Para preservar dados, crie uma migração de banco antes de atualizar.

## Observação de segurança
Este projeto é didático. O exemplo permite que qualquer conta autenticada e confirmada acesse o gerenciamento de usuários, conforme o escopo simplificado da aula. Para uso real, implemente autorização por perfil (administrador) antes de permitir edição e exclusão de outras contas.
