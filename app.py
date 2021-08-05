import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from auth  import *
from models import *

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  migrate = Migrate(app, db)
  setup_db(app , database_path)
  
  #db_drop_and_create_all()



  QUESTIONS_PER_PAGE = 3

  def paginate_questions(request, selection):
    '''function for paginating questions'''

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


  ############ PUBLIC USERS ###############
  @app.route('/' , methods=['GET'])
  def hello():
    return jsonify({
        'message': 'hello from restraunt API'
         }), 200


  @app.route('/menu' , methods=['GET'])
  def get_menu():
    try:
       menu = Menu.query.all()
       current_dishes =paginate_questions(request , menu)

       if not menu:
        return jsonify({
        'success': True,
        'dishes': 'NO DISHIES'
         }), 200

       dishes = []
       for dish in menu:
         dishes.append({
        "id": dish.id ,
        "dish_name": dish.dish_name,
        "category": dish.category,
        "description" : dish.description,
        "price": dish.price
        })

       return jsonify({
        'success': True,
        'dishes': current_dishes,
        'total_dishs': len(menu),
         }), 200
    except:
        abort(422)
        

  @app.route('/book' , methods=['POST'])
  def book():
    try:
      body = request.get_json();
      Account = body.get('account' , None);
      AppointmentـTime = body.get('appointmentـTime' , None);
      Guest = body.get('guest' , None);
      Chairs = body.get('chairs' , None);

      if((Account) and (AppointmentـTime ) and (Guest) and (Chairs)):
        chairs_num=int(Chairs)
        Tables= Table.query.filter( Table.chairs_num == chairs_num ).all()
        reservations = Reservation.query.filter(Reservation.appointmentـTime == AppointmentـTime)

        all_reservations =[]
        for r in reservations:
            all_reservations.append(r.table_id)

        Table_id = None
        for t in Tables:
            if t.id not in all_reservations:
                Table_id = t.id
                break

        if Table_id is None:
         return jsonify({
             'success': False,
              'message':"the table is not available for this date and time "
         }), 409 

        if((Account) and (AppointmentـTime ) and (Guest) and (Table_id)):
          book =  Reservation(guest=Guest , appointmentـTime= AppointmentـTime, table_id=Table_id , account=Account)
          book.insert()
          return jsonify({
             'success': True,
              'message':"The table was reserved successfully "
         }), 200 
      else:
         return jsonify({
             'success': False,
              'message':"please fill all the fields"
         }), 400
    except:
      abort(422) 

################## Reservation manger ################################

  @app.route('/<string:user>/reservation' , methods=['GET'])
  @requires_auth('read:reservation')
  def get_reservation(jwt , user):

      reservations = Reservation.query.filter(Reservation.account == user).all()
      
      guest_reservation = []
      for r in reservations:
        guest_reservation.append({
        'table_id': r.table_id,
        'appointmentـTime': r.appointmentـTime
        })
      return jsonify({
        'success': True,
        'reservation': guest_reservation
         }), 200

  

  @app.route('/reservation-detail' , methods=['GET'])
  @requires_auth('read:reservations-details')
  def get_reservation_detail(jwt):
    try:
      reservations = Reservation.query.all()
      current_reservations =paginate_questions(request , reservations)

      if not reservations :
        return jsonify({
             'success': True,
              'reservation_detail':'No reservations'
         }), 200

      all_reservation = []
      for r in reservations:
        all_reservation.append({
        'id':r.id,
        'guest':r.guest,
        'table_id': r.table_id,
        'appointmentـTime': r.appointmentـTime
        })
      return jsonify({
             'success': True,
              'reservation_detail': current_reservations,
              'total_reservations': len(reservations),
         }), 200
    except:
      abort(422)



#################### Menu manager ###############################

  
  @app.route('/menu/add', methods=['POST'])
  @requires_auth('post:dish')
  def post_new_dish(jwt):
    try:
      body = request.get_json();
      Dish_name= body.get('dish_name' , None);
      Category = body.get('category' , None);
      Description = body.get('description' , None);
      Price = body.get('price' , None);

      if((Dish_name) and (Category) and (Description) and (Price)): 

          new_dish =  Menu( dish_name= Dish_name , category=Category, description=Description ,  price = Price )
          new_dish.insert()
          return jsonify({
              'success': True,
              'message':'The dish was added successfully'
           }), 200
      else:
         return jsonify({
              'success': False,
              'message':"please fill all the fields" 
           }), 400
    except:
      abort(422)

  
  @app.route('/menu/<int:dish_id>/edit', methods=['PATCH'])
  @requires_auth('edit:dish')
  def edit_dish(jwt , dish_id):
    try:
      dish = Menu.query.get(dish_id); 
      if not dish :
        return jsonify({
              'success': False,
              'message':"invalid dish id" 
           }), 400
      body = request.get_json();
      Dish_name= body.get('dish_name' , None);
      Category = body.get('category' , None);
      Description = body.get('description' , None);
      Price = body.get('price' , None);

      if Dish_name :
       dish.dish_name = Dish_name
      if Category :
       dish.category = Category
      if Description :
       dish.description = Description
      if Price :
       dish.price = Price

      dish.update()
      return jsonify({
              'success': True,
              'message':"The dish has been updated successfully" 
           }), 200
    except:
      abort(422)
      



  @app.route('/menu/<int:dish_id>/delete', methods=['DELETE'])
  @requires_auth('delete:dish')
  def delete_dish(jwt , dish_id):
    try:
      Dish = Menu.query.get(dish_id)
      if not Dish :
        return jsonify({
              'success': False,
              'message':"invalid dish id" 
           }), 400
      Dish.delete()
      return jsonify({
              'success': True,
              'message':"The dish was deleted successfully" 
           }), 200
    except:
      abort(422)




  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422



  @app.errorhandler(AuthError)
  def process_AuthError(error):
    response = jsonify(error.error)
    response.status_code = error.status_code

    return response



  return app

app = create_app()

if __name__ == '__main__':
    app.run()
