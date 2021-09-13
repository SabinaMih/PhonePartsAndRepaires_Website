from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review
from .forms import ReviewForm
from django.core.paginator import Paginator, EmptyPage, InvalidPage 
from django.utils import timezone
from django.views.decorators.http import require_POST


def allProdCat(request, category_id=None):
    c_page = None
    products_list = None
    if category_id != None:
        c_page = get_object_or_404(Category, id=category_id)
        products_list = Product.objects.filter(category=c_page, available=True)
    else:
        products_list = Product.objects.all().filter(available=True)

    '''Paginator code'''
    paginator = Paginator(products_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages) 
        
    return render(request, 'shop/category.html', {'category':c_page, 'products':products})
    

def prod_details(request, category_id, product_id):
    try:
        product = Product.objects.get(category_id=category_id, id=product_id)
    except Exception as e:
        raise e
    return render(request, 'shop/product.html', {'product':product})

# function for our reviews
def add_product_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = request.user
            review.save()
            return redirect('shop:allProdCat')
    else:
        form = ReviewForm()
    return render(request, 'add_product_review.html', {'form':form})