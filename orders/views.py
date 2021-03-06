import json

from django.http  import JsonResponse
from django.views import View

from products.models import Product, Cart
from user_auth       import authentication

class CartView(View):
    @authentication
    def post(self, request):
        data            = json.loads(request.body)
        current_user_id = request.user

        try:
            user_id           = current_user_id
            product_id        = data['product_id']
            purchase_quantity = data['quantity']

            if not Product.objects.filter(id = product_id).exists():
                return JsonResponse( {'MESSAGE' : 'PRODUCT DOES NOT EXIST'}, status = 400)

            if Cart.objects.filter(user_id = user_id, product_id = product_id).exists():
                current_product                    = Cart.objects.get(product_id = product_id, user_id = user_id)
                current_product.purchase_quantity += int(purchase_quantity)
                current_product.save()

            else:
                Cart.objects.create(
                    user_id           = user_id,
                    product_id        = product_id, 
                    purchase_quantity = purchase_quantity
                    )

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

    @authentication
    def delete(self, request):
        try:
            current_user_id = request.user
            selected_list   = request.GET.getlist('product-id')

            product_in_cart = Cart.objects.filter(product_id__in = selected_list, user_id = current_user_id)
            
            if not product_in_cart.exists():
                return JsonResponse( {'MESSAGE' : 'NO ITEM TO REMOVE'}, status = 400)

            product_in_cart.delete()

            return JsonResponse( {'MESSAGE' : 'SUCCESSFULLY DELETED'}, status = 200)
            
        except KeyError:
            return JsonResponse( {'MESSAGE' : 'KEY ERROR'}, status = 400)