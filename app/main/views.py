from datetime import datetime

from flask import current_app, flash, redirect, render_template, request, session, url_for

from .. import db
from ..email import send_email
from ..models import User
from . import main
from .forms import NameForm, TempForm1, TempForm2


# view functions
@main.route("/")
def index():
    return render_template("index.html", current_time=datetime.utcnow())


@main.route("/name", methods=["GET", "POST"])
def name():
    print(session)

    name_form = NameForm()

    if name_form.validate_on_submit():
        old_name = session.get("name", "")
        new_name = name_form.name.data or ""
        print(old_name)
        print(new_name)
        if old_name != "" and new_name != "" and old_name != new_name:
            flash("You changed your name you sob!")
        session["name"] = new_name
        name_form.name.data = ""
        do_something_cool(name_form.cool.data)
        return redirect(url_for(".name"))

    return render_template("name.html", name=session.get("name", ""), len=len, form=name_form)


@main.route("/greetings", methods=["GET", "POST"])
def greetings():
    name_form = NameForm()
    if name_form.validate_on_submit():
        name = name_form.name.data
        user = User.query.filter(User.name == name).first()
        if user is None:
            db.session.add(User(name=name))
            db.session.commit()
            session["new_user"] = True

        else:
            session["new_user"] = False
        session["name"] = name
        return redirect(url_for(".greetings"))

    return render_template(
        "greetings.html", name=session.get("name"), form=name_form, new_user=session.get("new_user", False)
    )


@main.route("/something/<cool>")
def do_something_cool(cool):
    print(cool)
    return redirect(url_for(".index"))


@main.route("/agent")
def agent():
    res = request.headers.get("User-Agent")
    return render_template("agent.html", res=res)


@main.route("/convert", methods=["GET", "POST"])
def convert_temp():

    temp_form1 = TempForm1()
    temp_form2 = TempForm2()

    if temp_form1.celcius.data and temp_form1.validate_on_submit():
        print("Greetings")
        celcius = session["celcius"] = temp_form1.celcius.data
        if celcius is not None:
            session["bad"] = 1.8 * celcius + 32
        else:
            if "bad" in session:
                session.pop("bad")
        return redirect(url_for(".convert_temp"))

    elif temp_form2.bad.data and temp_form2.validate_on_submit():
        print("Vad")
        bad = session["bad"] = temp_form2.bad.data
        if bad is not None:
            session["celcius"] = (bad - 32) / 1.8
        else:
            if "celcius" in session:
                session.pop("celcius")
        return redirect(url_for(".convert_temp"))

    elif temp_form1.validate_on_submit() or temp_form2.validate_on_submit():
        if "bad" in session:
            session.pop("bad")
        if "celcius" in session:
            session.pop("celcius")

    return render_template(
        "temp.html", celcius=session.get("celcius"), bad=session.get("bad"), form1=temp_form1, form2=temp_form2
    )


@main.route("/email", methods=["GET", "POST"])
def email():
    form = NameForm()
    if form.validate_on_submit():
        username = form.name.data
        user = User.query.filter_by(name=username).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
            app = current_app
            flasky_admin = app.config["FLASKY_ADMIN"]
            if flasky_admin:
                send_email(flasky_admin, "New User", "mail/new_user", user=user)
        else:
            session["known"] = True
        session["name"] = username
        form.name.data = ""
        return redirect(url_for(".email"))
    return render_template(
        "email.html", len=len, form=form, username=session.get("name"), known=session.get("known", False)
    )
