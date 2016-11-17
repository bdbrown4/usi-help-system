from google.appengine.ext import ndb
import uuid
import ast

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

class Category(ndb.Model):
    #id=""
    name=ndb.StringProperty()
    id=ndb.StringProperty()

    def __init__(self,name,*args,**kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.id=str(uuid.uuid1())
        self.name=name

class Problem(ndb.Model):
    problem=ndb.StringProperty()
    solution=ndb.StringProperty()
    id=ndb.StringProperty()

    def __init__(self,problem,solution,*args,**kwargs):
        super(Problem, self).__init__(*args, **kwargs)
        self.id=str(uuid.uuid1())
        self.problem=problem
        self.solution=solution

class Node(ndb.Model):
    payload=ndb.PickleProperty()
    id=ndb.StringProperty()
    lft=ndb.PickleProperty()
    rgt=ndb.PickleProperty()

    def createTree(self,treeString):
        treeDict=ast.literal_eval(treeString)
        


    def __init__(self,payload,lft=None,rgt=None,*args,**kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.id=str(uuid.uuid1())
        self.payload=payload
        payload.put()
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

    def spaceMe(self,scount):
        spaceStr = ""
        while scount > 0:
            spaceStr += " ";
            scount -= 1
        return spaceStr

    def payloadVal(self,payload):
        if payload.problem != None:
            return payload.problem
        else:
            return payload.solution

    def printTree(self,myNode=None, scount=0):
        if myNode == None:
            myNode=self
        if isinstance(myNode.payload, Category):
            if myNode.rgt == None and myNode.lft == None:
                print self.spaceMe(scount) + myNode.payload.name
            else:
                if myNode.lft != None:
                    print self.spaceMe(scount) + myNode.payload.name
                    self.printTree(myNode.lft, scount + 4)
                if myNode.rgt != None:
                    if myNode.lft == None: print self.spaceMe(scount) + myNode.payload.name
                    self.printTree(myNode.rgt, scount)
        else:
            if myNode.rgt == None and myNode.lft == None:
                print self.spaceMe(scount) + self.payloadVal(myNode.payload)
            else:
                if myNode.lft != None:
                    print self.spaceMe(scount) + self.payloadVal(myNode.payload)
                    self.printTree(myNode.lft, scount + 4)
                if myNode.rgt != None:
                    if myNode.lft == None:
                        print self.spaceMe(scount) + self.payloadVal(myNode.payload)
                    self.printTree(myNode.rgt, scount)

    def convertTree(self, myNode=None, scount=0):

        if myNode == None:
            myNode = self

        if myNode.rgt == None and myNode.lft == None:
            print self.spaceMe(scount) + myNode.payload.id
            return { 'node': myNode.payload.id }
        else:
            if myNode.lft != None:
                if myNode.rgt == None:
                    print self.spaceMe(
                        scount) + "left guid: " + myNode.lft.payload.id + " node guid: " + myNode.payload.id
                    return {'node':myNode.payload.id, 'lft':self.convertTree(myNode.lft, scount + 4)}
                else:
                    print self.spaceMe(
                        scount) + "left guid: " + myNode.lft.payload.id + " node guid: " + myNode.payload.id + " right guid: " + myNode.rgt.payload.id
                    return { 'node': myNode.payload.id, 'lft': self.convertTree(myNode.lft, scount + 4), 'rgt': self.convertTree(myNode.rgt, scount)}
                self.convertTree(myNode.lft, scount + 4)
            #if myNode.rgt != None:
                #if myNode.lft == None:
                    #print self.spaceMe(scount) + "right guid: " + myNode.rgt.payload.id + " node guid: " + myNode.payload.id
                #self.convertTree(myNode.rgt, scount)



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
