from .models import Cart, CartItem
from .views import _cart_id

def cart_count(request):
    cart_item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:    
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            cart_item_count = sum(item.quantity for item in cart_items)
        except Cart.DoesNotExist: 
            cart_item_count = 0  
        
        return {'cart_count': cart_item_count}