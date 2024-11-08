# flask-ezlogin

**flask-ezlogin** é um pacote que facilita a configuração de sistemas de login no Flask usando Flask-Login.

## Instalação

Você pode instalar diretamente do PyPI com:

```bash
pip install flask-ezlogin
```

### Funcionalidades

login_required: Um wrapper para o decorator login_required do Flask-Login.
check_authentication: Redireciona o usuário autenticado para uma rota protegida se ele já estiver logado.
prevent_cache: Adiciona cabeçalhos para evitar cache em páginas sensíveis, como as páginas de login e cadastro.

Exemplos de Uso
Aqui estão alguns exemplos práticos de como usar os decorators oferecidos pelo flask-ezlogin.

1. Proteger uma Rota com login_required
   Use login_required para restringir o acesso a uma rota apenas para usuários autenticados.

from flask import Flask, redirect, url_for
from flask_ezlogin import login_required, logout_user

app = Flask(**name**)

@app.route("/protected")
@login_required
def protected():
return "Esta é uma rota protegida."

@app.route("/logout")
@login_required
def logout():
logout_user()
return redirect(url_for("index"))

2. Redirecionar Usuários Autenticados com check_authentication
   Use check_authentication para redirecionar usuários já autenticados para uma rota protegida. Isso é útil, por exemplo, na página de login.

from flask import Flask, render_template
from flask_ezlogin import check_authentication, prevent_cache

app = Flask(**name**)

@app.route("/login")
@check_authentication("protected") # Redireciona para /protected se o usuário já estiver logado
@prevent_cache # Evita cache para essa página
def login():
return render_template("login.html")

3. Evitar Cache com prevent_cache
   O decorator prevent_cache adiciona cabeçalhos para garantir que o navegador não armazene a página em cache.

@app.route("/register")
@prevent_cache
def register():
return render_template("register.html")

### Contribuição

Contribuições são bem-vindas! Se você encontrar problemas, tiver ideias para novas funcionalidades ou melhorias, sinta-se à vontade para abrir um pull request ou relatar problemas no repositório GitHub.

### Licença

Este projeto é licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
