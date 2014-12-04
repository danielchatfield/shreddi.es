from flask import Flask, request, render_template

from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages


app = Flask(__name__)


class Nosh(messages.Enum):
    SHREDDIES = 1
    MILK = 2


class Nom(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True, required=True)
    food = msgprop.EnumProperty(Nosh, required=True)
    amount = ndb.FloatProperty(required=True)


NOSH_MOO_UNIT = {
    Nosh.SHREDDIES: "grams",
    Nosh.MILK: "pints"
}


@app.route('/')
def home():
    eats = Nom.query().order(-Nom.date).fetch(1000)
    result = "<h1>mallinson's shreddies nommation ~#~#~</h1><br/>"
    for eat in eats:
        result += "mallinson nommed {} {} of {} on {}<br/>".format(
            eat.amount, NOSH_MOO_UNIT[eat.food], eat.food.name, eat.date)
    return result


@app.route('/yum', methods=['GET', 'POST'])
def yum():
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
