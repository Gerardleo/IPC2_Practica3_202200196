from flask import Flask, request, jsonify
import flask_cors

app = Flask(__name__)
flask_cors.CORS(app)

almacenPeliculas=[]


@app.route('/api/new-movie', methods=['POST'])
def api():
    data = request.get_json()
    if data is None:
        return jsonify(message='No se recibieron datos'), 400

    movie_id = data.get('id_movie')
    if any(movie.get('id_movie') == movie_id for movie in almacenPeliculas):
        return jsonify(message=f'La película con ID {movie_id} ya existe'), 400

    almacenPeliculas.append(data)
    return jsonify(message='Película agregada correctamente')

@app.route('/api/all-movies-by-genero/<string:genero>', methods=['GET'])
def get_movies_by_genre(genero):
    movies_in_genero = [movie for movie in almacenPeliculas if movie['genero'] == genero]
    if not movies_in_genero:
        return jsonify(message=f'No se encontraron películas en el género: {genero}'), 404
    return jsonify(movies_in_genero)



@app.route('/api/update-movie', methods=['PUT'])
def update_movie():
    data = request.get_json()
    if data is None:
        return jsonify(message='No se recibieron datos en el cuerpo de la solicitud'), 400

    movie_id = data.get('id_movie')
    new_name = data.get('movie_name')
    new_genero = data.get('genero')

    if not movie_id or not new_name or not new_genero:
        return jsonify(message='El cuerpo de la solicitud debe incluir "id_movie", "name" y "genero"'), 400

    movie_to_update = next((movie for movie in almacenPeliculas if movie['id_movie'] == movie_id), None)

    if movie_to_update is None:
        return jsonify(message=f'No se encontró una película con id_movie {movie_id}'), 404

    movie_to_update['movie_name'] = new_name
    movie_to_update['genero'] = new_genero

    return jsonify(message=f'Película con id_movie {movie_id} actualizada correctamente', updated_movie=movie_to_update)



if __name__ == '__main__':
    app.run(debug=True, port=5000)

