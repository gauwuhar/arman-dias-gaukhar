from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interactive_guide', methods=['GET', 'POST'])
def interactive_guide():
    return render_template('interactive_guide.html')


if __name__ == '__main__':
    app.run(debug=True)









#---------генератор--------------
import google.generativeai as genai
genai.configure(api_key='AIzaSyCqfehAC7iwbfBc8jnMRgSt8OIa2Z02kpo')
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Напиши мне туристический маршрут для путешествий по Астане')
print(response.text)
#--------------------------------