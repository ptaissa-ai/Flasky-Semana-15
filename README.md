# Flasky — Semana 15 · Autenticação

Aplicação acadêmica baseada na Aula 090. O pacote `app/auth` concentra cadastro, login por e-mail, opção de manter conectado, logout e confirmação de conta. Werkzeug armazena o hash da senha, Flask-Login gerencia a sessão e itsdangerous assina links válidos por 24 horas. O SendGrid envia os links por HTTPS. Contas pendentes podem entrar para confirmar ou solicitar outro link, mas o painel exige uma conta confirmada.

O pacote `app/main` contém o painel. Uma conta comum pode editar o próprio perfil. Um administrador pode listar, editar e excluir outras contas. Alterar um endereço exige confirmar o novo e-mail.

## PythonAnywhere

No console Bash:

```bash
cd ~
git clone https://github.com/ptaissa-ai/Flasky-Semana-15.git
cd Flasky-Semana-15
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
chmod 600 .env
python -c 'import secrets; print(secrets.token_hex(32))'
```

Abra `.env` em **Files**. Use a chave gerada em `SECRET_KEY` e copie somente os valores de `API_KEY` e `API_FROM` da configuração privada da Semana 14, se ainda estiverem válidos. Em `APP_BASE_URL`, coloque o endereço HTTPS exibido na aba **Web**. Mantenha `.env` fora do Git.

Em **Web**, aponte **Source code** e **Working directory** para `/home/taissapieri/Flasky-Semana-15` e **Virtualenv** para `/home/taissapieri/Flasky-Semana-15/venv`. A versão Python precisa corresponder à do ambiente. Copie o conteúdo de `wsgi_pythonanywhere.py` para o arquivo WSGI indicado na aba Web. Caso exista um mapeamento de `/static/`, aponte-o para `/home/taissapieri/Flasky-Semana-15/app/static`. Clique em **Reload**. Ao atualizar a aplicação existente, o endereço atual passa a exibir a Semana 15.

A Semana 15 usa seu próprio SQLite `flasky.db`, criado na primeira execução. Cadastre uma conta nova. O banco da Semana 14 tem outro esquema e seus usuários não têm senhas.

## Teste no site

1. Crie uma conta com um e-mail que você controla e tente entrar antes de confirmar. O painel deve pedir confirmação.
2. Abra o link recebido, entre na conta se for solicitado e clique em **Confirmar minha conta**.
3. Confira a saudação, edite seu perfil e saia.
4. Para testar o painel administrativo, promova uma conta já confirmada com o ambiente virtual ativo:

```bash
python -m flask --app flask_app promover-admin seu-email@exemplo.com
```

O SendGrid precisa de uma chave com permissão Mail Send e remetente verificado. Se o envio falhar, o cadastro fica pendente. Após corrigir a configuração, entre e use **Reenviar e-mail de confirmação**.

## Rodar localmente

Instale as dependências e execute `python -m flask --app flask_app run`. Para testar e-mail localmente, configure `APP_BASE_URL=http://127.0.0.1:5000` e credenciais de envio válidas. O teste automatizado usa SQLite em memória e simula a API do SendGrid.

```bash
python -m unittest discover -s tests -v
```
