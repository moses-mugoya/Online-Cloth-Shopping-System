from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Review
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForm, FeedbackForm
from django.contrib import messages
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required


def product_list(request, category_slug=None):
    category = None
    shirt_cat = Category.objects.get(name='Shirts')
    trousers = Category.objects.get(name='Men trousers')
    women_trousers = Category.objects.get(name='Women trousers')
    women_suit = Category.objects.get(name='Women suit')
    blouse = Category.objects.get(name='Blouses')
    dress = Category.objects.get(name='Dresses')
    men_suit = Category.objects.get(name='Men suit')
    sweater = Category.objects.get(name='Sweaters')
    others = Category.objects.get(name='Others')
    shoes = Category.objects.get(name='Shoes')
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'catalog/list.html', {'category': category,
                                                 'categories': categories,
                                                 'page': page,
                                                 'products': products,
                                                 'shirt': shirt_cat,
                                                 'trousers': trousers,
                                                 'women_trousers': women_trousers,
                                                 'women_suit': women_suit,
                                                 'blouse': blouse,
                                                 'dress': dress,
                                                 'men_suit': men_suit,
                                                 'sweater': sweater,
                                                 'shoes': shoes,
                                                 'others': others,
                                                 })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviews = product.reviews.filter(active=True)

    review_count = product.reviews.count()

    paginator = Paginator(reviews, 3)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    cart_product_form = CartAddProductForm()
    return render(request,
                  'catalog/detail.html',
                  {'product': product,
                   'reviews': reviews,
                   'review_count': review_count,
                   'cart_product_form': cart_product_form})


@login_required
def product_review(request, id):
    product = get_object_or_404(Product, id=id, available=True)
    reviews = product.reviews.filter(active=True)

    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)

        if review_form.is_valid():
            new_review_form = review_form.save(commit=False)
            new_review_form.product = product
            new_review_form.user = request.user
            new_review_form.save()
            messages.success(request, 'Your review has successfully been submitted')
    else:
        review_form = ReviewForm()

    review_count = product.reviews.count()

    cart_product_form = CartAddProductForm()

    return render(request,
                  'catalog/review.html',
                  {'product': product,
                   'reviews': reviews,
                   'review_form': review_form,
                   'review_count': review_count,
                   'cart_product_form': cart_product_form})


def help_center(request):
    return render(request, 'catalog/help.html')


def returns_policy(request):
    return render(request, 'catalog/returns.html')


def secure_payment(request):
    return render(request, 'catalog/payment.html')


def responsibility(request):
    return render(request, 'catalog/responsibility.html')


def privacy(request):
    return render(request, 'catalog/privacy.html')


def delivery(request):
    return render(request, 'catalog/delivery.html')


def careers(request):
    return render(request, 'catalog/career.html')


def conditions(request):
    return render(request, 'catalog/conditions.html')


def contact(request):
    return render(request, 'catalog/contact.html')


def feedback(request):
    if request.method == 'POST':
        feedback_form = FeedbackForm(data=request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
            messages.success(request, 'Thank you! Your feedback has successfully been received')
    else:
        feedback_form = FeedbackForm()
    return render(request, 'catalog/feedback.html', {'feedback_form': feedback_form})





