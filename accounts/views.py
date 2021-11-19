from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from .filter import Orderfilter
from accounts.models import *
from .forms import CustomerForm, OrderForm,CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorator import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group

# Create your views here.
@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			
			messages.success(request, 'Account was created for ' + username)	
			return redirect('loginPage')
	
	context = {'form':form}
	return render(request, 'accounts/register.html',context)	

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password) 
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}	
	return render(request, 'accounts/login.html',context)	

def logoutUser(request):
	logout(request)
	return redirect('loginPage')

@login_required(login_url='loginPage')
@admin_only
def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status = 'Delivered').count()
	pending = orders.filter(status = 'Pending').count()	
	context = {'customers':customers,'orders':orders,'total_orders':total_orders,'delivered':delivered,
	'pending':pending
	}

	return render(request,'accounts/home.html',context)


@login_required(login_url='loginPage')
@allowed_users(allowed = ['customer'])	
def userprofile(request):
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()
	delivered = orders.filter(status = 'Delivered').count()
	pending = orders.filter(status = 'Pending').count()	
	context = {'orders':orders,'total_orders':total_orders,'delivered':delivered,
	'pending':pending}
	return render(request, 'accounts/userprofile.html',context)	

@login_required(login_url='loginPage')
@allowed_users(allowed = ['customer'])
def settings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()
		
	context = {'form':form}
	return render(request, 'accounts/accountSettings.html',context)	



@login_required(login_url='loginPage')
@allowed_users(allowed = ['admin'])
def products(request):
	products = Product.objects.all()
	return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='loginPage')
@allowed_users(allowed = ['admin'])
def customer(request,pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()
	myFilter = Orderfilter(request.GET, queryset=orders)
	orders = myFilter.qs 


	context = {'customer':customer, 'orders':orders, 'order_count':order_count,'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed = ['admin'])
def createorder(request,pk_test):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),can_delete=False)
	customer = Customer.objects.get(id=pk_test)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset':formset}

	return render(request, 'accounts/order_form.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed = ['admin'])
def updateorder(request,pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	
	context = {'form':form}
	
	return render(request, 'accounts/order_form.html',context)

@login_required(login_url='loginPage')
@allowed_users(allowed = ['admin'])
def deleteorder(request,pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'order':order}
	return render(request, 'accounts/delete.html',context)	

