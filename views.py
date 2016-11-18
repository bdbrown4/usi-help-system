from main import app
from flask import render_template,flash,redirect,url_for,request
from models import Item, BinaryTree, Contact, Category, Problem, Node
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

@app.route('/form')
def form():
    return render_template('form.html')

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


@app.route('/submittedContacts', methods=['POST'])
def submitted_form():
    #Get info from fields
    name = request.form['name']
    email = request.form['email']
    comments = request.form['comments']
    #use Contact constructor to make db item
    contactObj=Contact(name=request.form['name'],
                 email=request.form['email'],
                 comments=request.form['comments'])
    #Store obj in database
    contactObj.put()
    return render_template(
        'submittedContacts.html',
        name=name,
        email=email,
        comments=comments)


roots = []

@app.route('/testTree',methods=['GET','POST'])
def test():
    if request.form.has_key("changeForm"):
        print(request.form['selectedCat'])
        myObj = None
        for node in roots:
            if node.nodeType() == "Category" and node.payload.name == request.form['selectedCat']:
                myObj = node
                break
            elif node.nodeType() == "Problem" and node.payload.problem == request.form['selectedCat']:
                myObj = node
                break
        if myObj!=None:
            del roots[:]
            for thing in myObj.returnRootChildren():
                roots.append(thing)
    elif len(roots) == 0:
        r1 = Node(Category("Lawn Equipment"))
        roots.append(r1)
        lm = r1.addSubNode(Category("Lawn Mower"))
        we = r1.addSubNode(Category("Weed Eater"))
        r1.addSubNode(Category("Edger"))

        r2 = Node(Category("Mobile Phone"))
        rr2 = r2.addSubNode(Problem("Are you having a problem?", None))
        roots.append(r2);
        gp = rr2.addSubNode(Problem("Does the lawn mower have gas?", None))
        mnoises = rr2.addSubNode(Problem("Is the lawn mower making noises?", None))
        gp.addSubNode(Problem(None, "You don't have any gas!"))

        we.addSubNode(Category("Torro"))
        honda = lm.addSubNode(Category("Honda"))
        bd = lm.addSubNode(Category("B&D"))
        honda.addSubNode(Category("WOW"))
        bd.addSubNode(Category("itWORKS!"))
        r1.printTree()
        #r2.printTree()
        treeDict = r1.convertTree()
        #r2.convertTree()
        #treeDictPrint = Node(treeDict)
        #treeDictPrint.printTree()


    return render_template("testindex.html",
                           roots=roots
                           )
