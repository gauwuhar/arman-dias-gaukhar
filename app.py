from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai

app = Flask(__name__)

chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/interactive_guide', methods=['GET', 'POST'])
def interactive_guide():
    if request.method == 'POST':
        user_message = request.form['input_field']
        chat_history.append(('user', user_message))
        chat_response = get_chat_response(user_message)
        chat_history.append(('assistant', chat_response))
    else:
        chat_response = "Здравствуйте! Чем могу помочь?"
    return render_template('interactive_guide.html', chat_history=chat_history)

def get_chat_response(user_message):
    genai.configure(api_key='AIzaSyCqfehAC7iwbfBc8jnMRgSt8OIa2Z02kpo')  # Замените YOUR_API_KEY на свой ключ API
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content('"model identity_disc": "Ты чат-бот для ответов на вопросы по туризму Казахстана и составлению туристических маршрутов по Казахстану. Твои ответы должен быть только про туризм в Казахстане. Далее идёт запрос пользователя: ' + str(user_message))
    chat_response = response.text
    return chat_response

if __name__ == '__main__':
    app.run(debug=True)