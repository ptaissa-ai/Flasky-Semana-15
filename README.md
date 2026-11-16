# Flasky — Semana 16 · Autenticação

Aplicação acadêmica baseada na Aula 090. O pacote `app/auth` concentra cadastro, login por e-mail, opção de manter conectado, logout e confirmação de conta. Werkzeug armazena o hash da senha, Flask-Login gerencia a sessão e itsdangerous assina links válidos por 24 horas. O SendGrid envia os links por HTTPS. Contas pendentes podem entrar para confirmar ou solicitar outro link, mas o painel exige uma conta confirmada.

O pacote `app/main` contém o painel. Uma conta comum pode editar o próprio perfil. Um administrador pode listar, editar e excluir outras contas. Alterar um endereço exige confirmar o novo e-mail.

## PythonAnywhere

No console Bash do PythonAnywhere, clone a branch da Semana 16 em uma pasta própria:

```bash
cd ~
git clone --branch semana16-autenticacao https://github.com/ptaissa-ai/Flasky-Semana-15.git Flasky-Semana-16
cd Flasky-Semana-16
source ~/Semana-14-Flasky/venv/bin/activate
python -m pip install --no-cache-dir --no-compile -r requirements.txt
cp -n .env.example .env
chmod 600 .env
python -c 'import secrets; print(secrets.token_hex(32))'
```

Abra `.env` em **Files**. Use a chave gerada em `SECRET_KEY` e copie somente os valores de `API_KEY` e `API_FROM` da configuração privada da Semana 15, se ainda estiverem válidos. Em `APP_BASE_URL`, coloque o endereço HTTPS exibido na aba **Web**. Mantenha `.env` fora do Git.

Em **Web**, aponte **Source code** e **Working directory** para `/home/taissapieri/Flasky-Semana-16` e **Virtualenv** para `/home/taissapieri/Semana-14-Flasky/venv`. A versão Python precisa corresponder à do ambiente. Copie o conteúdo de `wsgi_pythonanywhere.py` para o arquivo WSGI indicado na aba Web. Caso exista um mapeamento de `/static/`, aponte-o para `/home/taissapieri/Flasky-Semana-16/app/static`. Clique em **Reload**. Ao atualizar a aplicação existente, o endereço atual passa a exibir a Semana 16.

A Semana 16 usa seu próprio SQLite `flasky.db`, criado na primeira execução. Cadastre uma conta nova. O banco da Semana 14 tem outro esquema e seus usuários não têm senhas.

## Teste no site

1. Crie uma conta com um e-mail que você controla e tente entrar antes de confirmar. O painel deve pedir confirmação.
2. Abra o link recebido, entre na conta se for solicitado e clique em **Confirmar minha conta**.
3. Confira a saudação, edite seu perfil e saia.
4. Na tela de login, escolha **Esqueci minha senha**. Confira o e-mail e o spam. O link vale 30 minutos e é invalidado ao salvar a nova senha.
5. Depois de entrar, use **Alterar senha** e informe a senha atual.
6. Para testar o painel administrativo, promova uma conta já confirmada com o ambiente virtual ativo:

```bash
python -m flask --app flask_app promover-admin seu-email@exemplo.com
```

O SendGrid precisa de uma chave com permissão Mail Send e remetente verificado. Se o envio falhar, o cadastro fica pendente. Após corrigir a configuração, entre e use **Reenviar e-mail de confirmação**.

## Rodar localmente

Instale as dependências e execute `python -m flask --app flask_app run`. Para testar e-mail localmente, configure `APP_BASE_URL=http://127.0.0.1:5000` e credenciais de envio válidas. O teste automatizado usa SQLite em memória e simula a API do SendGrid.

```bash
python -m unittest discover -s tests -v
```

## Testar com Resend

Crie a conta Resend com o mesmo e-mail do cadastro Flasky. Adicione `RESEND_API_KEY` com uma chave de envio ao `.env` e recarregue o aplicativo. A presença dessa variável seleciona o Resend para confirmação e recuperação de senha. O remetente padrão, `onboarding@resend.dev`, só permite envio ao endereço da conta Resend. Para demais destinatários, verifique um domínio e defina `RESEND_FROM` com um remetente desse domínio.

## Brevo e aviso de cadastro

No painel Brevo, verifique o telefone, verifique um remetente e gere uma chave de API.
No .env do PythonAnywhere, preencha BREVO_API_KEY com a chave, BREVO_FROM com o endereço
verificado e STUDENT_EMAIL com o seu e-mail pessoal. Clique em Web → Reload.
Quando BREVO_API_KEY está definida, a Brevo tem prioridade sobre Resend e SendGrid.

Em um cadastro novo, o Flasky tenta enviar a confirmação ao endereço cadastrado
e uma notificação separada para o e-mail pessoal e para flaskaulasweb@zohomail.com.
A notificação informa nome, prontuário e nome de usuário. O botão de reenvio
envia apenas a confirmação para a conta existente.
