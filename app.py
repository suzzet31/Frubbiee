import os
import pymongo
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, 
    send_from_directory, jsonify, make_response, send_file)
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from jinja2 import Template
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
if os.path.exists("env.py"):
    import env


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__, static_url_path='')


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]



mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    index = list(mongo.db.index.find())
    return render_template("index.html", index=index )


@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/get_recipes//<search_recipe>")
def search_recipe(search_word):
    cursor = recipes.find({'$text': {'$search': search_word}})
    result = []
    for data in cursor:
        result.append(data)
    return result
    def convert_result_to_message(result):
        if len(result) == 0:
            return "Sorry, we currently don't have any recipe pertaining to your smoothie."
    message = ""
    for data in result:
        message += f"Food: {data['name']}\n"
        message += "Steps\n"
        count = 1
        for step in data['steps']:
            message += f"{count}. {step}\n"
            count += 1
        message += '\n\n'
        flash("thank you for your request")
        return render_template("recipes.html", recipes=recipes)


@app.route("/register")
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("profile.html", username=username)



@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recipes", methods=["GET","POST"])
def add_recipes():
    if request.method == "POST":
        my_favourite = "on" if request.form.get("my_favourite") else "off"
        recipes = {
            "category_name": request.form.get("category_name"),
            "main_ingredient": request.form.get("main_ingredient"),
            "smoothie_name": request.form.get("smoothie_name"),
            "recipe_description": request.form.get("recipe_description"),
            "type_of_equipments": request.form.get("type_of_equipments"),
            "pre_time": request.form.get("pre_time"),
            "my_favourite": my_favourite,
            "created_by":session["user"]
        }
        mongo.db.recipes.insert_one(recipes)
        flash("Drink Successfully Added")
        return redirect(url_for("get_recipes"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_recipes.html", categories=categories)



@app.route("/edit_recipes/<recipes_id>", methods=["GET","POST"])
def edit_recipes(recipes_id):
    if request.method == "POST":
        my_favourite = "on" if request.form.get("my_favourite") else "off"
        submit = {
            "category_name": request.form.get("category_name"),
            "main_ingredient": request.form.get("main_ingredient"),
            "smoothie_name": request.form.get("smoothie_name"),
            "recipe_description": request.form.get("recipe_description"),
            "type_of_equipments": request.form.get("type_of_equipments"),
            "pre_time": request.form.get("pre_time"),
            "my_favourite": my_favourite,
            "created_by":session["user"]
         }
        mongo.db.recipes.update({"_id": ObjectId(recipes_id)}, submit)
        flash("Drink Successfully updated")
        
    recipes = mongo.db.recipes.find_one({"_id": ObjectId(recipes_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_recipes.html", recipes=recipes, categories=categories)


@app.route("/delete_recipes/<recipes_id>")
def delete_recipes(recipes_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipes_id)})
    flash("Recipes Successfully Deleted")
    return redirect(url_for("get_recipes"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html",categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added")
        return redirect(url_for("get_categories"))


        return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Successfully Updated")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method =="POST":
        flash("Thanks {}, we have received your message!".format(
        request.form.get("name")))
        mongo.db.recipes.remove({"_id": ObjectId(posts_id)})
    flash("Your message has being sent")
    return render_template("contact.html", page_title="Contact")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Files successfully uploaded')
        return redirect('/')

@app.route('/foo', methods=['GET'])
def foo():
    for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            if file.endswith('B4.TIF'):
                fname4 = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if file.endswith('B5.TIF'):
                fname5 = os.path.join(app.config['UPLOAD_FOLDER'], file)

    bytes_obj = plot(fname4,fname5)

    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')


# stackflow  

@app.route("/""/<filename_local>")
def myfiles(filename_local):
    return send_from_directory("/index", filename_local)

    
@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(directory_to_image_folder, filename, as_attachment=True)


@app.route("/send_file/<filename>")
def send_file(filename):
   return send_from_directory(app.config["UPLOAD_FOLDER"] +"/" + getFolder(filename) , getImageName(filename))



@app.route("/upload/<images>", methods=["GET", "POST"])
def upload(images):
    if request.method == "POST":
        submit = {
            "images": request.form.get("filename")
        }
        # check if the post request has the file part
        if 'images' not in request.files:
            flash('No file part')
            return redirect(request.url)
        images = request.files['filename']
        # if user does not select file, browser also
        # submit a empty part without filename
        if images.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(images.filename):
            filename = secure_filename(images.filename)
            file.save(os.path.join(app.config['upload_folder'], filename))
            return render_template("upload.html",upload=upload, upload_file=upload_file , images = images )
    
        mongo.db.images.update({"_id": ObjectId(filename_id)}, submit)
        flash("images Successfully Updated")
        return redirect(url_for("gallery.html"))
        
    images = mongo.db.users.find_one({"images": session["user"]})["images"]
    return render_template("upload.html", images=images)    


@app.route("/gallery")
def gallery():
    images = os.listdir('static/images')
    if request.method == "POST":
        images = {
            "filename": request.form.get("images")
        }
        mongo.db.images.select( upload_images)
        flash("File Successfully Uploaded")
        return redirect(url_for("filename"))

    filename = mongo.db.filename.find_one()
    return render_template("gallery.html", filename=filename, upload_file=upload_file)

    print(images)
    return render_template("gallery.html", images=images)
    form = AddRecipe()
    user = User.query.filter_by(id=current_user.id).first()
    imagesList = []

    if request.method == 'POST' and 'image[]' in request.files:
        if form.validate_on_submit():
            product = recipe()
            file = request.files.getlist("image[]")
            for zipfile in file:
                filename = zipfile.filename.split('/')[0]
                zipfile.save(os.path.join(UPLOAD_FOLDER, filename))
                imagesList.append(filename)

            product.images = imagesList[imagesList]
            db.session.add(image)
            db.session.commit()

            flash('Images Uploaded', 'success')
            return redirect(url_for('master.index'))

    else:
        return render_template('add-recipes.html', form=form)
    return render_template('add-recipes.html', form=form, action='add')
 

@app.route("/upload_folder")
def upload_folder():
    try:
        return database_upload_folder()
    except DatabaseError as e:
        app.logger.exception(e)
        return "Can not upload folder"


# youtube tutorial with Julian Nash (https://www.youtube.com/channel/UC5_oFcBFlawLcFCBmU7oNZA)

app.config["ALLOWED_IMAG_EXTENSIONS"] = ["PNG", "JPG", "JPEG" "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 *1024 *1024

def allowed_image(filename):

    if not "." in filename:
        def allowed_image_filesize(filesize):
             if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
                 return render_template("gallery.html", images=images, upload_file=upload_file)@app.route("/register", methods=["GET", "POST"])
 

@app.route("/images")
def images(filename):
    return send_from_directory("/images", filename=filename)

app.route("/images/<filename>")
def images(filename):
        if request.method =="POST":
          like = "on" if request.form.get("like") else "off"
          filename = {
            "images.filename": request.form.get("filename"),
            "images.comment": request.form.get("commentt"),
            "images.like": like,
            "created_by":session["user"]
            }
          mongo.db.images.upload({"_id": ObjectId(images_id)}, filename)
          flash("Image Successfully uploaded")

          filename = mongo.db.filename.find().sort("filename", 1)
          return render_template("images.html", images=images, filename=filename)

@app.route("/get_images")
def get_images():
    recipes = list(mongo.db.images.find())
    return render_template("images.html", images=images)


@app.route("/get_images//<search_images>")
def search_images(search_word):
    cursor = images.find({'$text': {'$search': search_word}})
    result = []
    for data in cursor:
        result.append(data)
    return result
    def convert_result_to_message(result):
        if len(result) == 0:
            return "Sorry, we currently don't have any images pertaining to your smoothie."
    message = ""
    for data in result:
        message += f"Food: {data['name']}\n"
        message += "Steps\n"
        count = 1
        for step in data['steps']:
            message += f"{count}. {step}\n"
            count += 1
        message += '\n\n'
        flash("thank you for your request")
        return render_template("images.html", images=images)




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)