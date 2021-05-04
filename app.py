import os
import pymongo
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, 
    send_from_directory, make_response, send_file,)
from flask_admin import Admin   
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")



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


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
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
            "prep_time": request.form.get("prep_time"),
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



@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Successfully Deleted")
    return redirect(url_for("get_categories"))


# stackflow  



@app.route("/gallery")
def gallery():
        images = os.listdir('static/images')
        if request.method == "POST":
            images = {
                "filename": request.form.get("filename")
            }
            mongo.db.images.select( upload_images)
            flash("File Successfully Uploaded")
            return redirect(url_for("filename"))

        filename = mongo.db.filename.find_one()
        return render_template("gallery.html", filename=filename)


@app.route("/image.jpg")
def image():
    return render_template("image.jpg")




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)