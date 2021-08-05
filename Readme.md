# Full Stack Capstone Project

The Restruant API supports a basic Restruant by allowing users to query the database to preview the Menu or to book a table. There are 3 different user roles (and related permissions), which are:

Public user: Can view the menu and book a table.
Reservation manager: Can view a all reservations details.
Menu manager: Can add or delete dishes from the Menu.


##Running the API 
API endpoints can be accessed via https://restaurant-fsnd-capstone.herokuapp.com/

Auth0 information for endpoints that require authentication can be found in setup.sh.


## Installing Dependencies 

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Testing
To run the tests, run the postman collectection file in postman [Restraunt.postman_collection](https://)

## API Reference

### Error Handling
Errors are returned as JSON in the following format:
```
{
	"success": False,
	"error": 422,
	"message": "Unprocessable: " 
}

{
	"success": False, 
	"error": 404,
	"message": "Not found"
}
```
The API will return two types of errors:
- 404 – resource not found
- 422 – unprocessable

### Endpoints
### public Endpoints
#### GET /
- General:
  - Returns a welcome message
```
{
    'message': 'hello from restraunt API'
}
 ```
#### GET /menu
- General:
  - Returns a list of dishes
  - Results are paginated in groups of 3.
 ```
 {
    "dishes": [
        {
            "category": "Pizza",
            "description": "Tomato sauce, Mozzarella, Cantal cheese and oregano",
            "dish_name": "Margherita Pizza",
            "id": 1,
            "price": "25$"
        },
        {
            "category": "Pizze",
            "description": "Tomato sauce, Mozzarella, and olives",
            "dish_name": "vegtables Pizza",
            "id": 2,
            "price": "30$"
        },
        {
            "category": "Cold Drinks",
            "description": "Fresh Mango juice",
            "dish_name": "Mango juice",
            "id": 3,
            "price": "11$"
        }
    ],
    "success": true,
    "total_dishs": 8
}
 ```

#### POST /book
- General:
  - Book a table by providing email, Guest name, Chairs number, and date & Time.
  - Returns a massage and success value.

 ```
 {
    "message": "The table was reserved successfully ",
    "success": true
}
 ```
### [Reservation manger] Endpoints
#### GET /<string:user>/reservation
- General:
  - returns a list of reservations for specific user
  - requires  ```'read:reservation'``` permission
 ```
{
    "reservation": [
        {
            "appointmentـTime": "Mon, 02 Aug 2021 00:28:42 GMT",
            "table_id": 2
        }
    ],
    "success": true
}
 ```
#### GET /reservation-detail
- General:
  - returns a list of reservations for all user
  - requires  ```'read:reservations-details'``` permission
 ```
{
    "reservation_detail": [
        {
            "account": "Najla@gmail.com",
            "appointmentـTime": "Mon, 02 Aug 2021 00:28:42 GMT",
            "guest": "Najla",
            "id": 1,
            "table_id": 1
        },
        {
            "account": "Guest@gmail.com",
            "appointmentـTime": "Mon, 02 Aug 2021 00:28:42 GMT",
            "guest": "Guest 1",
            "id": 2,
            "table_id": 2
        },
        {
            "account": "Sara@gmail.com",
            "appointmentـTime": "Tue, 03 Aug 2021 00:28:42 GMT",
            "guest": "Sara",
            "id": 3,
            "table_id": 3
        }
    ],
    "success": true,
    "total_reservations": 4
}
 ```

### [Menu manger] Endpoints
#### POST /menu/add
- General:
  - add a dish to the menu by providing the dish name, category, description, and price.
  - requires  ```'post:dish'``` permission
 ```
{
    "message": "The dish was added successfully",
    "success": true
}
 ```

#### PATCH /menu/<int:dish_id>/edit
- General:
  - Modify dish by passing the dish id in the url parameters.
  - requires  ```'edit:dish'``` permission
 ```
{
    "message": "The dish has been updated successfully",
    "success": true
}
 ```

#### DELETE /menu/<int:dish_id>/delete
- General:
  - delete dish by passing the dish id in the url parameters.
  - requires  ```'delete:dish'``` permission
 ```
{
              'message':"The dish was deleted successfully" ,
              'success': True     
}
 ```


