def get_guest_wishlist(request):
    return request.session.get("wishlist", [])


def add_to_guest_wishlist(request, product_id):
    wishlist = request.session.get("wishlist", [])
    if product_id not in wishlist:
        wishlist.append(product_id)
        request.session["wishlist"] = wishlist
    return wishlist


def remove_from_guest_wishlist(request, product_id):
    wishlist = request.session.get("wishlist", [])
    if product_id in wishlist:
        wishlist.remove(product_id)
        request.session["wishlist"] = wishlist
    return wishlist
