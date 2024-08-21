from flask import Flask, abort, flash, make_response, render_template, request, send_from_directory, session, redirect, url_for
import os
import sqlite3
from werkzeug.security import generate_password_hash,  check_password_hash
from werkzeug.utils import secure_filename
# from werkzeug.security import generate_password_hash 
app = Flask(__name__)
app.config[ "SESSION_PERMANENT" ] = False
app.config[ "SESSION_TYPE" ] = "filesystem"
app.secret_key = "loginwithsessions"# Secret key for session management
 
    





@app.route('/')
def home():
    if not session.get('logged_in') :
        return render_template('login.html')
    else:
        # Display Products
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        db.commit()
        db.close()
        # print(products)
        return render_template("home.html", products=products)

      








# Create Tabels 
db = sqlite3.connect('data/myData.db')
cursor = db.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE
        )
    ''')
cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            image BLOB NOT NULL
        )
    ''')
db.commit()
db.close()






# Define a function to get the database connection
def get_db():
    db = sqlite3.connect('data/myData.db')
    return db








#Login

# Check If The Input User Existing In The database or Not
def check_user(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    db.close()

    if user is not None:
        stored_password_hash = user[0]
        return check_password_hash(stored_password_hash, password)
    else:
        return False

@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form.get("username").lower()
    password = request.form.get("password")
    result = check_user(username, password)
    # Validate login credentials (for demonstration purposes)
    if (result):
        session['logged_in'] = True
          # Set a cookie with user information
        response = make_response(redirect(url_for('home')))
        response.set_cookie('username', username)
        return response
    else:
         error = 'Name or password is not valid.'
         return render_template('login.html', error=error)
    #    return abort(403, "Wrong username or password")



# Delete session Here and, Delete The Cookie From The User's Browser By Js 
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')
    # return redirect(url_for('login'))





# Define the signup route
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    error = ''
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        email = request.form['email']

        # Basic input validation
        if not username or not password or not email:
            error = 'All fields are required.'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters.'

        # Check if user already exists 
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            error = 'User already exists.'

        if error is '':
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                           (username, hashed_password, email))
            db.commit()
            db.close()
            return render_template('login.html')  # Replace with success page

        flash(error)

    return render_template('signup.html', error=error)





# Users Dashboard 
@app.route("/users_dashboard")
def users_dashboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print(users)
    db.commit()
    db.close()
    return render_template("users_dashboard.html", users=users)

# Delete User With Id 

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    db.close()
    return redirect(url_for('users_dashboard'))



    


# Show Data User  
@app.route('/edit_user/<int:user_id>')
def edit_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    db.close()
    return render_template('edit_user.html', user=user)





@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    # Get the request data
    username = request.form['username'].lower()
    email = request.form['email']

    # Update the user data
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE users SET username = ?, email = ? WHERE id = ?', (username, email, user_id))
        db.commit()
        db.close()
        return redirect(url_for('users_dashboard'))
    except Exception as e:
        # Log the error and return a 400 error response
        print(f'Error updating user: {e}')
        return render_template('404.html'), 404






# Products Dashboard
@app.route("/products_dashboard")
def products_dashboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return render_template("products_dashboard.html", products=products)

# Add Product 
@app.route("/add_product")
def add_product():
    return render_template('add_product.html')



# Upload File 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(APP_ROOT,
'static/Images')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024**2 ## 5MB


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        product_title = request.form['title']
        product_price = request.form['price']
        product_image = request.files['image']

        # print("Upload folder:", app.config['UPLOAD_FOLDER'])
        # print("File name:", product_image.filename)

        # Check if an image was uploaded
        if product_image.filename == '':
            return 'No image uploaded', 400

        # Validate file type and size
        if product_image.filename != '' and product_image.filename.split('.')[1] in ['jpg','jpeg', 'webp', 'png', 'gif']:
            if product_image.content_length <= app.config['MAX_CONTENT_LENGTH']:
                # Save the file
                try:
                    with open(os.path.normpath(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(product_image.filename))), 'wb') as f:
                      f.write(product_image.read())
                    print("File saved successfully")
                except Exception as e:
                    print("Error saving file:", e)

                # Insert data into database
                db = get_db()
                cursor = db.cursor()
                cursor.execute('INSERT INTO products (title, price, image) VALUES (?, ?, ?)', (product_title, product_price, product_image.filename))
                db.commit()
                db.close()

                return redirect(url_for('products_dashboard'))
            else:
                return 'File size exceeds the maximum limit', 400
        else:
            return 'Invalid file type', 400

    return render_template('add_product.html')


#Download Image Product
@app.route('/downloader/<int:product_id>', methods=['GET', 'POST'])
def download_file_server(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT image FROM products WHERE id = ?', (product_id,))
    image_name = cursor.fetchone()[0]
    db.close()

    return send_from_directory(app.config['UPLOAD_FOLDER'], image_name, as_attachment=True)





# Delete Product 
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT image FROM products WHERE id = ?', (product_id,))
    image_name = cursor.fetchone()[0]
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    db.commit()
    db.close()

        # Delete the image from the folder
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    if os.path.exists(image_path):
        os.remove(image_path)
    return redirect(url_for('products_dashboard'))


     #View Product
@app.route('/view_product/<int:product_id>')
def view_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    db.commit()
    db.close()
    return render_template('view_product.html', product=product)

# Main
if __name__ == "__main__":
    app.run(debug=True)




