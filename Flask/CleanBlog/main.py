from flask import Flask, render_template, request
import requests, os, smtplib
from dotenv import load_dotenv

load_dotenv()

FROM_ADDR = os.getenv('GMAIL_ACCOUNT')
TO_ADDRS = ['manch.hon@gmail.com',]
PYTHON_APP_GMAIL_CODE = os.getenv('PYTHON_APP_GMAIL_CODE')

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    # response = requests.get('https://api.npoint.io/674f5423f73deab1e9a7')
    response = requests.get('https://api.npoint.io/933313e36c95a0378f7b')
    posts = response.json()
    return render_template('/index.html', posts=posts)
    # return render_template('index.html')

@app.route('/about')
def about():
    return render_template('/about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    method = request.method
    if method == 'POST':
        subject = 'New Customer Contact Form'
        body = f'''Customer Contact Form\n\n
        Name: {request.form['name']}\n
        Email: {request.form['email']}\n
        Phone: {request.form['phone']}\n
        Message: {request.form['message']}\n
        \n\n'
        '''
        msg = f"Subject:{subject}\n\n{body}"
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=FROM_ADDR, password=PYTHON_APP_GMAIL_CODE)
            for recipent in TO_ADDRS:
                connection.sendmail(from_addr=FROM_ADDR, to_addrs=recipent, msg=msg)

    return render_template('/contact.html', method=method)
    # if method == 'GET':
        
    # else:
    #     name = request.form['name']
    #     email = request.form['email']
    #     phone = request.form['phone']
    #     message = request.form['message']
    #     print(f'name: {name}  email: {email} phone: {phone}  message: {message}')
    #     return "<h1>Successfully sent your message</h1>"

@app.route('/post/<int:post_id>')
def post(post_id):
    # response = requests.get('https://api.npoint.io/674f5423f73deab1e9a7')
    response = requests.get('https://api.npoint.io/933313e36c95a0378f7b')
    posts = response.json()
    post = None
    for p in posts:
        if p['id'] == post_id:
            post = p
            break
    return render_template('/post.html', post=post)

# @app.route('/process_form', methods=['POST'])
# def process_form():
#     name = request.form['name']
#     email = request.form['email']
#     phone = request.form['phone']
#     message = request.form['message']
#     print(f'name: {name}  email: {email} phone: {phone}  message: {message}')
#     return "<h1>Successfully sent your message</h1>"


if __name__ == '__main__':
    app.run(debug=True)