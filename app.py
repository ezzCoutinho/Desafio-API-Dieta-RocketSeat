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
  id = data.get("id")
  name = data.get("name")
  description = data.get("description")
  date = data.get("date")
  is_not_diet = data.get("is_not_diet")
  if name and description:
    diet = Diets(id=id, name=name, description=description, date=date, is_not_diet=is_not_diet)
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

if __name__ == "__main__":
  app.run(debug=True)