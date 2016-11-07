from main import app
from flask import render_template,flash,redirect,url_for,request
from models import Item, BinaryTree
from forms import ItemForm, DelForm, EditForm
from google.appengine.ext import ndb
import uuid


@app.route('/',methods=['GET','POST'])
def index():
    addForm=ItemForm()
    delForm = DelForm()
    editForm = EditForm()
    itemsOfInterest = Item.query()
    #makes database if it doesn't exist...
    if len(itemsOfInterest.fetch(None))==0:
        mower=Item(id=str(uuid.uuid1()), item='Lawn Mower')
        eater=Item(id=str(uuid.uuid1()),item='Weed Eater')
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
    if request.form.has_key("edit") and editForm.validate_on_submit():  # If edit button press & something in edit box then...
        myItems = Item.query()  # get item list
        for item in myItems:  # find correct item
            print item
            print item.id
            if str(item.id) == str(editForm.id.data):
                # Get item
                item = item.key.get()
                # Change item to edit box data
                item.item = editForm.editItem.data
                # Save item
                item.put()
        flash('Item Edited!')
        return redirect(url_for('index'))
    elif request.form.has_key("delete") and delForm.validate_on_submit():
        myItems = Item.query()
        for item in myItems:
            print item
            print item.id
            if str(item.id) == str(delForm.id.data):
                ndb.delete_multi([item.key])
        flash('Item deleted!')
        return redirect(url_for('index'))
    elif request.form.has_key("add") and addForm.validate_on_submit():
        newItem = Item(id=str(uuid.uuid1()),item=addForm.item.data)
        print("myUUID is "+newItem.id)
        newItem.put()
        flash('New item added!')
        return redirect(url_for('index'))
    return render_template('index.html',
                           title='USI Help System',
                           itemsOfInterest=itemsOfInterest,
                           addForm=addForm,
                           delForm=delForm,
                           editForm=editForm
                           )
@app.route('/question',methods=['GET','POST'])
def testTree():
    myTree = BinaryTree("Maud")
    myTree.insertLeft("Bob")
    myTree.insertRight("Steven")
    myTree.insertLeft("Tom")
    myTree.insertRight("Jerry")
    myTree.printTree(myTree)
    return render_template('questiontree.html',
                           myTree = myTree.getNodeValue(),
                           myTreeLeft = myTree.getLeftChild(),
                           myTreeRight = myTree.getRightChild()
                           )

