import google.generativeai as genai

genai.configure(api_key='AIzaSyCqfehAC7iwbfBc8jnMRgSt8OIa2Z02kpo')

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Напиши мне туристический маршрут для путешествий по Астане')

print(response.text)