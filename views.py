from main import app
from flask import render_template,flash,redirect,url_for,request,session
from models import Item, UserClass, Contact, Category, Problem, Node, Tree
from forms import ItemForm, DelForm, EditForm
from google.appengine.ext import ndb
import uuid
import hashlib
import config
import ast


@app.route('/testTree',methods=['GET','POST'])
def test():
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

@app.route('/logout')
def logout():
    #Clear session data to log out
    session.clear()
    return render_template('logout.html')

#User inputs username/password
@app.route('/login')
def login():
    return render_template('login.html')

#app takes username/password and authenticates user
@app.route('/authenticate', methods=['POST'])
def authenticate():
    userexists=False
    #Get username and password from login form
    username=request.form['username']
    password=request.form['password']
    #Hash password for comparison with hash entry in database
    h = hashlib.md5()
    h.update(password)
    hashpassword = h.hexdigest()
    #Print to console for troubleshooting
    #print(username)
    #print(hashpassword)
    #Get list of usuers
    users=UserClass.query()
    #Compare username from form with every username in database
    for user in users:
        #print(user.username)
        #If username found, set userexists true
        if user.username==username:
            userexists=True
            #print(hashpassword)
            # If username found, check password from form with password in databse for that username
            if user.password==hashpassword:
                #Set session data with username
                session['username'] = username
                #Set user rights
                session['rights'] = user.rights
                flash('Logged in successfully.')
                return render_template('authenticated.html')
    #If login failed, tell user either username or password was bad, return to login form
    flash('Login failed');
    if userexists==False: flash('Username does not exist')
    else: flash('Incorrect password')
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/noAnswer')
def noAnswer():
    del roots[:]
    del items[:]
    return render_template('noAnswer.html')

@app.route('/registersubmitted', methods=['POST']) #https://docs.python.org/2/library/hashlib.html
def registersub():
    #get info from fields
    username = request.form['username']
    email = request.form['email']
    #get password from field, create md5 hash for more secure storage
    password = request.form['password']
    h = hashlib.md5()
    h.update(password)
    passwordhash=h.hexdigest()
    print("got info")
    #Check each username in database for copies (two users with same username is problem for login)
    users=UserClass.query()
    for user in users:
        if user.username==username: flash('Username already in use'); return render_template('register.html')
        if user.email==email: flash('Email already in use'); return render_template('register.html')
    #build user object
    userObj = UserClass(username = request.form['username'],
                        email = request.form['email'],
                        password = passwordhash,
                        rights='2')
    print("built obj")
    #Store user in db
    userObj.put()
    print("stored obj")
    return render_template('registersubmitted.html',
                            username=username)

def storeCat(myCat):
    myCat2=Category(myCat)
    myCat2.put()
    return myCat2

def storeProb(myProb, myAns):
    myProb2=Problem(myProb,myAns)
    myProb2.put()
    return myProb2

roots = []
items = []
models = []
parts=[]
problems=[]

