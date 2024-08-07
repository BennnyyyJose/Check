from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import hashlib
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=5)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="checkmate_db"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute('SELECT * FROM users WHERE (username = %s OR user_id = %s) AND password = %s', 
                       (identifier, identifier, hashed_password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials, please try again.'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['userid']
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute('SELECT * FROM users WHERE username = %s OR user_id = %s', (username, user_id))
        existing_user = cursor.fetchone()

        if existing_user:
            return 'Username or User ID already exists. Please choose a different one.'

        cursor.execute('INSERT INTO users (user_id, username, password) VALUES (%s, %s, %s)', 
                       (user_id, username, hashed_password))
        db.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()
    return render_template('dashboard.html', projects=projects)

@app.route('/projects')
def projects():
    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()
    return render_template('projects.html', projects=projects)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']

        cursor.execute('INSERT INTO projects (project_name, project_description) VALUES (%s, %s)', 
                       (project_name, project_description))
        db.commit()
        return redirect(url_for('projects'))

    return render_template('add_project.html')

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    cursor.execute('DELETE FROM projects WHERE id = %s', (project_id,))
    db.commit()
    return redirect(url_for('projects'))

@app.route('/project/<int:project_id>')
def project_details(project_id):
    cursor.execute('SELECT * FROM projects WHERE id = %s', (project_id,))
    project = cursor.fetchone()
    if project:
        return render_template('project_details.html', project=project)
    else:
        return 'Project not found.'

@app.route('/category/<string:category_name>')
def category_details(category_name):
    cursor.execute('SELECT category_name, wstg_id, test_name, objectives, tools, owasp_top_10, cwe, result, affected_item_url, status FROM test_cases WHERE category_name = %s', (category_name,))
    test_cases = cursor.fetchall()
    return render_template('category_details.html', category_name=category_name, test_cases=test_cases)

@app.route('/update_test_case', methods=['POST'])
def update_test_case():
    category_name = request.form.get('category_name', '')
    test_case_id = request.form.get('test_case_id', '')
    result = request.form.get('result', '')
    affected_item_url = request.form.get('affected_item_url', '')
    status = request.form.get('status', '')

    try:
        test_case_id = int(test_case_id)  # Ensure test_case_id is an integer
        cursor.execute('UPDATE test_cases SET result = %s, affected_item_url = %s, status = %s WHERE id = %s',
                       (result, affected_item_url, status, test_case_id))
        db.commit()
        return redirect(url_for('category_details', category_name=category_name))
    except ValueError:
        return "Invalid test case ID or data", 400
    except mysql.connector.Error as err:
        return f"Error: {err}", 400


@app.route('/learning_notes')
def learning_notes():
    if 'user_id' in session:
        cursor.execute('SELECT id, topic FROM learning_notes WHERE user_id = %s', (session['user_id'],))
        notes = cursor.fetchall()
        return render_template('learning_notes.html', notes=notes)
    return redirect(url_for('login'))

@app.route('/add_topic', methods=['POST'])
def add_topic():
    if 'user_id' in session:
        user_id = session['user_id']
        topic = request.form['topic']
        cursor.execute('INSERT INTO learning_notes (user_id, topic, note) VALUES (%s, %s, %s)', (user_id, topic, ""))
        db.commit()
        return redirect(url_for('learning_notes'))
    else:
        return redirect(url_for('login'))

@app.route('/note/<int:note_id>')
def view_note(note_id):
    cursor.execute('SELECT id, topic, note FROM learning_notes WHERE id = %s', (note_id,))
    note = cursor.fetchone()
    if note:
        return render_template('note.html', note={'id': note[0], 'topic': note[1], 'note': note[2]})
    return 'Note not found'

@app.route('/save_note', methods=['POST'])
def save_note():
    note_id = request.form.get('note_id')
    note_content = request.form.get('note_content')

    if note_id:
        try:
            note_id = int(note_id)
            cursor.execute('UPDATE learning_notes SET note = %s WHERE id = %s', (note_content, note_id))
            db.commit()
            message = "Note saved successfully!"
            return redirect(url_for('view_note', note_id=note_id, message=message))
        except ValueError:
            return "Invalid note ID", 400
    else:
        return "Note ID is missing", 400

    return redirect(url_for('view_note', note_id=note_id))

@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    cursor.execute('DELETE FROM learning_notes WHERE id = %s AND user_id = %s', (note_id, session['user_id']))
    db.commit()
    return redirect(url_for('learning_notes'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
