import json

from django.http  import JsonResponse
from django.views import View

from products.models import Product, Cart
from orders.models   import Order, OrderItem
from users.models    import User
from user_auth       import authentication

class CartView(View):
    @authentication
    def post(self, request):
        data        = json.loads(request.body)
        current_user_id = request.user

        try:
            user_id           = current_user_id
            product_id        = data['product_id']
            purchase_quantity = data['quantity']
            current_quantity  = 0

            if not Product.objects.filter(id = product_id).exists():
                return JsonResponse( {'MESSAGE' : 'PRODUCT DOES NOT EXIST'}, status = 400)

            if Cart.objects.filter(user_id= user_id, product_id = product_id):
                current_quantity = Cart.objects.get(user_id = user_id, product_id = product_id).purchase_quantity

            Cart.objects.update_or_create(product_id = product_id, user_id = user_id, defaults = { 'purchase_quantity' : int(current_quantity) + int(purchase_quantity) })

            return JsonResponse( {'MESSAGE' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse( {'MESSAGE' : 'KEY ERROR'}, status = 400)

    @authentication
    def get(self, request):
        current_user_id = request.user
        
        carts = Cart.objects.filter(user_id = current_user_id)

        if not carts.exists():
            return JsonResponse( {'MESSAGE' : 'EMPTY CART'}, status = 204)
        
        return JsonResponse( {'MESSAGE' : [
            {
                "product_img"  : cart.product.productimage_set.first().image_url,
                "price"        : cart.product.price,
                "name"         : cart.product.name,
                "package_type" : cart.product.package_type[:2],
                "quantity"     : cart.purchase_quantity
                }
        for cart in carts]}, status = 201)