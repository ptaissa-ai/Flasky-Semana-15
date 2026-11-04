# Flasky — Gerenciamento de usuários

Aplicação Flask inspirada nas funcionalidades observadas em https://teixeif.pythonanywhere.com/.

## Funcionalidades
- Cadastro de usuários com nome e e-mail.
- Listagem de usuários e função.
- Edição e exclusão com confirmação.
- Persistência com SQLite.
- Validação de e-mail e proteção CSRF.
- Notificação por e-mail ao administrador via SMTP (opcional, configurável).

## Executar localmente
1. Crie e ative um ambiente virtual.
2. Instale as dependências: `pip install -r requirements.txt`
3. Copie `.env.example` para `.env` e configure as variáveis. O uso de python-dotenv pode ser adicionado ao ambiente; no PythonAnywhere, configure as variáveis diretamente no painel ou no WSGI.
4. Execute: `python flask_app.py`
5. Acesse `http://127.0.0.1:5000`.

O banco SQLite `flasky.db` é criado automaticamente na primeira execução.

## Publicar no PythonAnywhere
1. Envie os arquivos para `/home/SEU_USUARIO/flasky`.
2. Em **Web**, crie uma aplicação Flask com a mesma versão de Python usada no ambiente virtual, ou selecione configuração manual.
3. No Bash Console:
   `mkvirtualenv flasky-venv --python=python3.11`
   `workon flasky-venv`
   `pip install -r /home/SEU_USUARIO/flasky/requirements.txt`
4. Na aba **Web**, informe o caminho do virtualenv:
   `/home/SEU_USUARIO/.virtualenvs/flasky-venv`
5. No arquivo WSGI disponibilizado pelo PythonAnywhere, use:
   ```python
   import sys
   path = '/home/SEU_USUARIO/flasky'
   if path not in sys.path:
       sys.path.insert(0, path)

   from flask_app import app as application
   ```
6. Configure as variáveis de ambiente necessárias para e-mail e uma `SECRET_KEY` forte. Se preferir, carregue-as no WSGI antes de importar `flask_app`.
7. Clique em **Reload** na aba Web.

**Importante:** não execute `app.run()` no arquivo WSGI. Ele só é chamado no bloco de execução local.

## Configuração de e-mail
O envio só é ativado quando `MAIL_SERVER`, `MAIL_USERNAME`, `MAIL_PASSWORD` e `ADMIN_EMAIL` estão configurados. Não coloque senhas ou chaves no GitHub. Use variáveis de ambiente e, para contas Gmail, uma senha de app quando aplicável.

## Observação de segurança
Este projeto reproduz um painel acadêmico de CRUD. Para uso público real, acrescente autenticação e autorização de administrador antes de permitir que visitantes editem ou excluam registros. A função exibida é atribuída pelo servidor e não pode ser escolhida pelo formulário público.
