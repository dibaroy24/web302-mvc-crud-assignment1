# Creating a Controller for our Car Model which will control the flow of data
# from the Model to the View and back

# Import the Flask class as well as required corresponding functions from the
# flask package, model form our models module, classes from our forms module,
# and objects from our settings module
from flask import Flask, render_template, request, redirect
from models import Car
from forms import CarForm, EditCarForm, DeleteCarForm
from settings import site_title, mydb, mycursor

# Creating a new instance of the Flask class usign the __name__ attribute as
# the parameter
app = Flask(__name__)

# Adding a function which will load an Add Car page with a form which will
# allow the user to add a new car
@app.route('/add-car')
def add():
    # Using get() method of the args property of the request object to collect
    # GET data from the URL
    get = {
        "add": request.args.get("add")
    }

    # Creating a new instance of our CarForm class with csrf_enabled set to
    # False
    form = CarForm(csrf_enabled=False)

    # Passing our get and form variables to the Jinja template
    return render_template(
        "add-car.html.j2",
        site_title = site_title,
        page_title = site_title + " - Add Car",
        get = get,
        form = form
    )

# The create() function will use the app.route decorator to point to address
# but must have another paramter of methods=('GET', 'POST') to accept
# data from GET requests and POST requests
@app.route("/create-car", methods=('GET', 'POST'))
def create():
    # Create a new instance of our CarForm class using the request.form
    # object which will get the request method (GET or POST) as the first
    # parameter
    form = CarForm(request.form, csrf_enabled=False)

    # To check if our require fields have been filled out and then create a new
    # instance of our Car class and its contructor method will take the form
    # object
    if form.validate_on_submit():

        car = Car(form)

        # Since, our object has been created; use an INSERT INTO statement to
        # add the object's properties to our database
        query = "INSERT INTO `cars` (`name`, `image`, `topspeed`) VALUES (%s, %s, %s)"
        # query = "INSERT INTO `cars` (`name`, `image`, `topspeed`) VALUES (%s, %s, %d)"
        value = (car.name, car.image, car.topspeed)
        mycursor.execute(query, value)
        mydb.commit()

        # If the required fields have been filled out add the car to the
        # database and redirect to the View Cars page with GET data to
        # display a success message, else go back to the Add Car page with
        # GET data to display an error message
        return redirect('/?add=success')
    else:
        return redirect('/add-car?add=error')

# The read() function will be used to retreive data from the database and
# display it on a View Cars page using the get() again
@app.route("/")
def read():
    get = {
        "add": request.args.get("add"),
        "edit": request.args.get("edit"),
        "delete": request.args.get("delete")
    }

    # Using a SELECT * FROM statement to collect all of the rows
    # in the database and the fetchall method to return them in a dictionary
    query = "SELECT * FROM `cars`"
    mycursor.execute(query)

    cars = mycursor.fetchall()

    # The View Cars page will also have a delete button which will allow
    # the user to delete a car
    # Therefore we will need to create a new instance of our DeleteCarForm
    # class
    form = DeleteCarForm(csrf_enabled=False)

    # Placing the topspeed variable in a LIST to work on the maximum value
    # and display it on the application

    speeds = []

    for car in cars:
        speeds.append(car['topspeed'])

    # Finally we will pass our get, cars, and form variables to the Jinja
    # template

    return render_template(
        "view-cars.html.j2",
        site_title = site_title,
        page_title = site_title + " - View Cars",
        get = get,
        cars = cars,
        form = form,
        speeds = speeds
    )

# The edit() function which will load and Edit Car page with a form which will
# allow the user to edit an existing car using the get method to collect GET
# data from the URL
# This data will be used to check if there are any errors when the form
# is submitted as well as to get the ID of the spefcific car we are
# editing
@app.route("/edit-car")
def edit():
    get = {
        "edit": request.args.get("edit"),
        "id": request.args.get("id")
    }

    # Using a SELECT * FROM statement and interpolate the ID which was passed
    # to the script with GET data to find the matching darabase row using the
    # WHERE clause
    query = f"SELECT * FROM `cars` WHERE id='{get['id']}'"
    mycursor.execute(query)

    car = mycursor.fetchone()

    # Then create a new instance of our EditCarForm class and set
    # csrf_enabled to false
    form = EditCarForm(csrf_enabled=False)
    # This will allow us to set the values of each form field to the already
    # existing values which are stored in the database by assining the data
    # attribute of each attribute of the form object to the corresponding values
    # of the car object
    form.name.data = car["name"]
    form.image.data = car["image"]
    form.topspeed.data = car["topspeed"]
    # The ID attribute will be sent using the ID which is passed to the Edit
    # Car page using a link with GET data
    form.id.data = get["id"]

    # Passing our get, car and form variables to the Jinja template
    return render_template(
        "edit-car.html.j2",
        site_title = site_title,
        page_title = site_title + " - Edit " + car["name"],
        car = car,
        get = get,
        form = form
    )

# The update() function will process the data from our form and will redirect
# to a different address using methods=('GET', 'POST') to accept data from GET
# requests and POST requests
@app.route("/update-car", methods=("GET", "POST"))
def update():
    # Then we will create a new instance of our EditCarForm class
    form = EditCarForm(request.form, csrf_enabled=False)
    # Retreive the ID of the car which is being updated by accessing the data
    # attribute of the id attribute of form object which is actually coming
    # from POST
    id = form.id.data

    # To check if our required fields are filled out
    if form.validate_on_submit():
        # Create a new instance of our Car class and its constructor method
        # which will take the form object
        car = Car(form)

        # Since, our object has been created; use an UPDATE statement and
        # interpolate the ID of the car to find a matching database row
        query = f"UPDATE `cars` SET name=%s, image=%s, topspeed=%s WHERE id={id}"
        value = (car.name, car.image, car.topspeed)
        mycursor.execute(query, value)
        mydb.commit()

        # If the required fields have been filled out update the car in the
        # database and redirect to the View Cars page with GET data to display
        # a success message
        return redirect('/?edit=success')
    else:
        # The ID of the item needs to be passed back to the edit page so that
        # it can display the data.
        return redirect(f"/edit-object?edit=error&id={id}")

# The delete() function will need to collect the ID of the car from form to
# identify which car we are deleting
@app.route("/delete-car", methods=("GET", "POST"))
def delete():
    form = DeleteCarForm(csrf_enabled=False)
    id = form.id.data

    if form.validate_on_submit():
        # To ensure that the ID has been submited, use a DELETE statement and
        # interpolate the ID of the car to find a matching database row using
        # the WHERE clause to delete a row
        query = f"DELETE FROM `cars` WHERE id='{id}'"
        mycursor.execute(query)
        mydb.commit()

        return redirect("/?delete=success")
    else:
        return redirect('/?delete=error')
