from flask import Flask, request, jsonify
from models.diets import Diets # Temos que trazer a modelagem dos dados, para o app
from database import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-diet"

db.init_app(app)

@app.route("/meals", methods = ["POST"])
def create_meals():
  data = request.json
  name = data.get("name")
  description = data.get("description")
  date = data.get("date")
  is_not_diet = data.get("is_not_diet")
  if name and description:
    diet = Diets(name=name, description=description, date=date, is_not_diet=is_not_diet)
    db.session.add(diet)
    db.session.commit()
    return jsonify({"message": "Ok! dieta registrada com sucesso..."})
  
  return jsonify({"message": "Falha! em registrar a dieta."}), 404

@app.route("/meals/<int:id_meals>", methods = ["PUT"])
def update_meals(id_meals):
  data = request.json
  meal = Diets.query.get(id_meals)

  if meal:
    meal.name = data.get("name")
    meal.description = data.get("description")
    meal.date = data.get("date")
    meal.is_not_diet = data.get("is_not_diet")
    db.session.commit()

    return jsonify({"message": "Ok! dieta foi atualizada com sucesso!"})
  
  return jsonify({"message": "Dieta não foi atualizada!"}), 404

@app.route("/meals/<int:id_meals>", methods = ["DELETE"])
def delete_meals(id_meals):
  meal = Diets.query.get(id_meals)

  if meal:
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": f"Ok! a dieta {id_meals}, foi apagada!"})
  
  return jsonify({"message": "Não foi possível apagar a dieta!"}), 404

@app.route("/meals", methods = ["GET"])
def read_meals():
  meals = Diets.query.all()
  meal_list = [meal.to_dict() for meal in meals]
    
  output = {

    "diet": meal_list,
    "total_diets": len(meal_list)
  }

  return jsonify(output)

@app.route("/meals/<int:id_meals>", methods = ["GET"])
def read_meal(id_meals):
  meal = Diets.query.get(id_meals)

  if meal:
    return jsonify({"name": meal.name, "description": meal.description, "date": meal.date, "is not diet": meal.is_not_diet})

  return jsonify({"message": "Não foi possível achar a dieta!"}), 404 


if __name__ == "__main__":
  app.run(debug=True)