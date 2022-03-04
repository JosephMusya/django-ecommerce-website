# from email.mime import application
# from itertools import product
from django.http import FileResponse, JsonResponse
from django.shortcuts import render,redirect
from .models import Product,Category,Cart,Order,OrderItem,Profile
from django.contrib import messages
from .forms import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth .models import User
from django.db.models import Q
from random import randint
from fpdf import FPDF
# Create your views here.

def home(request):    
    categories = Category.objects.all()
    if request.method == "GET":
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        available_prod = Product.objects.filter(
            Q(name__icontains=q)
        )
        
        if available_prod:
            context = {'properties':available_prod, 'categories':categories}
            return render(request,'base/home.html',context)
        else:
            context = {'properties':available_prod, 'categories':categories}
            messages.info(request,"No product found")
            return render(request,'base/home.html',context)

def viewCategory(request,pk):
    id = Category.objects.only('id').get(names=pk).id
    item = Product.objects.all().filter(category = id)
    context = {'items':item,'category':pk}
    return render(request, 'base/view_category.html', context)

def viewSingle(request,pk):
    #i = Product.objects.only('id').get(name=pk).id
    item = Product.objects.get(id=pk)
    context = {'item':item}

    return render(request, 'base/view_single.html', context)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login was successful. Welcome " + username)
            return redirect('home')
            
        else:
            messages.error(request, "Login failed! Confirm your credentials")

    return render(request, 'base/login.html')

def logoutUser(request):
    logout(request)
    messages.warning(request,"You have logged out")
    return redirect('home')

def registerUser(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            #username = CustomUserForm(request.POST.get('username'))
            #password = CustomUserForm(request.POST.get('password2'))
            #user = authenticate(request, username=username,password=password)
            messages.success(request, "Registration successful")
            #login(request, user)
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'base/register.html', context)

def addItem(request):
    item = Product()
    categories = Category.objects.all()
    context = {'categories':categories}
    
    if request.method == "POST":
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.price = request.POST.get('price')
        item.img = request.FILES['image']
        #item.category = request.POST.get('category')
        item.save()
        messages.success(request,"Item was added successfuly")

        return redirect('add-item')
            
    return render(request,'base/add_item.html',context)   

def viewItem(request):
    item = Product.objects.all()
    context = {'item':item}
    
    return render(request,'base/view_item.html', context)

def editItem(request,pk):
    item = Product.objects.get(id=pk)
    context = {'item':item}
    
    if request.method=="POST":
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.price = request.POST.get('price')
        item.save()
        messages.success(request, str(item.name)+" updated successfully")
        return redirect('view-item')

    return render(request,'base/edit_item.html',context)

def addCart(request):  
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_name = str(request.POST.get('product_name'))
            product_qty = int(request.POST.get('product_quantity'))
            if Cart.objects.filter(user=request.user.id,
                                    product_id=product_id):
                return JsonResponse({'status': 'Item already in Cart'})
        
            else:                                   
                availableQty= Product.objects.get(id=product_id).quantity
                if availableQty >=  product_qty:
                    Cart.objects.create(user=request.user,
                                        product_id=product_id,
                                        product_qty=product_qty,
                                        )
                    return JsonResponse({'status': 'Item added to Cart'})
                else:
                    return JsonResponse({'status': 'only {} {} available'.format(str(availableQty),str(product_name))})

        else:
            return JsonResponse({'status': 'Login required to shop!!!'})
    return redirect('/')

@login_required(login_url = 'login')
def viewCart(request):
    cart = Cart.objects.filter(user=request.user)
    total_items,total_price = [],[]
    checkout = []
    for item in cart:
        number = item.product_qty
        price = item.product.price
        total_price.append(price)
        total_items.append(number)
    if cart:
        if item.product.quantity >= item.product_qty:
            checkout = True
        else:
            checkout = False

    total_qty = sum(total_items)
    total_price = sum(total_price)
    
    context = {'cart': cart, 'total_price':total_price, 'total_qty':total_qty,'checkout':checkout}
    return render(request, 'base/cart.html', context)

def editCart(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user.id,
                        product_id=product_id):
            product_qty = int(request.POST.get('product_quantity'))
            cart = Cart.objects.get(product_id = product_id)
            cart.product_qty = product_qty
            cart.save()
            return JsonResponse({'status': 'Cart Updated'})
    return redirect('/')

def remove(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id')) 
        if Cart.objects.filter(user=request.user.id,
                        product_id=product_id):
            
            cartItem = Cart.objects.get(product_id=product_id)
            cartItem.delete()            
    return redirect('/')

def checkout(request):
    userprofile = Profile.objects.filter(user=request.user).first()
    rawCart = Cart.objects.filter(user=request.user)
    raw_price = []
    for item in rawCart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)
        
        cartItems = Cart.objects.filter(user=request.user)
        
        i = item.product.price * item.product_qty
        raw_price.append(i)
    
    total_price = sum(raw_price)
    
    context = {'cartItems':cartItems, 'total_price':total_price,'userprofile':userprofile}
    return render(request, 'base/checkout.html', context)

