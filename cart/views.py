# views.py (cart app)

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from product.models import Product
from .models import CartItem
from django.shortcuts import get_object_or_404
from reportlab.pdfgen   import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4



# 🔹 1. Called from Home Page, redirects to Products Page
@login_required(login_url='login')
def add_to_cart_from_home(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
        except Product.DoesNotExist:
            return redirect('home_page')
        return redirect('products_page')  # ✅ Redirect to product page to shop more
    return redirect('home_page')

# 🔹 2. Called from Products Page, stays on the same page
@login_required(login_url='login')
def add_to_cart_from_products(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
        except Product.DoesNotExist:
            return redirect('products_page')
        return redirect('products_page')  # ✅ Stay on same page
    return redirect('products_page')

# 🔹 3. Cart Page View
@login_required(login_url='login')
def cart_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart_page.html', {'cart_items': cart_items, 'total_price': total_price})



# 🔼 Increase the quantity of a cart item
def increase_quantity(request, item_id):
    # Check if the request is a POST request (form submission)
    if request.method == "POST":
        # Fetch the CartItem object for the current user and given item_id, or show 404 if not found
        item = get_object_or_404(CartItem, id=item_id, user=request.user)

        # Increase the quantity by 1
        item.quantity += 1

        # Save the updated object to the database
        item.save()

        # Redirect to the cart page after updating
        return redirect('cart_page')

    # If the request is not POST, just redirect to cart page
    return redirect('cart_page')


# 🔽 Decrease the quantity of a cart item
def decrease_quantity(request, item_id):
    # Check if the request is a POST request (form submission)
    if request.method == "POST":
        # Fetch the CartItem object for the current user and given item_id, or show 404 if not found
        item = get_object_or_404(CartItem, id=item_id, user=request.user)

        # Decrease the quantity by 1
        item.quantity -= 1

        # If quantity becomes 0 or less, remove the item from cart
        if item.quantity <= 0:
            item.delete()
        else:
            # Otherwise, save the updated object
            item.save()

        # Redirect to the cart page after updating
        return redirect('cart_page')

    # If the request is not POST, just redirect to cart page
    return redirect('cart_page')

def gernrate_invoice(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)   # bring the cart items for the user how is currently logging 

    if not cart_items:
        return HttpResponse("Your cart is empty.")
    
    total = sum(item.product.price * item.quantity for item in cart_items)

    response = HttpResponse(content_type ="application/pdf")
    response['content-Dispostion'] = 'attachment: filename ="invoice.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width , height = A4
    y = height -50  # Adjust height for header
    p.setFont("Helvetica", 16)
    p.drawString(30, y, f"Invoice for {user.username}")

    y -= 30  # Move down for items
    p.setFont("Helvetica", 16)
    p.drawString(50, y, "Product:")
    p.drawString(250, y, "Qty:")
    p.drawString(300, y, "Price:")
    p.drawString(400, y, "Subtotal:")

    y -= 20  # Start below header 

    for item in cart_items:
        subtotal = item.quantity * item.product.price

        # Write entire row in same line
        p.drawString(50, y, item.product.name)                     # Product Name
        p.drawString(250, y, str(item.quantity))                   # Qty
        p.drawString(320, y, f"₹{item.product.price:.2f}")         # Price
        p.drawString(420, y, f"₹{subtotal:.2f}")                   # Subtotal

        y -= 20  # Move to next line for next product

    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(300, y, "Total:")
    p.drawString(400, y, f"₹{total}")
    p.showPage()
    p.save()
    return response