@app.route("/submittedNameAddress", methods=['POST'])
def submissionOfPart():
    name = request.form['name']
    address = request.form['address']
    return render_template("submittedNameAddress.html",
                           name=name,
                           address=address)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.form.has_key("changeCat") or request.form.has_key("changeProb"):
        myObj = None
        for node in roots:
            if (node.nodeType() == "Category" and node.payload.name == request.form['selectedCat']) or node.nodeType() == "Problem":
                myObj = node
                break
        if myObj!=None:
            del roots[:]
            del problems[:]
            del models[:]
            roots.append(myObj)
            for thing in myObj.returnRootChildren():
                items.append(thing)
    elif request.form.has_key("changeItem"):
        myObj = None
        for node in items:
            if (node.nodeType() == "Category" and node.payload.name == request.form['selectedItem']):
                myObj = node
                break
        if myObj != None:
            del items[:]
            items.append(myObj)
            for thing in myObj.returnRootChildren():
                models.append(thing)
    elif request.form.has_key("changeModelParts"):
        myObj = None
        for node in models:
            if (node.nodeType() == "Category" and node.payload.name == request.form['selectedModel']):
                myObj = node
                break
        if myObj != None:
            del models[:]
            models.append(myObj)
            for thing in myObj.returnRootChildren():
                if thing.nodeType() == "Category":
                    parts.append(thing)
            return render_template("parts.html",
                                   models=models,
                                   parts=parts)
    elif request.form.has_key("Parts"):
        return render_template("parts.html",
                                   models=models,
                                   parts=parts)
    elif request.form.has_key("Part"):
        myObj = None
        for node in parts:
            if node.nodeType() == "Category" and node.payload.name == request.form['selectedPart']:
                myObj=node
                break
        if myObj !=None:
            del roots[:]
            del items[:]
            del models[:]
            del parts[:]
            part=myObj
        return render_template("partSelectedDiv.html",
                               part=part)
    elif request.form.has_key("changeModelProblems"):
        myObj = None
        for node in models:
            if (node.nodeType() == "Category" and node.payload.name == request.form['selectedModel']):
                myObj = node
                break
        if myObj != None:
            del models[:]
            models.append(myObj)
            for thing in myObj.returnRootChildren():
                if thing.nodeType() == "Problem":
                    problems.append(thing)
            return render_template("problems.html",
                                   models=models,
                                   problems=problems)
    elif request.form.has_key("Problems"):
        return render_template("problems.html",
                                   models=models,
                                   problems=problems)
    elif request.form.has_key("Problem") and request.form['yesProbs']:
        myObj = None
        for node in problems:
            if (node.nodeType() == "Problem" and (node.payload.problem == request.form['selectedThing'] or node.payload.solution == request.form['selectedThing'])):
                myObj = node
                break
        if myObj != None:
            del roots[:]
            del items[:]
            del parts[:]
            del problems[:]
            problems.append(myObj)
            for thing in myObj.returnRootChildren():
                if thing.payload.problem:
                    problems.append(thing)
                else:
                    answer = thing.payload.solution
            return render_template("problems.html",
                                   models=models,
                                   problems=problems,
                                   answer=answer)
    #Needs to be pushed to github
    #else
    elif len(roots) == 0:
        metaData=Tree.query()
        if len(metaData.fetch(None))==0:
            r1 = Node(storeCat("Lawn Equipment"))
            roots.append(r1)
            lm = r1.addSubNode(storeCat("Lawn Mower"))
            we = r1.addSubNode(storeCat("Weed Eater"))
            ed = r1.addSubNode(storeCat("Edger"))

            r2 = Node(storeCat("Mobile Phone"))
            att=r2.addSubNode(storeCat("AT&T"))
            verizon=r2.addSubNode(storeCat("Verizon"))
            sprint=r2.addSubNode(storeCat("Sprint"))
            nexs=sprint.addSubNode(storeCat("Nexus"))
            iphones=sprint.addSubNode(storeCat("iPhone 7"))
            galaxys=sprint.addSubNode(storeCat("Galaxy 7S"))
            nexa=att.addSubNode(storeCat("Nexus"))
            iphonea=att.addSubNode(storeCat("iPhone 7"))
            galaxya=att.addSubNode(storeCat("Galaxy 7S"))
            nexv=verizon.addSubNode(storeCat("Nexus"))
            iphonev=verizon.addSubNode(storeCat("iPhone 7"))
            galaxyv=verizon.addSubNode(storeCat("Galaxy 7S"))

            nexsprobone = nexs.addSubNode(storeProb("Broken Screen?", None))
            nexsprobtwo = nexs.addSubNode(storeProb("Broken home button?",None))
            nexsprobthree = nexs.addSubNode(storeProb("Phone doesn't turn on?", None))
            nexsprobone.addSubNode(storeProb(None, "You need a new screen!"))
            nexsprobtwo.addSubNode(storeProb(None, "You need a new home button!"))
            nexsprobthree.addSubNode(storeProb(None, "You need a new battery!"))
            nexaprobone= nexa.addSubNode(storeProb("Broken Screen?", None))
            nexaprobtwo = nexa.addSubNode(storeProb("Broken home button?",None))
            nexaprobthree = nexa.addSubNode(storeProb("Phone doesn't turn on?", None))
            nexaprobone.addSubNode(storeProb(None, "You need a new screen!"))
            nexaprobtwo.addSubNode(storeProb(None, "You need a new home button!"))
            nexaprobthree.addSubNode(storeProb(None, "You need a new battery!"))
            nexvprobone = nexv.addSubNode(storeProb("Broken Screen?", None))
            nexvprobtwo = nexv.addSubNode(storeProb("Broken home button?",None))
            nexvprobthree = nexv.addSubNode(storeProb("Phone doesn't turn on?", None))
            nexvprobone.addSubNode(storeProb(None, "You need a new screen!"))
            nexvprobtwo.addSubNode(storeProb(None, "You need a new home button!"))
            nexvprobthree.addSubNode(storeProb(None, "You need a new battery!"))

            iphonesprobone = iphones.addSubNode(storeProb("Broken Screen?", None))
            iphonesprobtwo = iphones.addSubNode(storeProb("Broken home button?", None))
            iphonesprobthree = iphones.addSubNode(storeProb("Phone doesn't turn on?", None))
            iphonesprobone.addSubNode(storeProb(None, "You need a new screen!"))
            iphonesprobtwo.addSubNode(storeProb(None, "You need a new home button!"))
            iphonesprobthree.addSubNode(storeProb(None, "You need a new battery!"))
            iphoneaprobone = iphonea.addSubNode(storeProb("Broken Screen?", None))
            iphoneaprobtwo = iphonea.addSubNode(storeProb("Broken home button?", None))
            iphoneaprobthree = iphonea.addSubNode(storeProb("Phone doesn't turn on?", None))
            iphoneaprobone.addSubNode(storeProb(None, "You need a new screen!"))
            iphoneaprobtwo.addSubNode(storeProb(None, "You need a new home button!"))
            iphoneaprobthree.addSubNode(storeProb(None, "You need a new battery!"))
            iphonevprobone = iphonev.addSubNode(storeProb("Broken Screen?", None))
            iphonevprobtwo = iphonev.addSubNode(storeProb("Broken home button?", None))
            iphonevprobthree = iphonev.addSubNode(storeProb("Phone doesn't turn on?", None))
            iphonevprobone.addSubNode(storeProb(None, "You need a new screen!"))
            iphonevprobtwo.addSubNode(storeProb(None, "You need a new home button!"))
            iphonevprobthree.addSubNode(storeProb(None, "You need a new battery!"))

            galaxysprobone = galaxys.addSubNode(storeProb("Broken Screen?", None))
            galaxysprobtwo = galaxys.addSubNode(storeProb("Broken home button?", None))
            galaxysprobthree = galaxys.addSubNode(storeProb("Phone doesn't turn on?", None))
            galaxysprobone.addSubNode(storeProb(None, "You need a new screen!"))
            galaxysprobtwo.addSubNode(storeProb(None, "You need a new home button!"))
            galaxysprobthree.addSubNode(storeProb(None, "You need a new battery!"))
            galaxyaprobone = galaxya.addSubNode(storeProb("Broken Screen?", None))
            galaxyaprobtwo = galaxya.addSubNode(storeProb("Broken home button?", None))
            galaxyaprobthree = galaxya.addSubNode(storeProb("Phone doesn't turn on?", None))
            galaxyaprobone.addSubNode(storeProb(None, "You need a new screen!"))
            galaxyaprobtwo.addSubNode(storeProb(None, "You need a new home button!"))
            galaxyaprobthree.addSubNode(storeProb(None, "You need a new battery!"))
            galaxyvprobone = galaxyv.addSubNode(storeProb("Broken Screen?", None))
            galaxyvprobtwo = galaxyv.addSubNode(storeProb("Broken home button?", None))
            galaxyvprobthree = galaxyv.addSubNode(storeProb("Phone doesn't turn on?", None))
            galaxyvprobone.addSubNode(storeProb(None, "You need a new screen!"))
            galaxyvprobtwo.addSubNode(storeProb(None, "You need a new home button!"))
            galaxyvprobthree.addSubNode(storeProb(None, "You need a new battery!"))

            nexs.addSubNode(storeCat("Screen"))
            nexs.addSubNode(storeCat("Home Button"))
            nexs.addSubNode(storeCat("Battery"))
            nexa.addSubNode(storeCat("Screen"))
            nexa.addSubNode(storeCat("Home Button"))
            nexa.addSubNode(storeCat("Battery"))
            nexv.addSubNode(storeCat("Screen"))
            nexv.addSubNode(storeCat("Home Button"))
            nexv.addSubNode(storeCat("Battery"))

            iphones.addSubNode(storeCat("Screen"))
            iphones.addSubNode(storeCat("Home Button"))
            iphones.addSubNode(storeCat("Battery"))
            iphonea.addSubNode(storeCat("Screen"))
            iphonea.addSubNode(storeCat("Home Button"))
            iphonea.addSubNode(storeCat("Battery"))
            iphonev.addSubNode(storeCat("Screen"))
            iphonev.addSubNode(storeCat("Home Button"))
            iphonev.addSubNode(storeCat("Battery"))

            galaxys.addSubNode(storeCat("Screen"))
            galaxys.addSubNode(storeCat("Home Button"))
            galaxys.addSubNode(storeCat("Battery"))
            galaxya.addSubNode(storeCat("Screen"))
            galaxya.addSubNode(storeCat("Home Button"))
            galaxya.addSubNode(storeCat("Battery"))
            galaxyv.addSubNode(storeCat("Screen"))
            galaxyv.addSubNode(storeCat("Home Button"))
            galaxyv.addSubNode(storeCat("Battery"))

            roots.append(r2);

            torro = we.addSubNode(storeCat("Torro"))
            torro.addSubNode(storeCat("Gas Tank"))
            torro.addSubNode(storeCat("Pull String"))
            torro.addSubNode(storeCat("Spark Plugs"))
            craftsmen = we.addSubNode(storeCat("Craftsmen"))
            craftsmen.addSubNode(storeCat("Gas Tank"))
            craftsmen.addSubNode(storeCat("Nylon String"))
            honda = lm.addSubNode(storeCat("Honda"))
            honda.addSubNode(storeCat("Gas Tank"))
            honda.addSubNode(storeCat("Blades"))
            honda.addSubNode(storeCat("Spark Plugs"))
            bd = lm.addSubNode(storeCat("B&D"))
            bd.addSubNode(storeCat("Wheels"))
            bd.addSubNode(storeCat("Bearings"))
            torro2 = ed.addSubNode(storeCat("Torro"))
            torro2.addSubNode(storeCat("Handles"))
            torro2.addSubNode(storeCat("Screws"))

            torroprobone= torro.addSubNode(storeProb("Do you have gas?", None))
            torroprobtwo= torro.addSubNode(storeProb("Is your pull string tangled?", None))
            torroprobone.addSubNode(storeProb(None,"You have no gas!"))
            torroprobtwo.addSubNode(storeProb(None, "You need to untangle your pull string!"))
            craftsmenprobone = craftsmen.addSubNode(storeProb("Do you have gas?", None))
            craftsmenprobtwo = craftsmen.addSubNode(storeProb("Is your pull string tangled?", None))
            craftsmenprobone.addSubNode(storeProb(None, "You have no gas!"))
            craftsmenprobtwo.addSubNode(storeProb(None, "You need to untangle your pull string!"))
            hondaprobone = honda.addSubNode(storeProb("Do you have gas?", None))
            hondaprobtwo = honda.addSubNode(storeProb("Are the blades dull?", None))
            hondaprobone.addSubNode(storeProb(None, "You have no gas!"))
            hondaprobtwo.addSubNode(storeProb(None, "Your blades are dull!"))
            bdprobone = bd.addSubNode(storeProb("Are your wheels wobbling?", None))
            bdprobtwo = bd.addSubNode(storeProb("Are you hearing a squeaking noise as you mow?", None))
            bdprobone.addSubNode(storeProb(None,"You need to tighten the wheels!"))
            bdprobtwo.addSubNode(storeProb(None,"You need to put some damn WD-40 on those bearings!!!"))
            torro2probone = torro2.addSubNode(storeProb("Are you handles wobbling off as you cut?", None))
            torro2probtwo = torro2.addSubNode(storeProb("Are your handles rusty?",None))
            torro2probone.addSubNode(storeProb(None,"You need to tighten the screws!"))
            torro2probtwo.addSubNode(storeProb(None,"You definitely need some new handles!"))

            r1.printTree()

            #treeDict = r1.convertTree()
            Tree(str(r1.convertTree())).put()
            Tree(str(r2.convertTree())).put()
            #r1Prime = Node(treeDict)
            #r1Prime.printTree()
        else:
            for probsol in Problem.query(): config.probList.append(probsol)
            for cat in Category.query(): config.catList.append(cat)
            trees = Tree.query()  # get item list
            for tree in trees:  # find correct item
                roots.append(Node(ast.literal_eval(tree.tree)))



    return render_template("testindex.html",
                           roots=roots,
                           items=items)
