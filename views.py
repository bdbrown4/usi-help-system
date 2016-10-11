from main import app
from flask import render_template,flash,redirect,url_for
from models import Item
from forms import ItemForm
import uuid

@app.route('/',methods=['GET','POST'])
def index():
    form=ItemForm()
    itemsOfInterest = Item.query()
    if len(itemsOfInterest.fetch(None))==0:
        mower=Item(id=str(uuid.uuid1()), item='Lawn Mowers')
        eater=Item(id=str(uuid.uuid1()),item='Weed Eaters')
        mower.addModel('Honda')
        mower.addModel('Black & Decker')
        eater.addModel('Torro')
        eater.addModel('Echo')
        print mower.item
        print eater.item
        mower.put()
        eater.put()
        itemsOfInterest = Item.query()
    print "The query length is "+str(len(itemsOfInterest.fetch(None)))
    if form.validate_on_submit():
        newItem = Item(id=str(uuid.uuid1()),item=form.item.data)
        print("myUUID is "+newItem.id)
        newItem.put()
        flash('New item added!')
        return redirect(url_for('index'))
    return render_template('index.html',
                           title='USI Help System',
                           itemsOfInterest=itemsOfInterest,
                           form=form
                           )
