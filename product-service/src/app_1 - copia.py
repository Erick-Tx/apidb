# Importaciones necesarias
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_basicauth import BasicAuth
#from werkzeug.urls import url_quote
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_limiter import Limiter
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_basicauth import BasicAuth

# Lista de productos de ejemplo
products = [{'id': 1, 'name': 'Product 1'},
            {'id': 2, 'name': 'Product 2'}]

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar el límite de solicitudes
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# Número de puerto para ejecutar la aplicación
port_number = 7002

# curl -u Dazeth:123 -v http://localhost:7002/products
# curl -H 'Authorization: bAsic am9objptY -v http://localhost:7002/products

# Configuración de autenticación básica
app.config['BASIC_AUTH_USERNAME'] = 'Dazeth'
app.config['BASIC_AUTH_PASSWORD'] = '123'
#app.config['BASIC_AUTH_FORCE'] = True
####################################################################
# Inicializar la autenticación básica
basic_auth = BasicAuth(app)


####################################################################
# Ruta para obtener la lista de productos
# curl -v http://localhost:7002/products
@app.route('/products')
@limiter.limit("10/minute")  # Límite de solicitudes
@basic_auth.required  # Autenticación requerida
def get_products():
    # Registros de nivel de información
    app.logger.info("LogInfo: GET productos")
    app.logger.debug("A debug message")
    app.logger.info("An info message")
    app.logger.warning("A warning message")
    app.logger.error("An error message")
    app.logger.critical("A critical message")
    
    # Devolver la lista de productos como JSON
    return jsonify(products)

# curl -v http://localhost:7002/product/1
# Ruta para obtener un producto por su ID
@app.route('/product/<int:id>')
@limiter.limit("10/minute")  # Límite de solicitudes
def get_product(id):
    # Filtrar la lista de productos por ID
    product_list = [product for product in products if product['id'] == id]
    # Manejar el caso en que el producto no se encuentre
    if len(product_list) == 0:
        return f'Product with id {id} not found', 404
    # Devolver el producto encontrado como JSON
    return jsonify(product_list[0])

# Ruta para agregar un nuevo producto
# curl --header "Content-Type: application/json" --request POST --data "{\"name\": \"Product 3\"}" -v http://localhost:7002/product
@app.route('/product', methods=['POST'])
@limiter.limit("10/minute")  # Límite de solicitudes
def post_product():
    # Obtener el producto del cuerpo de la solicitud
    request_product = request.json

    # Generar un nuevo ID para el producto
    new_id = max([product['id'] for product in products]) + 1

    # Crear un nuevo producto
    new_product = {
        'id': new_id,
        'name': request_product['name']
    }

    # Agregar el nuevo producto a la lista
    products.append(new_product)

    # Devolver el nuevo producto como JSON con el código de estado 201 (Created)
    return jsonify(new_product), 201

# Ruta para actualizar un producto por su ID
# curl --header "Content-Type: application/json" --request PUT --data '{"name": "Updated Product 2"}' -v http://localhost:7002/product/2
@app.route('/product/<int:id>', methods=['PUT'])
@limiter.limit("10/minute")  # Límite de solicitudes
def put_product(id):
    # Obtener la carga útil de la solicitud
    updated_product = request.json

    # Buscar el producto con el ID especificado
    for product in products:
        if product['id'] == id:
            # Actualizar el nombre del producto
            product['name'] = updated_product['name']
            # Devolver el producto actualizado como JSON con el código de estado 200 (OK)
            return jsonify(product), 200

    # Devolver un mensaje de error si el producto no se encuentra con el código de estado 404 (Not Found)
    return f'Product with id {id} not found', 404

# Ruta para eliminar un producto por su ID
# curl --request DELETE -v http://localhost:7002/product/2
@app.route('/product/<int:id>', methods=['DELETE'])
@limiter.limit("10/minute")  # Límite de solicitudes
def delete_product(id):
    # Buscar el producto con el ID especificado
    product_list = [product for product in products if product['id'] == id]
    # Manejar el caso en que el producto no se encuentre
    if len(product_list) == 1:
        # Eliminar el producto de la lista
        products.remove(product_list[0])
        # Devolver un mensaje de éxito con el código de estado 200 (OK)
        return f'Product with id {id} deleted', 200

    # Devolver un mensaje de error si el producto no se encuentra con el código de estado 404 (Not Found)
    return f'Product with id {id} not found', 404

# Iniciar la aplicación si se ejecuta como script principal
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port_number)
