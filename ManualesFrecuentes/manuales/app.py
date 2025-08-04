from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    return '<h1>Página Principal del Proyecto</h1><p>¡Bienvenidos al proyecto colaborativo!</p>'

# --- DEJA ESTE ESPACIO PARA TUS COMPAÑEROS ---
@app.route('/despedida')
def despedida():
    return '<h1>¡Hasta la próxima!</h1><p>Gracias por visitar.</p>'

@app.route('/soporteTecnico')
def soporteTecnico():
    return render_template('soporteTecnico.html') 

@app.route('/Registro')
def registro():
    return render_template('Registro.html') 

@app.route('/recuperarContrasena')
def recuperarContrasena():
    return render_template('recuperarContrasena.html') 



if __name__ == '__main__':
    app.run(port=5000)


# --- FIN DEL ESPACIO ---

if __name__ == '__main__':
    app.run(debug=True)
