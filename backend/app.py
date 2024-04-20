from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    create_table()
    return render_template('index.html')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie = {
            'title': request.form['title'],
            'genre': request.form['genre'],
            'actors': request.form['actors'],
            'description': request.form['description'],
            'release_year': request.form['release_year'],
            'video_url': request.form['video_url'],
            'rating': request.form['rating'],
            'stream_url': request.form['stream_url'],
        }
        add_movie_to_db(movie)
        return redirect(url_for('list_movies'))
    return render_template('add_movie.html')


@app.route('/list_movies', methods=['GET', 'POST'])
def list_movies():
    create_table()

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        movies = search_movies_in_db(search_query)
    else:
        try:
            conn = sqlite3.connect(db_filename)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM movies')
            movies = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            print("Ошибка😡 при выводе списка фильмов: ", e)

    return render_template('list_movies.html', movies=movies)


@app.route('/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(movie_id):
    if request.method == 'POST':
        field = request.form['field']
        new_value = request.form['new_value']
        update_movie_in_db(movie_id, field, new_value)
        return redirect(url_for('list_movies'))

    return render_template('update_movie.html', movie_id=movie_id)


if __name__ == '__main__':
    app.run(debug=True)









#---------генератор--------------
import google.generativeai as genai
genai.configure(api_key='AIzaSyCqfehAC7iwbfBc8jnMRgSt8OIa2Z02kpo')
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Напиши мне туристический маршрут для путешествий по Астане')
print(response.text)
#--------------------------------