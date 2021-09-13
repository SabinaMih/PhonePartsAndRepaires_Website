from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

def add_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(
                wishlist_id=_wishlist_id(request)
            )
        wishlist.save()
    try:
        wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
        wishlist_item.quantity += 1
        wishlist_item.save()
    except WishlistItem.DoesNotExist:
        wishlist_item = WishlistItem.objects.create(
                    product = product, 
                    quantity = 1, 
                    wishlist = wishlist
            )
        wishlist_item.save()
    return redirect('wishlist:wishlist_detail')

def wishlist_detail(request, wtotal=0, wcounter=0, wishlist_items = None):
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, active=True)
        for wishlist_item in wishlist_items:
            wtotal += (wishlist_item.product.price * wishlist_item.quantity)
            wcounter += wishlist_item.quantity 
    except ObjectDoesNotExist:
        pass

    return render(request, 'wishlist.html', {'wishlist_items':wishlist_items, 'wtotal':wtotal, 'wcounter':wcounter})

def wishlist_remove(request, product_id):
    wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    if wishlist_item.quantity > 1:
        wishlist_item.quantity -= 1
        wishlist_item.save()
    else:
        wishlist_item.delete()
    return redirect('wishlist:wishlist_detail')

def wishlist_full_remove(request, product_id):
    wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    wishlist_item.delete()
    return redirect('wishlist:wishlist_detail')
