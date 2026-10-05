from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category

def home_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:6]
    return render(request, 'home_page.html', {
        'categories': categories,
        'products': products
    })

@login_required(login_url='/account/login/')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price_raw = request.POST.get('price')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')
    

        try:
            price = Decimal(price_raw)
        except (TypeError, ValueError, InvalidOperation):
            return render(request, 'add_product.html', {
                'error': 'Price must be a number (e.g. 99.99).',
                'categories': Category.objects.all()
            })

        if price.as_tuple().exponent < -2 or abs(price) >= Decimal('100000.00'):
            return render(request, 'add_product.html', {
                'error': 'Price must be between 0.00 and 999999.99',
                'categories': Category.objects.all()
            })

        try:
            category_obj = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(request, 'add_product.html', {
                'error': 'Invalid category selected.',
                'categories': Category.objects.all()
            })

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            Product_image=image,
            Categories=category_obj,
        )

        return redirect('home_page')

    return render(request, 'add_product.html', {
        'categories': Category.objects.all()
    })

def products_page(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(Categories__id=category_id)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
       
        'selected_category': int(category_id) if category_id else None
    }
    return render(request, 'products_page.html', context)

@login_required(login_url='/account/login/')
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
    except Product.DoesNotExist:
        pass
    return redirect('products_page')

def product_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories = Category.objects.all()
    products = Product.objects.filter(Categories=category)
    return render(request, 'products_page.html', {
        'products': products,
        'categories': categories,
        'selected_category': category.id
    })
    

def home_search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            products = Product.objects.filter(name__icontains = query)
        else:
            products = Product.objects.all()
        return render(request, 'products_page.html', {'products': products})
    
def product_search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            products = Product.objects.filter(name__icontains = query)
        else:
            products = Product.objects.all()
        return render(request, 'products_page.html', {'products': products})