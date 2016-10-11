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
