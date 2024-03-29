import os
from flask import Flask, render_template, request, redirect
import requests
import ast
from bson import ObjectId
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def hola():
    return render_template('index.html', title="Bienvenido!")

@app.route('/partidas')
def get_partidas():
    #realizo la request a la API
    r = requests.get('https://murmuring-forest-97474.herokuapp.com/partidas')
    #transformo el resultado del request a lista para poder iterarlo en el template
    partidas = ast.literal_eval(r.text)
    # cambio el _id por el $oid para evitar hacer conversiones en el template
    for p in partidas:
        p["_id"] = p["_id"]["$oid"]
    return render_template('partidas.html', title="Listado de partidas", partidas=partidas)


@app.route('/partida/<id>')
def get_partida(id):
    r = requests.get('https://murmuring-forest-97474.herokuapp.com/partida/{}'.format(id))
    #transformo a diccionario
    partida = ast.literal_eval(r.text)
    #piso id para tratar mas facil en template
    partida["_id"] = partida["_id"]["$oid"]
    tab = partida["tablero"].split(",")
    return render_template('partida.html', title="Partida {}".format(partida["_id"]) , partida=partida, tablero=tab)


@app.route('/partida/<id>/jugar/<pos>')
def jugar(id, pos):
    r = requests.get('https://murmuring-forest-97474.herokuapp.com/partida/{}/jugar/{}'.format(id, pos))
    return redirect('/partida/{}'.format(id))


@app.route('/crear_partida', methods=['POST'])
def crear_partida():
    result = request.form.to_dict()
    now = datetime.now()
    result["add_date"] = now.strftime("%m/%d/%Y, %H:%M:%S")
    r = requests.post(url='https://murmuring-forest-97474.herokuapp.com/nueva_partida', json=result)
    # convierto a diccionario
    partida = ast.literal_eval(r.text)
    return redirect('/partida/{}'.format(partida["_id"]["$oid"]))


@app.route('/nueva_partida', methods=['GET'])
def nueva_partida():
    return render_template('nueva_partida.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
