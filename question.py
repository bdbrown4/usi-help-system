from main import app
from flask import render_template,flash,redirect,url_for,request
from models import Item, BinaryTree
from forms import ItemForm, DelForm, EditForm
from google.appengine.ext import ndb
import uuid

# test tree

# @app.route('/question',methods=['GET','POST'])
# def testTree():
#     myTree = BinaryTree("Maud")
#     myTree.insertLeft("Bob")
#     myTree.insertRight("Tony")
#     myTree.insertRight("Steven")
#     myTree.insertLeft("Mike")
#     myTree.printTree(myTree)
#     myTree.getLeftChild()
#     myTree.getNodeValue()
#     myTree.getRightChild()
#     return redirect(url_for('questiontree'))
#     return render_template('questiontree.html',
#                            myTree = myTree
#                            )