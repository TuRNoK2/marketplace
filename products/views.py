from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy


from django.shortcuts import render

from .forms import ProductForm, ProductEditForm
from .models import Product

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product

def product_list(request):
    product_list = Product.objects.all().order_by('-id')
    paginator = Paginator(product_list, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {'page_obj': page_obj})

def home(request):
    return render(request, 'home.html')




@login_required
def create_product(request):
    if not request.user.is_seller:
        return HttpResponseForbidden("Только продавцы могут добавлять товары.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('my_products')
    else:
        form = ProductForm()

    return render(request, 'products/product_create.html', {'form': form})

@login_required
def my_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products/my_products.html', {'products': products})



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)  # Только свои товары
    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('my_products')
    else:
        form = ProductEditForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form})





def cart_view(request):
    return render(request, 'cart/cart.html')