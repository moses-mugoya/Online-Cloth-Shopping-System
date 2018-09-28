from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment, Balance
from orders.models import OrderDetails, Order
from .forms import PaymentForm, BalanceForm, EditBalanceForm
from decimal import Decimal


@login_required
def payment_process(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']

            try:
                payment = Payment.objects.get(code__iexact=code, active=True)
                if payment:
                    payment.active = False
                    payment.user = request.user
                    payment.save()
                    return render(request, 'payment/payment_done.html')
            except:
                messages.error(request, "Error! please make sure you enter the correct transaction code then try again")

    else:
        form = PaymentForm()
    return render(request, 'payment/payment.html', {'form': form})


@login_required
def credit_balance(request):
    bal = get_object_or_404(Balance, user=request.user)
    if request.method == 'POST':
        bal_form = BalanceForm(data=request.POST or None)
        if bal_form.is_valid():
            cd = bal_form.cleaned_data
            bal.amount += cd['amount']
            bal.credit_number = cd['credit_number']
            bal.save()
            bal_form.save()
            messages.success(request, 'Your top up was successful')
        else:
            messages.error(request, 'Top up failed!')
    else:
        bal_form = BalanceForm(instance=request.user)
    return render(request, 'payment/credit.html', {'bal_form': bal_form})


@login_required
def activate_account(request):
    if request.method == 'POST':
        form = EditBalanceForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, 'Your account has successfully been activated')
        else:
            messages.error(request, 'Top up failed!')
    else:
        form = EditBalanceForm()
    return render(request, 'payment/activated.html', {'form': form})


@login_required
def confirm_payment(request, id):
    user_balance = get_object_or_404(Balance, user=request.user)
    current_order = get_object_or_404(OrderDetails, id=id)
    ordered_items = Order.objects.filter(user=request.user)
    balance = user_balance.amount
    total_cost = current_order.get_total_cost()

    if balance >= Decimal(total_cost):
        user_balance.amount = balance - total_cost
        current_order.paid = True
        current_order.save()
        user_balance.save()
        for order in ordered_items:
            order.product.stock = order.product.stock - order.quantity
            order.product.save()
            order.save()
        return render(request, 'payment/payment_done.html')

    else:
        messages.error(request, 'Insufficient funds! Please top up your account then try again')
    return render(request, 'payment/pay.html', {'current_order': current_order})




