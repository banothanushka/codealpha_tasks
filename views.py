from django.shortcuts import render, redirect, get_object_or_403
from .models import Product

def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'shop/product_list.html', {
        'products': products,
        'cart_count': cart_count
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('product_list')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    cart_count = sum(cart.values())

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'id': product_id,
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'shop/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count
    })

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    product_id_str = str(item_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')
def checkout(request):
    cart = request.session.get('cart', {})
    
    
    if not cart:
        return redirect('cart_detail')
        
    if request.method == 'POST':
        
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        
        request.session['cart'] = {}
        request.session.modified = True
        
        return redirect('order_success')
        
    return render(request, 'shop/checkout.html')

def order_success(request):
    return render(request, 'shop/order_success.html')
