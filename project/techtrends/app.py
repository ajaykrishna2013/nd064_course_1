import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

def get_pos_count():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return len(posts)


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
connection_count = 0

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.error("Post {} does not exist".format(post_id))
        return render_template('404.html'), 404
    else:
        app.logger.info("Article {} retrieved!".format(post['title']))
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("About Us page retrieved!")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info("Article {} created".format(title))

            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def healthz():
    return jsonify({"result": "OK - health"}), 200


@app.route('/metrics')
def metrics():
    post_count = get_pos_count()
    return jsonify({
        "db_connection_count" : connection_count,
        "post_count": post_count}), 200



# start the application on port 7111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='7111')
