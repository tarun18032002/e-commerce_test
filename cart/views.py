from django.shortcuts import render,redirect
from .models import Cart, CartItem
from store.models import Products

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Create your views here.
def add_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:   
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product,quantity=1, cart=cart)
    cart_item.save()
    # print('cart_item', cart_item)
    return redirect('cart')

def cart(request):
    cart_items = None
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except Cart.DoesNotExist:
        pass
    total = 0
    tax = 0
    grand_total = 0
    if cart_items:
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
        tax = (total * 2) / 100
        grand_total = total + tax   
    else:
        cart_items = None   
    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart/cart.html', context)