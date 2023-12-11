# Importar las bibliotecas necesarias
import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
#from werkzeug.utils import url_quote
import logging

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Obtener las credenciales de Google desde las variables de entorno
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = os.getenv('secret_key')

# Configurar variables de entorno para permitir el transporte inseguro y relajar el alcance del token OAuth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Crear el Blueprint de Google para la autenticación OAuth
blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,  # Solicitar consentimiento nuevamente si es necesario
    scope=["profile", "email"]  # Alcance de la información solicitada al usuario
)

# Registrar el Blueprint en la aplicación con un prefijo de URL '/login'
app.register_blueprint(blueprint, url_prefix="/login")

# Ruta principal que renderiza la plantilla 'index.j2'
@app.route("/")
def index():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'

    # Verificar si el usuario está autenticado con Google
    if google.authorized:
        # Obtener datos del usuario desde el punto final de información del usuario OAuth
        google_data = google.get(user_info_endpoint).json()

    # Renderizar la plantilla con los datos de Google y la URL del punto final de información del usuario
    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)

# Ruta para redirigir al usuario a la página de inicio de sesión de Google
@app.route('/login')
def login():
    return redirect(url_for('google.login'))

# Iniciar la aplicación si el script se ejecuta directamente
if __name__ == "__main__":
    app.run()
