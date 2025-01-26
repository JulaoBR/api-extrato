from flask import Flask
from routes import routes
from decouple import config

from middleware.middleware import Middleware

app = Flask(__name__)

IPS_PERMITIDOS = config('IPS_PERMITIDOS', default='').split(',')

# Aplica o middleware
app.wsgi_app = Middleware(app.wsgi_app, ips_permitidos = IPS_PERMITIDOS)

# Registrando as rotas
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)