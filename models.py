from google.appengine.ext import ndb

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

class BinaryTree():

    def __init__(self,rootid):
      self.left = None
      self.right = None
      self.rootid = rootid

    def getLeftChild(self):
        return self.left
    def getRightChild(self):
        return self.right
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
            self.left = tree
            tree.left = self.left

    def printTree(self,tree):
        if tree != None:
            tree.printTree(tree.getLeftChild())
            print(tree.getNodeValue())
            tree.printTree(tree.getRightChild())
