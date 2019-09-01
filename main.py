import os
from flask import Flask, render_template
import requests
import ast
from bson import ObjectId

app = Flask(__name__)

@app.route('/partidas')
def get_partidas():
    #realizo la request a la API
    r = requests.get('https://murmuring-forest-97474.herokuapp.com/partidas')
    #transformo el resultado del request a lista para poder iterarlo en el template
    partidas = ast.literal_eval(r.text)
    # cambio el _id por el $oid para evitar hacer conversiones en el template
    for p in partidas:
        p["_id"] = p["_id"]["$oid"]
    return render_template('partidas.html', partidas=partidas)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
