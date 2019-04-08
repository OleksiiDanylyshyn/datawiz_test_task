from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from dwapi import datawiz
import datetime


# Create your views here.

def home(request):
    return render(request, 'datawiz_test_task_app/page_home.html')


@require_POST
def user_login(request):
    email = request.POST['email']
    password = request.POST['password']
    response_data = {}
    try:
        user = User.objects.get(username=email)
        if user.check_password(password):
            user = authenticate(username=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                response_data = {'response': 'success'}
        else:
            response_data = {'response': "dismatch"}
    except User.DoesNotExist:
        response_data = {'response': "nouser"}
    return JsonResponse(response_data)


def user_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def signup(request):
    return render(request, 'registration/page_sign_up.html')


@require_POST
def user_create(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=email)
    messages.success(request, 'Congratulation')
    return redirect(signup)


def user_profile(request):
    dw = get_client(request)
    dw_client_info = dw.get_client_info()
    shops = dw.get_shops()
    return render(request, 'datawiz_test_task_app/page_user_profile.html',
                  {'dw_client_info': dw_client_info, 'shops': shops})


def get_client(request):
    email = request.user.username
    password = request.user.password
    dw = datawiz.DW()
    return dw


def key_indicators(request):
    dw = get_client(request)
    data = dict()
    date_from = datetime.date(2015, 11, 17)
    date_to = datetime.date(2015, 11, 18)
    data['date_from'] = date_from
    data['date_to'] = date_to
    products_sale_turnover = dw.get_products_sale(products=[2837229, 2837240, 'sum'], by='turnover',
                                                  date_from=date_from,
                                                  date_to=date_to)
    data['turnover'] = list(products_sale_turnover['sum'])

    turnover_dif_percent = products_sale_turnover['sum'].pct_change() * 100
    data['turnover_dif_percent'] = round(list(turnover_dif_percent)[1], 2)
    turnover_dif = products_sale_turnover['sum'].diff()
    data['turnover_dif'] = round(list(turnover_dif)[1], 2)
    products_sale_qty = dw.get_products_sale(products=[2837229, 2837240, 'sum'], by='qty',
                                             date_from=date_from,
                                             date_to=date_to)
    data['qty'] = list(products_sale_qty['sum'])
    qty_diff_percent = products_sale_qty['sum'].pct_change() * 100
    data['qty_diff_percent'] = round(list(qty_diff_percent)[1], 2)
    qty_diff = products_sale_qty['sum'].diff()
    data['qty_diff'] = round(list(qty_diff)[1], 2)
    products_sale_receipts_qty = dw.get_products_sale(products=[2837229, 2837240, 'sum'], by='receipts_qty',
                                                      date_from=date_from,
                                                      date_to=date_to)
    data['receipts_qty'] = list(products_sale_receipts_qty['sum'])
    receipts_qty_percent = products_sale_receipts_qty['sum'].pct_change() * 100
    data['receipts_qty_percent'] = round(list(receipts_qty_percent)[1], 2)
    receipts_qty_diff = products_sale_receipts_qty['sum'].diff()
    data['receipts_qty_diff'] = round(list(receipts_qty_diff)[1], 2)
    avg_receipt = list(round(products_sale_turnover['sum'] / products_sale_receipts_qty['sum'], 2))
    data['avg_receipt'] = avg_receipt
    avg_receipt_diff = round(avg_receipt[1] - avg_receipt[0], 2)
    data['avg_receipt_diff'] = avg_receipt_diff
    avg_receipt_diff_percent = avg_receipt[1] * 100 / avg_receipt[0]
    data['avg_receipt_diff_percent'] = round(avg_receipt_diff_percent - 100, 2)
    return render(request, 'datawiz_test_task_app/page_key_indicators.html', {'data': data})


@require_GET
def products_increase(request):
    return render(request, 'datawiz_test_task_app/page_products_increase.html')


def get_products(request):
    dw = get_client(request)
    products_sale_turnover = dw.get_products_sale(by='turnover', date_from=datetime.date(2015, 11, 17),
                                                  date_to=datetime.date(2015, 11, 18), view_type='raw')
    products_sale_qty = dw.get_products_sale(by='qty', date_from=datetime.date(2015, 11, 17),
                                             date_to=datetime.date(2015, 11, 18), view_type='raw')
    products_diff_turnover_list = list(round(products_sale_turnover['turnover'].diff(), 2))
    products_diff_qty_list = list(round(products_sale_qty['qty'].diff(), 2))
    products_name_list = list(products_sale_turnover.name)
    data = dict()
    data['products_diff_turnover_list'] = products_diff_turnover_list
    data['products_diff_turnover_list'][0] = 0
    data['products_diff_qty_list'] = products_diff_qty_list
    data['products_diff_qty_list'][0] = 0
    data['products_name_list'] = products_name_list
    return JsonResponse(data)


def products_decrease(request):
    return render(request, 'datawiz_test_task_app/page_products_decrease.html')

