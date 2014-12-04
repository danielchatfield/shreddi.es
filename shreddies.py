from flask import Flask, request, render_template, session, abort
from flask_raven import raven_auth

from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages


app = Flask(__name__)
app.config['SECRET_KEY'] = "pleash dunt abuze me"


class Nosh(messages.Enum):
    SHREDDIES = 1
    MILK = 2


class Nom(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True, required=True)
    food = msgprop.EnumProperty(Nosh, required=True)
    amount = ndb.FloatProperty(required=True)


class Nommer(ndb.Model):
    pass


NOSH_MOO_UNIT = {
    Nosh.SHREDDIES: "grams",
    Nosh.MILK: "pints"
}


@app.route('/')
def home():
    eats = Nom.query().order(-Nom.date).fetch(1000)
    result = "<h1>mallinson's shreddies nommation ~#~#~</h1><br/><div id='nomTable'>"
    for eat in eats:
        result += "<div class='recordOfNom'>"
        result += "mallinson nommed {} {} of {} on {}</div><br/>".format(
            eat.amount, NOSH_MOO_UNIT[eat.food], eat.food.name, eat.date)
	result += "</div>"
    return result


@app.route('/yum', methods=['GET', 'POST'])
@raven_auth()
def yum():
    if '_raven' not in session:
        abort(401)

    crsid = session['_raven']
    user = ndb.Key(Nommer, crsid).get()
    if not user:
        abort(403)

    if request.method == 'POST':
        shreddies = None
        milk = None
        try:
            shreddies = int(request.form['shreddies'])
            milk = int(request.form['milk'])
        except ValueError:
            return render_template('yum.html')
        s = Nom()
        s.food = Nosh.SHREDDIES
        s.amount = shreddies
        s.put()
        m = Nom()
        m.food = Nosh.MILK
        m.amount = milk
        m.put()
    return render_template('yum.html')
