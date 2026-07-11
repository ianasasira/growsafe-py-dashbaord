from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, ProductCategory
from .forms import ProductForm

@login_required
def product_list(request):
    products = Product.objects.select_related('category').all()
    categories = ProductCategory.objects.all()
    
    if q := request.GET.get('q'):
        products = products.filter(name__icontains=q)
    if category := request.GET.get('category'):
        products = products.filter(category_id=category)
    if status := request.GET.get('status'):
        products = products.filter(status=status)
    
    return render(request, 'dashboard/products/list.html', {
        'products': products,
        'categories': categories,
    })

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:list')
    else:
        form = ProductForm()
    
    return render(request, 'dashboard/products/form.html', {'form': form})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'dashboard/products/detail.html', {'product': product})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'dashboard/products/form.html', {'form': form, 'product': product})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('catalog:list')
    return render(request, 'dashboard/products/delete.html', {'product': product})
