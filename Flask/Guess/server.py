from flask import Flask, render_template
import requests, datetime

app = Flask(__name__)

@app.route('/guess/<name>')
def guess(name):
    response = requests.get(f'https://api.agify.io?name={name}')
    response.raise_for_status()
    data = response.json()
    # name = data['name']
    age = data['age']
    response = requests.get(f'https://api.genderize.io?name={name}')
    response.raise_for_status()
    data = response.json()
    gender = data['gender']
    year = datetime.datetime.now().year 
    return render_template('index.html', name=name, age=age, gender=gender, year=year)

if __name__ == '__main__':
    app.run(debug=True)