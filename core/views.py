from django.shortcuts import render
from django.views import View
from product.models import Image, Product, Comment
from user.models import CustomerUser
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import validations


def IndexView(request):
    context ={'title': "Trang chủ"}
    products = Product.objects.all()[:16]
    for product in products:
        if product.discount:
            product.actual_price = int(product.price - product.price * product.discount / 100)
    context['products'] = products
    return render(request, 'homepage/index.html', context)


class ContactView(View):
    def get(self, request):
        context = {'title': 'Liên hệ'}
        return render(request, 'homepage/contact.html', context)


def ProductDetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.discount:
        product.actual_price = int(product.price - product.price * product.discount / 100)
    imgs = Image.objects.filter(product=product_id)
    title = 'Chi tiết sản phẩm'
    comments = Comment.objects.filter(product=product_id, is_buyer=True)[:3]
    context = {'title': title, 'product': product, 'imgs': imgs, 'comments': comments}
    return render(request, 'homepage/product.html', context)


def ProductComments(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    title = 'Bình luận'
    comments = Comment.objects.filter(product=product_id)
    context = {'title': title, 'product': product,'comments': comments}
    return render(request, 'homepage/product_comments.html', context)


def AddComment(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comment = request.GET['comment']
    if 'is_buyer' in request.GET:
        is_buyer = True
    else:
        is_buyer = False
    Comment.objects.create(comment=comment, is_buyer=is_buyer,product=product)
    return HttpResponseRedirect(reverse('core:product', args=(product_id,)))


def Register(request):
    context = {'title': 'Đăng ký'}
    return render(request, 'homepage/register.html', context)


def Register_Success(request):
    context = {'title': 'Đăng ký'}
    username = request.POST['username']
    phone_number = request.POST['phone']
    address = request.POST['address']
    email = request.POST['email']
    password = request.POST['password']
    password_again = request.POST['password_again']
    if password == '' or password_again == '':
        context['message'] = 'Password không thể để trống'
        return render(request, 'homepage/register.html', context)
    elif password != password_again:
        context['message'] = 'Password không trùng nhau'
        return render(request, 'homepage/register.html', context)
    elif address == '':
        context['message'] = 'Địa chỉ không thể để trống'
        return render(request, 'homepage/register.html', context)
    elif validations.validatePhoneNumber(phone_number) == False:
        context['message'] = 'Số điện thoại không hợp lệ'
        return render(request, 'homepage/register.html', context)
    elif validations.validateEmail(email) == False:
        context['message'] = 'Email chưa nhập đúng'
        return render(request, 'homepage/register.html', context)

    try:
        CustomerUser.objects.create_user(username=username, email=email, password=password, phone_number=phone_number, address=address)
    except ValueError:
        context['message'] = 'Username không thể để trống'
        return render(request, 'homepage/register.html', context)
    except Exception:
        context['message'] = 'Username đã tồn tại'
        return render(request, 'homepage/register.html', context)
    context['message'] = 'Đăng ký thành công'
    return render(request, 'homepage/register.html', context)