@login_required(login_url = 'login')
def placeOrder(request):
    if request.method == 'POST':
        current_user = User.objects.filter(id=request.user.id).first()
        
        if not current_user.first_name:
            current_user.first_name = request.POST.get('f_name')
            current_user.last_name = request.POST.get('l_name')
            current_user.save()
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.town = request.POST.get('town')
            userprofile.email = request.POST.get('email')
            userprofile.description = request.POST.get('description')
            userprofile.save()            
        
        newOrder = Order()
        newOrder.user = request.user
        newOrder.f_name = request.POST.get('f_name')
        newOrder.l_name = request.POST.get('l_name')
        newOrder.phone = request.POST.get('phone')
        newOrder.town = request.POST.get('town')
        newOrder.email = request.POST.get('email')
        newOrder.description = request.POST.get('description')
        newOrder.total_price = request.POST.get('total_price')
        newOrder.payment_mode = request.POST.get('payment_mode')
        
        #payment_mode = request.POST.get('payment_mode')
        
        track_no = str(request.user)+str(randint(000000,999999))
        while Order.objects.filter(track_no=track_no) is None:
            track_no = track_no
        newOrder.track_no = track_no
        newOrder.save()
        
        newOrder_items = Cart.objects.filter(user=request.user)
    
        pdf = FPDF('p','mm','A5')
        pdf.add_page()
        pdf.set_font('Arial','', 11)
        pdf.cell(40,10,'BENBIZ')
        pdf.ln()

        for item in newOrder_items:
            OrderItem.objects.create(
                order = newOrder,
                product = item.product,
                price = item.product.price,
                quantity = item.product_qty,             
            )
            
            orderProduct = Product.objects.filter(id=item.product_id).first()
            orderProduct.quantity = orderProduct.quantity-item.product_qty
            if orderProduct.quantity < 1:
                orderProduct = 0
            orderProduct.save()

            pdf.set_font('Arial','', 11)
            pdf.cell(40,5,'{}....................{} x {}'.format(item.product,item.product.price,item.product_qty))
            pdf.ln()
            
        pdf.ln()
        pdf.cell(40,5,'Order Made by: {} {}'.format(newOrder.f_name,newOrder.l_name))    
        pdf.ln()
        pdf.cell(40,5,'Date: {}'.format(newOrder.created_at))
        pdf.ln()
        pdf.cell(40,5,'Tracking Number: {}'.format(str(track_no)))
        pdf.ln()
        pdf.cell(40,5, 'Destination: {}'.format(newOrder.town))
        pdf.ln()
        pdf.cell(40,5, 'Total Price: {}'.format(newOrder.total_price))
        pdf.ln()
        pdf.cell(40,5, 'Payment Mode: {}'.format(newOrder.payment_mode))
        pdf.ln()
        pdf.cell(40,5,"Help line: +254757405701")
        pdf.ln()
        pdf.cell(40,5, "Retain this receipt as a proof of purchase")
        pdf.output('Receipt_{}.pdf'.format(str(track_no)))
        #receipt_name = str('Receipt_{}.pdf'.format(str(track_no)))
        
        #upload_r = Cart.objects.get(user=request.user)
        #upload_r.receipt = receipt_name
        #upload_r.save()
        #newOrder.receipt = receipt_name
        #newOrder.save()
        #downloadReceipt(receipt_name)
        Cart.objects.filter(user=request.user).delete() 
        #return JsonResponse({'status': 'Item already in Cart'})   
        messages.success(request,"Your has been placed successfully. Download Receipt")    
    return redirect('/')

def downloadReceipt(pdf_name):
    return FileResponse(open('static/{}'.format(pdf_name), 'rb'),
                        as_attachment=True, content_type='application/pdf')

def orderHistory(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request,'base/history.html', context)

def viewHistory(request,pk):
    order = Order.objects.filter(id=pk).filter(user=request.user).first()
    ordered_items = OrderItem.objects.filter(order=order)
    context = {'order':order, 'ordered_items':ordered_items}
    return render(request, 'base/view_history.html', context)

def prodList(request):
    products = Product.objects.filter().values_list('name',flat=True)
    prod_list = list(products)
    return JsonResponse (prod_list, safe=False)

def dispCart(request):

    cart = Cart.objects.filter(user=request.user.id)
    no_items = []
    if cart:
        for items in cart:
            no_items.append(items.product_qty)
    items = sum(no_items)
  
    context = {'items':items,'checkout':checkout}
    return render(request, 'main.html', context)