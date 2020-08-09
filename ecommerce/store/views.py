from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json

def store(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order = {
            'get_cart_items': 0,
        }
    cart_items = order.get_cart_items
    context = {
        'products': products,
        'cart_items': cart_items,
    }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0,
        }
    cart_items = order.get_cart_items
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0,
        }
    cart_items = order.get_cart_items
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html',context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(product=product, order=order)
    print(f'order_item created: {created}')

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)