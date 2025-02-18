from database import db
from sqlalchemy import func

class Diets(db.Model):
  # name (text), description (text), date(DateTime), is not diet(boolean)
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  description = db.Column(db.String(240), nullable=False)
  date = db.Column(db.DateTime, default=func.now())
  is_not_diet = db.Column(db.Boolean, default=False)

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "date": self.date.isoformat(),  # Certifica-se de que a data seja serializável
      "is_not_diet": self.is_not_diet
    }