from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.sql import func

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def random():
    random_cafe = db.session.execute(db.select(Cafe).order_by(func.random()).limit(1)).scalar_one()
    return jsonify(cafe=random_cafe.as_dict())
    # return f"<h1>{random_cafe.name}</h1>" \
    #        f"<p>{random_cafe.location}</p>" \
    #        f"<img src={random_cafe.img_url}>" \
    #        f"<p>{random_cafe.map_url}</p>" \
    #        f"<p>Seats: {random_cafe.seats}</p>" \
    #        f"<p>Has Toilet: {random_cafe.has_toilet}</p>" \
    #        f"<p>Has Wifi: {random_cafe.has_wifi}</p>" \
    #        f"<p>Has Sockets: {random_cafe.has_sockets}</p>" \
    #        f"<p>Can Take Calls: {random_cafe.can_take_calls}</p>" \
    #        f"<p>Coffee Price: {random_cafe.coffee_price}</p>"   

@app.route("/all")
def all_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars()
    cafes_list = [cafe.as_dict() for cafe in cafes]
    return jsonify(cafes=cafes_list)

@app.route("/search")
def search():
    cafe_loc = request.args.get("loc")
    cafes = db.session.execute(db.select(Cafe).where(Cafe.location == cafe_loc)).scalars()
    cafes_list = [cafe.as_dict() for cafe in cafes]
    if len(cafes_list) > 0:
        return jsonify(cafes=cafes_list)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe in that location"}), 404

# HTTP POST - Create Record
@app.route("/add", methods=["POST"]) 
def add():
    name = request.form.get("name")
    if len(name) > 0:
        new_cafe = Cafe(
            name=name,
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            seats=request.form.get("seats"),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            has_sockets=bool(request.form.get("has_sockets")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            coffee_price=request.form.get("coffee_price")
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe"}), 201
    else:
        return jsonify(error={"Bad Request": "Please provide a name and map_url"}), 400
    

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar_one_or_none()
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price"}), 200
    else:
        return jsonify(error={"Not Found": "Cafe not found"}), 404


# HTTP DELETE - Delete Record
@app.route("/report_closed/<cafe_id>", methods=["DELETE"])
def report_closed(cafe_id):
    api_key = request.args.get("api_key")
    if api_key != "TopSecretAPIKey":
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key"), 403
    
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar_one_or_none()
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe"}), 200
    else:
        return jsonify(error={"Not Found": "Cafe not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
