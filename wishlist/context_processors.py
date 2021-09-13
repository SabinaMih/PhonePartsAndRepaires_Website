from .models import Wishlist, WishlistItem
from .views import _wishlist_id

def counterW(request):
    item_countw = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            wishlist = Wishlist.objects.filter(wishlist_id=_wishlist_id(request))
            wishlist_items = WishlistItem.objects.all().filter(wishlist=wishlist[:1])
            for wishlist_item in wishlist_items:
                item_countw += wishlist_item.quantity
        except Wishlist.DoesNotExist:
            item_countw = 0
    return dict(item_countw = item_countw)