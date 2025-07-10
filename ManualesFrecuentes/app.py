from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return '<h1>Página Principal del Proyecto</h1><p>¡Bienvenidos al proyecto colaborativo!</p>'

# --- DEJA ESTE ESPACIO PARA TUS COMPAÑEROS ---
@app.route('/despedida')
def despedida():
    return '<h1>¡Hasta la próxima!</h1><p>Gracias por visitar.</p>'

@app.route('/info')
def informacion():
    return '<h1>Información del Proyecto</h1><p>Este es un proyecto para practicar el flujo de Git.</p>'


# --- FIN DEL ESPACIO ---

if __name__ == '__main__':
    app.run(debug=True)
