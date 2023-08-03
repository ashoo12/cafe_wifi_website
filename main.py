from flask import Flask, jsonify, render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField
from wtforms.validators import DataRequired,URL

app=Flask(__name__)
app.app_context().push()
Bootstrap(app)
app.secret_key="aishadarvesh"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Cafe(db.Model):
      id=db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(250), unique=True, nullable=False)
      map_url = db.Column(db.String(500), nullable=False)
      img_url = db.Column(db.String(500), nullable=False)
      location = db.Column(db.String(250), nullable=False)
      seats = db.Column(db.String(250), nullable=False)
      has_toilet = db.Column(db.Boolean, nullable=False)
      has_wifi = db.Column(db.Boolean, nullable=False)
      has_sockets = db.Column(db.Boolean, nullable=False)
      can_take_calls = db.Column(db.Boolean, nullable=False)
      coffee_price = db.Column(db.String(250), nullable=True)

db.create_all()
all_cafes=db.session.query(Cafe).all()

class CafeForm(FlaskForm):
      name = StringField('Cafe name', validators=[DataRequired()])
      map_url =StringField('Cafe Location on google map', validators=[DataRequired(),URL()])
      img_url =StringField('Cafe Image', validators=[DataRequired(),URL()])
      location =StringField('Location',validators=[DataRequired()])
      seats =StringField('Seats', validators=[DataRequired()])
      has_toilet =BooleanField('Has toilet', validators=[DataRequired()])
      has_wifi =BooleanField('Has wifi', validators=[DataRequired()])
      has_sockets =BooleanField('Has sockets', validators=[DataRequired()])
      can_take_calls =BooleanField('Can take calls', validators=[DataRequired()])
      coffee_price=StringField('Coffee price', validators=[DataRequired()])
      submit = SubmitField('Submit')



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/explore")
def explore():
      return render_template("explore.html")

@app.route("/cafes")
def cafes():
      return render_template("location.html",all_cafes=all_cafes)

@app.route("/cafe_amenities/<int:id>",methods=["GET","POST"])
def cafe_amenities(id):
      clicked_cafe=Cafe.query.get(id)
      return render_template("cafe_amenity.html", all_cafes=all_cafes,clicked_cafe=clicked_cafe)

@app.route("/add",methods=["GET","POST"])
def add_cafes():
      form=CafeForm()
      if form.validate_on_submit():
            new_cafe = Cafe(name=form.name.data,map_url=form.map_url.data,img_url=form.img_url.data,location=form.location.data,seats=form.seats.data,has_toilet=form.has_toilet.data,has_wifi=form.has_wifi.data,has_sockets=form.has_sockets.data,can_take_calls=form.can_take_calls.data,coffee_price=form.coffee_price.data)
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for('home'))
      return render_template("add.html",form=form)

@app.route('/delete/<int:id>',methods=["GET","POST"])
def delete(id):
      cafe_to_delete=Cafe.query.get(id)
      db.session.delete(cafe_to_delete)
      db.session.commit()
      return redirect(url_for('home'))   



if __name__ == '__main__':
    app.run(debug=True)