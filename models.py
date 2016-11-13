from google.appengine.ext import ndb
import uuid

class Item(ndb.Model):

    id=ndb.StringProperty()
    models=ndb.StringProperty(repeated=True)
    item=ndb.StringProperty()

    def __init__(self,*args,**kwargs):
        super(Item, self).__init__(*args, **kwargs)
        if kwargs.has_key('id'): self.id=kwargs['id']
        if kwargs.has_key('item'): self.item=kwargs['item']

    def addModel(self,model):
        self.models.append(model)

class Contact(ndb.Model):

    #Stores comment along with name and email for reply purposes
    #Currently stored contacts can only be deleted through admin server
    name=ndb.StringProperty()
    email=ndb.StringProperty()
    comments=ndb.TextProperty()

    def __init__(self,*args,**kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        if kwargs.has_key('name'): self.id=kwargs['name']
        if kwargs.has_key('email'): self.item=kwargs['email']
        if kwargs.has_key('comments'): self.item = kwargs['comments']

class Category:
    #id=""
    name=""

    def __init__(self,name,lft=None,rgt=None):
        #self.id=uuid.uuid1()
        self.name=name

class Problem:
    problem=""
    solution=""
    def __init__(self,problem,solution):
        self.problem=problem
        self.solution=solution

class Node:
    payload=""
    id=""
    lft=None
    rgt=None
    root=""

    def __init__(self,payload,lft=None,rgt=None):
        self.id=uuid.uuid1()
        self.payload=payload
        self.lft=lft
        self.rgt=rgt

    # def addNodes(self,newCat):

    def addSibling(self,sibNode,newNode):
        if sibNode.rgt==None: sibNode.rgt=newNode
        else: self.addSibling(sibNode.rgt,newNode)

    def addChild(self,child):
        if self.lft==None: self.lft=child;
        else: self.addSibling(self.lft,child)

    def addSubNode(self,payload):
        retNode=Node(payload,None,None)
        self.addChild(retNode)
        return retNode

    def nodeType(self):
        if isinstance(self.payload, Category): return "Category"
        else: return "Problem"

    def returnRootChildren(self):
        myKids=[]
        myNode=self.lft;
        while myNode!=None:
            myKids.append(myNode)
            myNode=myNode.rgt
        return myKids

    # def addProblem(self,name):
    #    retProb=Problem(name,self.rgt,self.rgt+1)

class User(ndb.Model):

    def __init__(self,id,nickname,email):
        self.id=id
        self.nickname=nickname
        self.email=email

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def is_authenticated(self):
        return True

# simple binary tree
# in this implementation, a node is inserted between an existing node and the root

class BinaryTree(ndb.Model):

    def __init__(self,rootid):
      self.left = None
      self.right = None
      self.rootid = rootid

    def getLeftChild(self):
        return self.left
    def setLeftChild(self,value):
        self.left = value
    def getRightChild(self):
        return self.right
    def setRightChild(self,value):
        self.right = value
    def setNodeValue(self,value):
        self.rootid = value
    def getNodeValue(self):
        return self.rootid

    def insertRight(self,newNode):
        if self.right == None:
            self.right = BinaryTree(newNode)
        else:
            tree = BinaryTree(newNode)
            tree.right = self.right
            self.right = tree

    def insertLeft(self,newNode):
        if self.left == None:
            self.left = BinaryTree(newNode)
        else:
            tree = BinaryTree(newNode)
            tree.left = self.left
            self.left = tree

    def printTree(self,tree):
        if tree != None:
            tree.printTree(tree.getLeftChild())
            print(tree.getNodeValue())
            tree.printTree(tree.getRightChild())
