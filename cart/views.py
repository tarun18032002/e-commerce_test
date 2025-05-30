from django.shortcuts import render,redirect,get_object_or_404
from .models import Cart, CartItem
from store.models import Products,Variation
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Create your views here.
def add_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try: 
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass 
    product = Products.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:   
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if len(product_variation)>0:
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product,quantity=1, cart=cart)
        if len(product_variation)>0:
            for item in product_variation:
                cart_item.variations.add(item)
    cart_item.save()
    return redirect('cart')

def cart(request):
    cart_items = None
    total = 0
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if cart_items:
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
            tax = (total * 2) / 100
            grand_total = total + tax   
        else:
            cart_items = None   
    except ObjectDoesNotExist:
        pass
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart/cart.html', context)


def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product = get_object_or_404(Products,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')