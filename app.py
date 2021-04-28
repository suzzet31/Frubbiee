import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, 
    send_from_directory, jsonify, make_response)
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from jinja2 import Template
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env



UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
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


# stackflow  

@app.route("/images")
def images(x):
    """
    Dealing with Unix Path names and Windows PathNames
    """
    if platform.system() == 'Linux':
        return  x[x.rfind("/")+1:]
    return x[x.rfind("\\")+1: ]
      
def getFolder(x):
        y = []
        if platform.system() == 'Linux':
            y = x.split("/")
        else:
            y = x.split("\\")
       # print(y)
        filename_name = "images"
        if "images" in x:
            filename +="smoothie.jpg/" + y[-2]
        elif "juice.png" in x:
            filename+="cherry.jpg"
   
@app.route("/send_file/<filename>")
def send_file(filename):
   return send_from_directory(app.config["UPLOAD_FOLDER"] +"/" + getFolder(filename) , getImageName(filename))


def send_image(filename):
    try:
        pass
    except expression as identifier:
        pass
    send_images = send_image_from_directory("images", filename)
    

@app.route("/gallery")
def gallery():
    image_name = os.listdir('static/images')
    print(images)
    return render_template("gallery.html", images=images)

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template("gallery.html", upload_file=upload_file )


# youtube tutorial with Julian Nash (https://www.youtube.com/channel/UC5_oFcBFlawLcFCBmU7oNZA)

@app.route("/post/<images_id>", methods=["GET", "POST"])
def post(images_id):
    if request.method == "POST":
        submit = {
            "filename": request.form.get("images")
        }
        mongo.db.categories.update({"_id": ObjectId(images_id)}, submit)
        flash("File Successfully Uploaded")
        return redirect(url_for("add images"))

    images = mongo.db.images.find_one({"_id": ObjectId(images_id)})
    return render_template("gallery.html", images=images, upload_file=upload_file)@app.route("/register", methods=["GET", "POST"])

app.config["IMAGE_UPLOADS"] = os.path.dirname(os.abspath(__file__))
app.config["ALLOWED_IMAG_EXTENSIONS"] = ["PNG", "JPG", "JPEG" "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 *1024 *1024

def allowed_image(filename):

    if not "." in filename:
        return False

ext = filename.rsplit(".", 1)[1]

if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:

    return True
else:
    return False

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/upload-images",methods=["GET", "POST"])
def upload_images():

    if request.method == "POST":

        if request.files:
            
            if request.allowed_image_filesize(request.cookies.get("filesize")):
                print("File exceeded maximum size")
                return redirect(requst.url)
                images = request.files["images"]
            if image.filename =="":
                 print ("Image must have a filename")
                 return redirect(request.url)

            if not allowed_image(image.filename):
                
                print("That Image extension is not allowed")


            else:
                filename = secure_filename(image.filename)
                     
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], images.filename))
                filename = secure_filename(images.filename)
                     
                images.save(os.path.join(app.config["IMAGE_UPLOADS"], images.filename))
                
                print("Images saved")

        return redirect(request.url)

    return render_template("upload_images.html") 


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)