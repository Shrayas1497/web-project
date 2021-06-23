from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User,auth
import sqlite3
import random
 # Create your views here

db_connector = sqlite3.connect('shrayas.db')
db_cursor = db_connector.cursor()

# db_cursor.execute('DROP TABLE IF EXISTS mobiles')
# db_connector,commit()

cart = []


# def dictionaryFactory(cursor, row):
# 	d = {}
# 	for idx, col in enumerate(cursor.description):
# 		d[col[0]] = row[idx]
# 	return d

# db_row_factory = dictionaryFactory

def register(request):
	if request.method=='POST':
		email_id = request.POST['email']
		email_id = email_id.split('@')
		email_id[1] = email_id[1]
		email_id = ''.join(email_id)
		first_name=request.POST['username']
		# last_name=request.POST['password'] 
		password1=request.POST['password1']
		password2=request.POST['password2']
		email=email_id

		if password1==password2:
			db_connector = sqlite3.connect('shrayas.db')
			db_cursor = db_connector.cursor()

			size = len(list(db_cursor.execute('SELECT * FROM user')))
			db_connector = sqlite3.connect('shrayas.db')
			db_cursor = db_connector.cursor()
			db_cursor.execute('INSERT INTO user(userid, email, password) VALUES(' + str(size + 1) + ',\"' + email +'\",' +  password1+')')
			#db_cursor.execute('INSERT INTO payment(user_id, payment_id) VALUES(' + str(size + 1) + ',\"' + email +'\",' +  pa')')
			# user=User.objects.create_user(username=first_name,password=password1,email=email)
			# user.save();
			db_connector.commit()
			print('user created')
		else:
			print('password not matching')
	return redirect('/')				

def home(request):
	user = request.session
	# print('this is home', )
	return render(request,'home.html', {'data': ('userId' in user)})

def login(request):
	if request.method=='POST':
		email_id = request.POST['email']
		email_id = email_id.split('@')
		email_id[1] = email_id[1]
		email_id = ''.join(email_id)
		username=email_id
		password=request.POST['password']
		db_connector = sqlite3.connect('shrayas.db')
		db_cursor = db_connector.cursor()
		data = list(db_cursor.execute('SELECT * FROM user'))
		print(data, username, password)
		for i in data:
			if(i[1] == username and i[2] == password):
				request.session['userId'] = {'id': i[0], 'cart': {}}
				# return redirect('/register')
				return HttpResponseRedirect('/')
		return HttpResponse('Invalid details')
	else:
		return render(request,'login sliding.html')

def logout(request):
   try:
      del request.session['userId']
   except:
      pass
   return redirect('/')

def mobiles(request):
	db_connector = sqlite3.connect('shrayas.db')
	db_cursor = db_connector.cursor()
	data = list(db_cursor.execute('SELECT * FROM mobiles'))
	# print(data)
	return render(request,'mobiles.html', {'data':data})

def laptops(request):
	db_connector = sqlite3.connect('shrayas.db')
	db_cursor = db_connector.cursor()
	data = list(db_cursor.execute('SELECT * FROM laptops'))
	# print(data)
	return render(request,'laptops.html', {'data':data})
	# return render(request,'laptops.html')
	dests=w.objects.all()
def tablets(request):
	db_connector = sqlite3.connect('shrayas.db')
	db_cursor = db_connector.cursor()
	data = list(db_cursor.execute('SELECT * FROM tabs'))
	# print(data)
	return render(request,'tabs.html', {'data':data})
	# return render(request,'tabs.html')
def headsets(request):
	print("in headsets")
	db_connector = sqlite3.connect('shrayas.db')
	db_cursor = db_connector.cursor()
	data = list(db_cursor.execute('SELECT * FROM headsets'))
	# print(data)
	return render(request,'headsets.html', {'data':data})

def gallery(request):
	return render(request,'gallery.html')

def cart(request):
	if('userId' in request.session):
		user = request.session['userId']
		userId = user['id']
		cart = user['cart']
		item = []
		total = 0
		print(cart, len(cart))
		if(len(cart) == 0):
			return HttpResponse("Cart is <strong>EMPTY</strong><br><a href='/'>GO TO HOME</a>")
		db_connector = sqlite3.connect('shrayas.db')
		db_cursor = db_connector.cursor()
		for i in cart:
			for j in cart[i]:
				query = "SELECT * FROM " + i+'s' + ' WHERE ' + i+'_id=' + j 
				data = list(db_cursor.execute(query))
				print(data)
				item.append((data[0][1], data[0][2]))
				total += int(data[0][2])
		print(item)
		return render(request,'payment.html',{'item': item, 'l': len(item), 'total': total})
	else:
		return redirect('/login')

def buynow(request):
	if ('userId' in request.session):
		user = request.session['userId']
		userId = user['id']
		cart = user['cart']
		incart = {}
		for i in request.GET:
			incart[i] = request.GET[i]
		print(incart, cart)
		for i in incart:
			if(i in cart):
				cart[i].append(incart[i])
			else:
				cart[i] = [incart[i]]
		request.session['userId'] = {'id': userId, 'cart': cart}
		
		return redirect('/cart')
	else:
		return redirect('/login')

def clearcart(request):
	user = request.session['userId']
	userId = user['id']
	cart = {}
	request.session['userId'] = {'id': userId, 'cart': cart}
	return redirect('/cart')

def addtocart(request):
	if ('userId' in request.session):
		print('--------->', request.META.get('HTTP_REFERER'))
		# print('This is add cart', request.GET)
		user = request.session['userId']
		userId = user['id']
		cart = user['cart']
		incart = {}
		for i in request.GET:
			incart[i] = request.GET[i]
		print(incart, cart)
		for i in incart:
			if(i in cart):
				cart[i].append(incart[i])
			else:
				cart[i] = [incart[i]]
		request.session['userId'] = {'id': userId, 'cart': cart}
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		return redirect('/login')

def payment(request):
	
 	return render(request,'/modals.html')


def setsession(request):
	request.session['userId'] = {'id': '0', 'cart':['A', 'B']}
	return HttpResponse('Session is set')

def showsession(request):
	user = request.session['userId']
	userId = user['id']
	cart = user['cart']
	return HttpResponse('This is session variable: ' + userId + ' and this is its cart: ' + cart[0] + ' ' + cart[1])

def modals(request):
	user = request.POST['firstname']
	address=request.POST['address']
	city=request.POST['city']
	mobile=request.POST['phno']
	user_id= str(request.session['userId']['id'])

	payment_id = random.randint(0,10000)
	payment_id = str(payment_id)
	# state=request.POST['state']
	state="Karnataka"
	db_connector = sqlite3.connect('shrayas.db')
	db_cursor = db_connector.cursor()
	db_cursor.execute('INSERT INTO payment(payment_id,user_id,full_name,address,city,mobile_number,state) VALUES( \"' + payment_id + '\", \"' + user_id + '\",\"' + user + '\", \"' + address + '\", \"' + city + '\", \"' + mobile + '\", \"Karnataka\")')	
	db_connector.commit()

	return render(request,'modals.html')
