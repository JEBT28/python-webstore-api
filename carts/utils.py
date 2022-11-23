from .models import Cart

def get_or_create_cart(request):
    user = request.user if request.user.is_authenticated() else None #puede o no pertenecer a un user
    cart_id = request.session.get('cart_id')
    cart = Cart.objects.filter(cart_id=cart_id).first() #Lista de objetos que cumplan con la condicion
    if cart is None:
        cart = Cart.objects.create(user=user) #si no existe el cart se crea
    if user and cart.user is None:
        cart.user = user
        cart.save()
    request.session['cart_id'] = cart.cart_id
    #duda de como mandarlo en angular
    return cart