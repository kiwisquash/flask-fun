from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, SubmitField


# forms
class NameForm(FlaskForm):
    name = StringField("What is your name?")
    cool = SelectField("What cool thing you want?", choices=[("switch", "Console"), ("pizza", "Food")])
    submit = SubmitField("Submit!")


class TempForm1(FlaskForm):
    celcius = FloatField("What is the temperature? (C)")
    submit = SubmitField("Submit!")


class TempForm2(FlaskForm):
    bad = FloatField("What is the temperature? (F)")
    submit = SubmitField("Submit!")
