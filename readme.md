# Frubbiee 

Description
-------------

A online fresh smoothie and juice recipe platform. 

These platform will get you a ideas on how to create fresh smoothie reipes and drinks that you can share with the community.


## Table of content
---------------
* Description
* For developers
* Wireframe
* Create Mongodb account
* Create Heroku account
* Prerequisites
* create app.py using python flask framework and Materialize
* CRUD (create/read/upadate and delete)
* pages
* Running the tests
* Code languages used 
* Deployment
* Built With
* Media
* Acknowledgments

## For Developers
 Code can be written in any IDE platform 

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

`python3 -m http.server`

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

To run a backend Python file, type `python3 app.py`, if your Python file is named `app.py` of course.

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

In Gitpod you have superuser security privileges by default. Therefore you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the lessons.

### wireframe
[Frubbiee wireframe.pdf](https://github.com/suzzet31/Frubbiee/files/6412367/Frubbiee.wireframe.pdf)
Frubbiee workflow chart
[Flowchart (1).pdf](https://github.com/suzzet31/Frubbiee/files/6416110/Flowchart.1.pdf)
![Flowchart](https://user-images.githubusercontent.com/82264522/116903116-e29a3a80-ac33-11eb-8f1e-11b3e5ed3979.jpeg)
 Mock up generato page (Multi device mockup generator)[https://techsini.com/multi-mockup/index.php]
 ![Frubbiee techsini multi-mockup generator](https://user-images.githubusercontent.com/82264522/116922607-85ab7e00-ac4d-11eb-9f62-a52e86d46a11.PNG)


* 
## Create Mongodb  account

Creating an Atlas Account — Creating an Atlas Account. First, you'll need to register for a free account on the MongoDB Atlas landing page.

 
* Create Mongodb
  database
  create a database and add its first collection at the same time:
  Click Create Database to open the dialog.
  Enter the name of the database and its first collection.
*

You use MongoDB Atlas, which is a Database-as-a-Service, to create and host your Database in the cloud that stores unstructured data
The Databases tab in MongoDB Compass has a Create Database button. In MongoDB Compass, 
you create a database and add its first collection at the same time: Click Create 
Database to open the dialog. Enter the name of the database and its first collection.


Creating an Atlas Account — Creating an Atlas Account. First, you'll need to register 
for an account on the MongoDB Atlas landing pageusing your gmail account
Choose a MongoDB Atlas Cluster and Cloud Provider within your region to Create a MongoDB Atlas User Prompt
select the free cluster type by create an Atlas Free Tier C Databases and Collections

create a cluster by selecting a AWS cloud provider, region (IRELAND) cluster tier(free)
Under the admin interface in the cluster button create a cluster name of your project
Once you have created you configur the cluster.On the left column select clusters. and the main three options that we
will be mainly using are the

 - connect 
 - Metrics
 - collection

Select the  connect button 
This provides you a link that will enable you to connect your clutter to your ide platform.
By creating your cluster, we add a SCRAM username and password  that is to be stored in .gitignore folder.

Next click on 'Network Access' within the Security menu,
in order to whitelist our IP address and make sure that it has access to our database.
Click 'Add IP Address', and for now, we are going to select 'Allow Access From Anywhere',

Then click on  'Collections' button. to create our own data, 
This is where we can create our database collection  


Click on database.
Enter the Database Name and the Collection Name. Enter the Database Name and the Collection Name to create the database and create your password and the name of the data collections
Click Create. Upon successful creation, the database and the collection appears in the Data Explorer
that will be linked to the ide platform You use jinja blocks to inject content  variable blocks that generates the database in any text-based format



###  Creating Heroku account

Visit the Heroku web site.(Heroku) [ http://heroku.com.]
* Create an account
* Activate your account
* Install the Heroku CLI.
* Add your SSH key to your Heroku account


Heroku is a cloud platform t cloud platforms,  enables each developer to  deploy apps in any other languages. 

First we need to do is create an account! Once we have created the accunt according to our location based and the requirements.
We will need to create our configurations under settings you will see a button labled `reveal config vars`.
Once you click on the button. You will open a new page. and add in IP number,your secret key, port, the Mongodb account address name, an d your Mongo_db_uri connecting link that contains your password and your username. 
It is very important to note your password and your mongo db username. This will be the same key and password that is used in the ide platform as well as your mongodb account.

The next step is you ned to save and click the  hide the Config vars button.

You will be directed back to the settings page on the top of the page select the deploy button. 
* Under deployment method there are different ways to deploy your page. 
  - GHeroku git
  - Guthub
  - container registry
* we are going to select the Github connect. to connect with your github account make sure that you are logged in to github,this this will enable you to connect to your github account.
* Once you connected to your github  account, select your repository to connect.
* Once coonected select enable automatic deployment button then give it a few munites to connect and collect data to the heroku cloud.  
* This takes a few minutes. Once it is done your will receive a message to state whether your site is enabled and deployed . 



### wireframe
[Frubbiee wireframe.pdf](https://github.com/suzzet31/Frubbiee/files/6412367/Frubbiee.wireframe.pdf)
Using the (mockflow website) [https://www.mockflow.com/app/#Wireframe]

###  Give examples

Installing
=======
To create a base template we need to install diffrent python functionalities to create a CRUD working platform.
To do this we need to install.
* pip3 flask-pymongo
* pip3 jinja framework
* pip3 dsnpython
* pip3 flask
* pip3 reeze --local > command
* create echo : web requirement.txt
* External API 

A step by step series of examples that tell you how to get a development env running
*  
### create app.py using python flask framework and Materialize 
T
Flask allows us to build web apps to use it we need to installl python flask in the ide terminal. that will enable us to create a flask app that is used to create this website
By creating a base template and using {% extends 'base.html' %} in a child template and closing {% endblock %} after that.
To refrence the pages in our files that are within our own repository, we must use the url_for() function.
url_for('static', filename=, and then just the link that's already provided.


Say what the step will be
## CRUD (create/read/upadate and delete)

Create a base template we need to install diffrent python functionalities to create a CRUD working platform referencing the base templates using the terminal point.

 ##### pages
 
  * Home page
  * Frubbie page(recipe page)
  * Gallery page
  * Log in
  * Register
  * Manage categories
  * Log out page
  * search page
  
  
 The below functionality are accessible inthe following pages
 
 * Create recipe in the new recipe page 
 * Read page the recipe(frubbiee page)
 * Update recipes/category pages by using the edit/cancel butons
 * Delete pages/categories/recipes using the delete functionalities in the cancle and done button


When a user submits an edit task form, they are sending their updated task data to the database

### Running the tests
To run the automated tests for this system
I used instant access to our real device cloud using the OS version, through the computer webpage, 
by selceting the developer inspect property to initiate the page into different respirotory sizes as the  Galaxy, iPhone, Huawei, Pixel, OnePlus, Xiaomi, etc.

before testing  on real devices to enabe me to deliver a high-quality customer experience by using the autometed real such as android and iOS devices.

Remotely control our devices for manual app testing to troubleshoot issues reported by your customers and verify the real-world user experiences such as the colours , the interfaces and the button functioalities that i was able to fix using the meterialized snippets.



### Code languages used 
And coding style tests
 in app.py , add code to import Flask and create an instance of the Flask object. Using the correct packages using the 
 the __name__ variable.
 Language used are. 
 * `HTML
 * `CSS
 * `Javascript
 * `Python Flask
 

### Deployment
Add additional notes about how to deploy this on a live system

Run the python3 app.py command. 

After adding the git add and git commit command, push your code to your repository's
github master or main branch or to your heroku remote master. 

* To deploy your app to Heroku. 

* Within our terminal we need to log from the CLI and then add heroku commands to access different pieces of functionality by
going back to the full-width Terminal and install Heroku,

* Type: npm install -g heroku.

* Once that finishes installing, we can login to Heroku using the command: heroku login -i.

* Use your heroku logins details that is created to access  Heroku account  . 

* Type: heroku apps: 

 * The first URL there is our live  link you use to for deployment.

### Built With

  Mongodb database collection
  Heroku cloud database
  Flask framework
  jinja templates
  werkzeug used togenerate password
  bson for identifying object id's
  Gitpod ide platform
  Github 
  Python flask framework
  pymomgo
  

## trouble shooting

* Kept on getting the favicon.ico HTTP/1.1" 404. 

I did a serach on stackover flow and nside head tag I added the 

`<link href='ico/favicon.ico' rel='icon'>` link
 
Import flask os links that are used
-------------
<!-- pip3 install  -->
*  Flask PyMongo  - The web framework used
* Mongo db - Dependency Management
* Jinja- Used to generate framework
* pymongo
* pip3 freeze -- 
* requirements txt
* install dependsng
* Flask
* flash
* render_template,
* redirect
* request
* session
* url_for, 
* send_from_directory
* make_response
* send_file
* flask_admin    
* flask_pymongo
* bson.objectid imported ObjectId
* from werkzeug.security imported generate_password_hash, check_password_hash
*  environ


Media
------------
* Google media  select tools button under usage rights select any of the 

 - Creative Commons licenses
 - Commercial & other licenses 

   * [https://images.unsplash.com/photo-1589734580748-6d9421464885?ixid=MnwxMjA3fDB8MHxzZWFyY2h8N3x8c21vb3RoaWV8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60]
                
   * [https://media.istockphoto.com/photos/healthy-appetizing-red-smoothie-dessert-in-glasses-picture-id1081369140?k=6&m=1081369140&s=612x612&w=0&h=FQaF-nWUJ4nO0H-k5lrlNj1SGloF4SnDePTxdDSRUds=]
             
   * [https://images.immediate.co.uk/production/volatile/sites/30/2020/08/3._healthy_ingredients_for_smoothie-b0c5bd6.jpg?quality=90&resize=960,872]

                   
   * [https://media.istockphoto.com/photos/raspberry-smoothies-and-raspberry-fruit-on-the-concrete-background-picture-id1165901530?k=6&m=1165901530&s=612x612&w=0&h=lTD1JB_C1TKA0yQ2GszOKx6AXC9GMEAROqNdJ1B3CZQ=]


* And unsplashed images
 
                   
 [https://images.unsplash.com/photo-1553530666-ba11a7da3888?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8c21vb3RoaWV8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60]

 Acknowledgments
-------------------
Hat tip to anyone whose code was used
* The code institute tutorial by `Mr. Tim Nelson`
* All the code institute tutors 
*  [Mr. Can Casullu]  My mentor thankj you for putting up with me
* The care support team especially [Mark] who has always there to recieve my calls.
* Tutor team
* stackflow 
* youtube tutorial with Julian Nash (https://www.youtube.com/channel/UC5_oFcBFlawLcFCBmU7oNZA
Inspiration
etc
