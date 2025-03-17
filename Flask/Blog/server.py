from flask import Flask, render_template
import requests
from post import Post

app = Flask(__name__)
posts = {}

@app.route('/')
def home():
    response = requests.get('https://api.npoint.io/c790b4d5cab58020d391')
    response.raise_for_status()
    data = response.json()
    print(data)
    for post in data:
        posts[post['id']] = Post(post['id'], post['title'], post['subtitle'], post['body'])
    # posts = [Post(post['id'], post['title'], post['subtitle'], post['body']) for
    #          post in data]
    return render_template('index.html', posts=posts.values())

@app.route('/post/<int:id>')
def get_post(id):
    if id in posts:
        post = posts[id]
        return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)

