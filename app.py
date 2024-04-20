from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interactive_guide', methods=['GET', 'POST'])
def interactive_guide():
    if request.method == 'POST':
        user_message = {
            'user_message': request.form['input_field'],
        }
        get_user_input(user_message)
    return render_template('interactive_guide.html')


def get_user_input(user_message):
    genai.configure(api_key='AIzaSyCqfehAC7iwbfBc8jnMRgSt8OIa2Z02kpo')
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content('Привет' + str(user_message))
    print(response.text)

if __name__ == '__main__':
    app.run(debug=True)