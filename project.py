from flask import Flask, url_for, redirect, render_template, request, \
jsonify, flash
from sqlalchemy import desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User , Category, Item
import random, string

from flask import session as login_session

#imports for google-plus signins

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web'] \
            ['client_id']

APPLICATION_NAME = "Item Catalog Application"

engine= create_engine("sqlite:///catalog.db")

Base.metadata.bind=engine

DBSession = sessionmaker(bind=engine)

session=DBSession()

app=Flask(__name__)

#JSON END-POINTS

@app.route('/category/JSON')
def CategoryJSON():
	category = session.query(Category).all()
	return jsonify(categories= [c.serialize for c in category])

@app.route('/items/JSON')
def ItemJSON():
	items = session.query(Item).all()
	return jsonify(items= [i.serialize for i in items])

#LOGIN BUTTON FUNCTIONALITY. A STATE VARIABLE IS CREATED HERE.

@app.route('/login/')
def ShowLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
		       for x in xrange(32))
	login_session['state']= state
	return render_template('login.html', STATE=state)

#GOOGLE PLUS CONNECT

@app.route('/gconnect', methods=['POST'])
def gconnect():
	#CHECKING FOR DISCREPANCY IN STATE VARIABLES
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'),401)
		response.headers['Content-type']= 'application/json'
		return response
	code = request.data

	try:
		#UPGRADE OAUTH OBJECT-> CREDENTIALS OBJECT
		oauth_flow = flow_from_clientsecrets('client_secrets.json',scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the'+ 
			'authorization code.'),401)
		response.headers['Content-type'] = 'application/json'
		return response

	# check validity of access token

	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' 
		   %access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url,'GET')[1])
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')),500)
		response.headers['Content-type'] = 'application/json'
		return response

	# verify that the access token is for the intended user

	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps('token user-id does not match'+
			           ' given user id'),401)
		response.headers['Content-type'] = 'application/json'
		return response

	# verify that the access token is valid for this app

	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps('token client-id does not match'+
			       ' app client-id'),401)
		response.headers['Content-type'] = 'application/json'
		return response

	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')

	if stored_credentials is not None and stored_gplus_id == gplus_id:
		response = make_response(json.dumps('The current user is'
			       +' already connected'),200)
		response.headers['Content-type'] = 'application/json'
		return response


	#STORE CREDENTIALS FOR FUTURE USE
	login_session['credentials'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"

  	params = {'access_token': credentials.access_token, 'alt':'json'}

  	answer = requests.get(userinfo_url, params = params)
  	data = answer.json()

  	login_session['username'] = data['name']
  	login_session['picture'] = data['picture']
  	login_session['email'] = data['email']

  	output = ''

  	output += '<h1>Welcome,'
  	output += login_session['username'] + '!</h1>'
  	output += '<img src="'
  	output += login_session['picture']
  	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
  	output += '-webkit-border-radius: 150px;'
  	output += '-moz-border-radius: 150px;"> '

  	flash("you are now logged in as %s" % login_session['username'])
  
  	print "done!"
  	login_session['logged_in'] = True
  	user_id = GetUserID(login_session['email'])
  	if user_id is None:
  		user_id = CreateUser(login_session)
  	login_session['user_id'] = user_id
  	return output

  #USER_RELATED FUNCTIONALITY--CREATION OF USER AND CHECKING.

def CreateUser(login_session):
	newUser = User(name=login_session['username'], 
		      email= login_session['email'])
	session.add(newUser)
	session.commit()
	print "New user successfully created!!"
	login_user = session.query(User).filter(User.name==
	             login_session['username']).one()
	return login_user.id

def GetUserInfo(user_id):
	user = session.query(User).filter(User.id==user_id).one()
	return user

def GetUserID(email):
	try:
		user = session.query(User).filter(User.email==email).one()
		return user.id
	except:
		return None

	#DISCONNECT FROM APPLICATION

@app.route('/gdisconnect')
def gdisconnect():
 	access_token = login_session['credentials']
 	print 'In gdisconnect access token is %s', access_token
 	print 'User name is '
 	print login_session['username']
 	if access_token is None:
 		print 'Access token is none'
 		response = make_response(json.dumps('user is already disconnected'),
 			       401)
 		response.headers['Content-type'] = 'application/json'
 		return response
 	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
 	       % login_session['credentials']
 	h = httplib2.Http()

 	result = h.request(url,'GET')[0]
 	print 'result is'
 	print result

 	if result['status'] == '200':
 		del login_session['credentials']
 		del login_session['gplus_id']
 		del login_session['username']
 		del login_session['picture']
 		del login_session['email']
 		
 		flash("You have disconnected successfully")
 		return redirect('/')
 	else:
 		response = make_response(json.dumps('failed to revoke token for given'+
 			      ' user'), 401)
 		response.headers['Content-type'] = 'application/json'
 		return response

 #LISTS ALL CATEGORIES AND THE LATEST ITEMS

@app.route('/')
def ListAllCategories():
	if 'username' not in login_session:
		categorylist = session.query(Category).all()
		latestitemlist = session.query(Item).order_by(desc(Item.id)).all()
		categoryLatest=[]
		for latestitems in latestitemlist:
			category = session.query(Category) \
			           .filter(latestitems.category_id==Category.id).one()
			categoryLatest.append(category)

		return render_template('listCategories.html',categories=categorylist,
			            latestitems=zip(latestitemlist,categoryLatest))
	else:
		categorylist = session.query(Category).all()
		latestitemlistUser = session.query(Item) \
		                    .filter(Item.user_id== \
			                login_session['user_id']) \
			                .order_by(desc(Item.id)).all()
		print latestitemlistUser
		categoryLatestUser = []
		for latestitems in latestitemlistUser:
			category = session.query(Category) \
			             .filter(latestitems.category_id \
				         ==Category.id).one()
			categoryLatestUser.append(category)
		return render_template('listCategories.html',categories=categorylist,
			            latestitemsUser=zip(latestitemlistUser,categoryLatestUser))


#LISTS ITEMS PER CATEGORY

@app.route('/catalog/<category_name>/items')
def ListItems(category_name):
	if 'username' not in login_session: 
		categorylist = session.query(Category).all()
		category = session.query(Category) \
		           .filter(Category.name==category_name).one()
		categoryId = category.id
		itemList = session.query(Item) \
		           .filter(Item.category_id==categoryId).all()
		numberItems = len(itemList)
		return render_template('listItemsPerCategory.html',
			                    categories = categorylist, items = itemList, 
								category_name=category_name, number=numberItems)
	else:
		categorylist = session.query(Category).all()
		category = session.query(Category) \
		           .filter(Category.name==category_name).one()
		categoryId = category.id
		itemListUser = session.query(Item).filter(Item.category_id \
			           ==categoryId).filter(Item.user_id \
			           ==login_session['user_id']).all()
		numberItems = len(itemListUser)
		return render_template('listItemsPerCategory.html',
								categories = categorylist, 
			                    items = itemListUser, 
								category_name=category_name, 
								number=numberItems)


#DESCRIBES ITEMS
@app.route('/catalog/<category_name>/<item_name>')
#use category name to separately identify two items with same name in different 
#category
def ItemDescription(category_name, item_name):
	category = session.query(Category) \
	           .filter(Category.name==category_name).one()
	categoryId = category.id
	item = session.query(Item).filter(Item.name==item_name).one()
	if(item.category_id==categoryId):
		itemdesc = item.description
		return render_template('itemDescription.html', 
			itemdescription = itemdesc, item = item)


#CRUD OPERATIONS
#create new item
@app.route('/catalog/item/new', methods=['GET','POST'])
def CreateItem():
	if 'username' not in login_session:
		return redirect('/login')
	categories = []
	categoryList = session.query(Category).all()
	for category in categoryList:
		categories.append(category)
	if request.method == 'POST':
		category = request.form['category']
		category_info = session.query(Category).filter(Category.name \
			            ==category).one()
		if category_info is not None:
			newItem = Item(name= request.form['name'], 
				description= request.form['description'], 
				picture= request.form['picture'],
				category_id = category_info.id, 
				user_id = login_session['user_id'] )
			session.add(newItem)
			session.commit()
			flash("New item created successfully")
			return redirect(url_for('ListAllCategories'))
		else:
			flash("You have entered the wrong category. Please check the list"+
				  " of available categories")
	else:
		return render_template('newItem.html', category_list=categories)

#edit an existing item
@app.route('/catalog/<item_name>/edit', methods=['GET','POST'])
def EditItem(item_name):
	if 'username' not in login_session:
		return redirect('/login')

	categories = []
	categoryList = session.query(Category).all()
	for category in categoryList:
		categories.append(category)

	editedItem = session.query(Item).filter(Item.name==item_name).one()
	if (editedItem.user_id != login_session['user_id']):
		return "<script>function myFunction() {alert'+"
		+"'('You are not authorized to edit this item."
		+"Please create your own item in order to edit.');}"
		+"</script><body onload='myFunction()'>"

	if request.method=='POST':
		category = request.form['category']
		category_info = session.query(Category).filter \
		                (Category.name==category).one()
		if request.form['name'] and \
		editedItem.category != request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description'] and \
		editedItem.description != request.form['description']:
			editedItem.description = request.form['description']
		if request.form['category'] and \
		editedItem.category_id != category_info.id:
			editedItem.category_id = category_info.id
		if request.form['picture'] and \
		editedItem.picture != request.form['picture']:
			editedItem.picture = request.form['picture']
		

		session.commit()
		flash("Item edited successfully")
		return redirect(url_for('ListAllCategories'))
	else:
		return render_template('editItem.html', item_name= item_name, 
			category_list = categories, item=editedItem)

#delete an existing item
@app.route('/catalog/<item_name>/delete', methods=['GET','POST'])
def DeleteItem(item_name):
	if 'username' not in login_session:
		return redirect('/login')

	deleteItem = session.query(Item).filter(Item.name== item_name).one()
	if (deleteItem.user_id != login_session['user_id']):
		return "<script>function myFunction() {alert" \
		       +"('You are not authorized to edit this item." \
		 	   +" Please create your own item in order to edit.');}" \
		       +"</script><body onload='myFunction()'>"
	
	if request.method=='POST':
		session.delete(deleteItem)
		session.commit()
		flash("Item deleted successfully")
		return redirect(url_for('ListAllCategories'))
	else:
		return render_template('deleteItem.html', item_name=item_name)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
