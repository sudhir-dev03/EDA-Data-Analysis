from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123@Faujdar",
    database="formdb"
)

cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    age = request.form['age']
    gender = request.form['gender']
    city = request.form['city']

    query = """
        INSERT INTO users (name, email, phone, age, gender, city)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (name, email, phone, age, gender, city)

    cursor.execute(query, values)
    conn.commit()

    user_id = cursor.lastrowid  

    return redirect(url_for('extra_form', user_id=user_id))

@app.route('/extra/<int:user_id>')
def extra_form(user_id):
    return render_template('extra.html', user_id=user_id)


@app.route('/submit_extra/<int:user_id>', methods=['POST'])
def submit_extra(user_id):
    course = request.form['course']
    hobby = request.form['hobby']
    experience = request.form['experience']

    query = """
        INSERT INTO user_extra (user_id, course, hobby, experience)
        VALUES (%s, %s, %s, %s)
    """

    values = (user_id, course, hobby, experience)

    cursor.execute(query, values)
    conn.commit()

    return "Data stored successfully in BOTH tables"


if __name__ == '__main__':
    app.run(debug=True)