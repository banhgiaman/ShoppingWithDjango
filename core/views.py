from django.shortcuts import render
from django.views import View
from product.models import Image, Product, Comment
from user.models import CustomerUser
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import validations
import matplotlib.pyplot as plt
import numpy as np
import mpld3
import pandas as pd
from .preprocess import VietnameseProcess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN


def IndexView(request):
    context ={'title': "Trang chủ"}
    products = Product.objects.all()[:]
    for product in products:
        if product.discount:
            product.actual_price = int(product.price - product.price * product.discount / 100)
    context['products'] = products
    return render(request, 'homepage/index.html', context)


def vectorize_comments(cmts):
    cmts_preprocess = []
    for cmt in cmts:
        sentence = VietnameseProcess(cmt)
        sentence.progress()
        cmts_preprocess.append(sentence.sentence)
    cmts_vector = TfidfVectorizer().fit_transform(cmts_preprocess)
    return cmts_vector


def plot_all_product(request):
    if request.user.is_superuser:
        cmts = Comment.objects.all()
        products = Product.objects.all()
        cmts_product = []
        for cmt in cmts:
            cmts_product.append({'cmt': cmt.comment, 'product': cmt.product.title})

        df = pd.DataFrame(cmts_product)
        vector = vectorize_comments(df.cmt)

        # reduce dimensions
        X = PCA(n_components=2).fit_transform(vector.toarray())

        # GMM alg
        gmm = GaussianMixture(n_components=2, random_state=0).fit_predict(X)

        X0_gmm = X[gmm == 0, :]
        X1_gmm = X[gmm == 1, :]
        cmt0 = []
        cmt1 = []
        for idx, item in enumerate(cmts_product):
            if gmm[idx] == 0:
                cmt0.append('<p><h5>Bình luận: '+cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx]['product'] + '</h3>')
            else:
                cmt1.append('<p><h5>Bình luận: '+cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx]['product'] + '</h3>')

        fig, ax = plt.subplots()
        scatter = ax.scatter(X0_gmm[:, 0],
                             X0_gmm[:, 1],
                             c=['#243B0B']*len(X0_gmm),
                             alpha=0.3,
                             cmap=plt.cm.jet)

        scatter2 = ax.scatter(X1_gmm[:, 0],
                             X1_gmm[:, 1],
                             c=['#B40404']*len(X1_gmm),
                              marker='^',
                             alpha=0.3,
                             cmap=plt.cm.jet)

        ax.grid(color='white', linestyle='solid')
        ax.set_title("Kết quả thu được từ thuật toán GMM", size=20)
        tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=cmt0)
        tooltip2 = mpld3.plugins.PointHTMLTooltip(scatter2, labels=cmt1)
        mpld3.plugins.connect(fig, tooltip)
        mpld3.plugins.connect(fig, tooltip2)
        html_fig_gmm = mpld3.fig_to_html(fig, template_type='general')

        # K-means clustering alg
        kmeans = KMeans(n_clusters=2, random_state=0).fit_predict(vector)
        X0_kmeans = X[kmeans == 0, :]
        X1_kmeans = X[kmeans == 1, :]
        cmt0 = []
        cmt1 = []
        for idx, item in enumerate(cmts_product):
            if kmeans[idx] == 0:
                cmt0.append('<p><h5>Bình luận: '+cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx]['product'] + '</h3>')
            else:
                cmt1.append('<p><h5>Bình luận: '+cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx]['product'] + '</h3>')

        fig, ax = plt.subplots()
        scatter = ax.scatter(X0_kmeans[:, 0],
                             X0_kmeans[:, 1],
                             c=['#243B0B'] * len(X0_kmeans),
                             alpha=0.3,
                             cmap=plt.cm.jet)

        scatter2 = ax.scatter(X1_kmeans[:, 0],
                              X1_kmeans[:, 1],
                              c=['#B40404'] * len(X1_kmeans),
                              marker='^',
                              alpha=0.3,
                              cmap=plt.cm.jet)

        ax.grid(color='white', linestyle='solid')
        ax.set_title("Kết quả thu được từ thuật toán K-Means Clustering", size=20)
        tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=cmt0)
        tooltip2 = mpld3.plugins.PointHTMLTooltip(scatter2, labels=cmt1)
        mpld3.plugins.connect(fig, tooltip)
        mpld3.plugins.connect(fig, tooltip2)
        html_fig_kmeans = mpld3.fig_to_html(fig, template_type='general')

        # MiniBatch K-means clustering alg
        minikmeans = MiniBatchKMeans(n_clusters=2, random_state=0).fit_predict(vector)
        X0_minikmeans = X[minikmeans == 0, :]
        X1_minikmeans = X[minikmeans == 1, :]
        cmt0 = []
        cmt1 = []
        for idx, item in enumerate(cmts_product):
            if minikmeans[idx] == 0:
                cmt0.append('<p><h5>Bình luận: '+cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx]['product'] + '</h3>')
            else:
                cmt1.append('<p><h5>Bình luận: '+cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx]['product'] + '</h3>')

        fig, ax = plt.subplots()
        scatter = ax.scatter(X0_minikmeans[:, 0],
                             X0_minikmeans[:, 1],
                             c=['#243B0B'] * len(X0_minikmeans),
                             alpha=0.3,
                             cmap=plt.cm.jet)

        scatter2 = ax.scatter(X1_minikmeans[:, 0],
                              X1_minikmeans[:, 1],
                              c=['#B40404'] * len(X1_minikmeans),
                              marker='^',
                              alpha=0.3,
                              cmap=plt.cm.jet)

        ax.grid(color='white', linestyle='solid')
        ax.set_title("Kết quả thu được từ thuật toán Mini-Batch K-Means Clustering", size=20)
        tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=cmt0)
        tooltip2 = mpld3.plugins.PointHTMLTooltip(scatter2, labels=cmt1)
        mpld3.plugins.connect(fig, tooltip)
        mpld3.plugins.connect(fig, tooltip2)
        html_fig_minikmeans = mpld3.fig_to_html(fig, template_type='general')

        # DBSCAN alg
        db = DBSCAN(eps=1.2, min_samples=30).fit_predict(vector)
        X0_db = X[db == 0, :]
        X1_db = X[db == -1, :]
        cmt0 = []
        cmt1 = []
        for idx, item in enumerate(cmts_product):
            if db[idx] == 0:
                cmt0.append(
                    '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                        'product'] + '</h3>')
            else:
                cmt1.append(
                    '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                        'product'] + '</h3>')

        fig, ax = plt.subplots()
        scatter = ax.scatter(X0_db[:, 0],
                             X0_db[:, 1],
                             c=['#243B0B'] * len(X0_db),
                             alpha=0.3,
                             cmap=plt.cm.jet)

        scatter2 = ax.scatter(X1_db[:, 0],
                              X1_db[:, 1],
                              c=['#B40404'] * len(X1_db),
                              marker='^',
                              alpha=0.3,
                              cmap=plt.cm.jet)

        ax.grid(color='white', linestyle='solid')
        ax.set_title("Kết quả thu được từ thuật toán DBSCAN", size=20)
        tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=cmt0)
        tooltip2 = mpld3.plugins.PointHTMLTooltip(scatter2, labels=cmt1)
        mpld3.plugins.connect(fig, tooltip)
        mpld3.plugins.connect(fig, tooltip2)

        html_fig_db = mpld3.fig_to_html(fig, template_type='general')
        return render(request, 'homepage/statistic.html',
                      {'title': 'Thống kê', 'products': products, 'div_figure_gmm': html_fig_gmm, 'div_figure_kmeans': html_fig_kmeans,
                       'div_figure_minikmeans': html_fig_minikmeans, 'div_figure_db': html_fig_db})

    else:
        return render(request, 'homepage/statistic.html', {'title': 'Thống kê'})


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


def plot_product(request):
    if request.user.is_superuser and request.method == 'POST':
        product_id = int(request.POST['dropdown'])
        cmts = Comment.objects.all()
        products = Product.objects.all()
        cmts_product = []
        for cmt in cmts:
            cmts_product.append({'cmt': cmt.comment, 'product': cmt.product.title, 'product_id': cmt.product.id})

        df = pd.DataFrame(cmts_product)
        vector = vectorize_comments(df.cmt)

        # reduce dimensions
        X = PCA(n_components=2).fit_transform(vector.toarray())

        # GMM alg
        gmm = GaussianMixture(n_components=2, random_state=0).fit_predict(X)

        X0_gmm = []
        X1_gmm = []
        cmt0 = []
        cmt1 = []
        for idx, item in enumerate(cmts_product):
            if cmts_product[idx]['product_id'] == product_id:
                if gmm[idx] == 0:
                    X0_gmm.append(X[idx])
                    cmt0.append(
                        '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                            'product'] + '</h3>')
                else:
                    X1_gmm.append(X[idx])
                    cmt1.append(
                        '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                            'product'] + '</h3>')
        X0_gmm = np.array(X0_gmm)
        X1_gmm = np.array(X1_gmm)

        fig, ax = plt.subplots()
        if len(X0_gmm) > 0:
            scatter = ax.scatter(X0_gmm[:, 0],
                                 X0_gmm[:, 1],
                                 c=['#243B0B'] * len(X0_gmm),
                                 alpha=0.3,
                                 cmap=plt.cm.jet)
            tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=cmt0)
            mpld3.plugins.connect(fig, tooltip)

        if len(X1_gmm) > 0:
            scatter2 = ax.scatter(X1_gmm[:, 0],
                                  X1_gmm[:, 1],
                                  c=['#B40404'] * len(X1_gmm),
                                  marker='^',
                                  alpha=0.3,
                                  cmap=plt.cm.jet)
            tooltip2 = mpld3.plugins.PointHTMLTooltip(scatter2, labels=cmt1)
            mpld3.plugins.connect(fig, tooltip2)

        ax.grid(color='white', linestyle='solid')
        ax.set_title("Kết quả thu được từ thuật toán GMM", size=20)


        html_fig_gmm = mpld3.fig_to_html(fig, template_type='general')

        # K-means clustering alg
        kmeans = KMeans(n_clusters=2, random_state=0).fit_predict(vector)
        X0_kmeans = []
        X1_kmeans = []
        cmt0 = []
        cmt1 = []
        for idx, item in enumerate(cmts_product):
            if cmts_product[idx]['product_id'] == product_id:
                if kmeans[idx] == 0:
                    X0_kmeans.append(X[idx])
                    cmt0.append(
                        '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                            'product'] + '</h3>')
                else:
                    X1_kmeans.append(X[idx])
                    cmt1.append(
                        '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                            'product'] + '</h3>')

        X0_kmeans = np.array(X0_kmeans)
        X1_kmeans = np.array(X1_kmeans)
        fig, ax = plt.subplots()

        if len(X0_kmeans) > 0:
            scatter = ax.scatter(X0_kmeans[:, 0],
                                 X0_kmeans[:, 1],
                                 c=['#243B0B'] * len(X0_kmeans),
                                 alpha=0.3,
                                 cmap=plt.cm.jet)
            tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=cmt0)
            mpld3.plugins.connect(fig, tooltip)

        if len(X1_kmeans) > 0:
            scatter2 = ax.scatter(X1_kmeans[:, 0],
                                  X1_kmeans[:, 1],
                                  c=['#B40404'] * len(X1_kmeans),
                                  marker='^',
                                  alpha=0.3,
                                  cmap=plt.cm.jet)
            tooltip2 = mpld3.plugins.PointHTMLTooltip(scatter2, labels=cmt1)
            mpld3.plugins.connect(fig, tooltip2)

        ax.grid(color='white', linestyle='solid')
        ax.set_title("Kết quả thu được từ thuật toán K-Means Clustering", size=20)

        html_fig_kmeans = mpld3.fig_to_html(fig, template_type='general')

        # MiniBatch K-means clustering alg
        minikmeans = MiniBatchKMeans(n_clusters=2, random_state=0).fit_predict(vector)
        X0_minikmeans = []
        X1_minikmeans = []
        cmt0 = []
        cmt1 = []
        for idx, item in enumerate(cmts_product):
            if cmts_product[idx]['product_id'] == product_id:
                if minikmeans[idx] == 0:
                    X0_minikmeans.append(X[idx])
                    cmt0.append(
                        '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                            'product'] + '</h3>')
                else:
                    X1_minikmeans.append(X[idx])
                    cmt1.append(
                        '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                            'product'] + '</h3>')

        X0_minikmeans = np.array(X0_minikmeans)
        X1_minikmeans = np.array(X1_minikmeans)

        fig, ax = plt.subplots()
        if len(X0_minikmeans) > 0:
            scatter = ax.scatter(X0_minikmeans[:, 0],
                                 X0_minikmeans[:, 1],
                                 c=['#243B0B'] * len(X0_minikmeans),
                                 alpha=0.3,
                                 cmap=plt.cm.jet)
            tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=cmt0)
            mpld3.plugins.connect(fig, tooltip)

        if len(X1_minikmeans) > 0:
            scatter2 = ax.scatter(X1_minikmeans[:, 0],
                                  X1_minikmeans[:, 1],
                                  c=['#B40404'] * len(X1_minikmeans),
                                  marker='^',
                                  alpha=0.3,
                                  cmap=plt.cm.jet)
            tooltip2 = mpld3.plugins.PointHTMLTooltip(scatter2, labels=cmt1)
            mpld3.plugins.connect(fig, tooltip2)

        ax.grid(color='white', linestyle='solid')
        ax.set_title("Kết quả thu được từ thuật toán Mini-Batch K-Means Clustering", size=20)

        html_fig_minikmeans = mpld3.fig_to_html(fig, template_type='general')

        ax.grid(color='white', linestyle='solid')
        ax.set_title("Kết quả thu được từ thuật toán Mini-Batch K-Means Clustering", size=20)

        # DBSCAN alg
        db = DBSCAN(eps=1.2, min_samples=30).fit_predict(vector)
        X0_db = []
        X1_db = []
        cmt0 = []
        cmt1 = []
        for idx, item in enumerate(cmts_product):
            if cmts_product[idx]['product_id'] == product_id:
                if db[idx] == 0:
                    X0_db.append(X[idx])
                    cmt0.append(
                        '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                            'product'] + '</h3>')
                else:
                    X1_db.append(X[idx])
                    cmt1.append(
                        '<p><h5>Bình luận: ' + cmts_product[idx]['cmt'] + '</h3><p><h5>Sản phẩm: ' + cmts_product[idx][
                            'product'] + '</h3>')

        X0_db = np.array(X0_db)
        X1_db = np.array(X1_db)
        fig, ax = plt.subplots()

        if len(X0_db) > 0:
            scatter = ax.scatter(X0_db[:, 0],
                                 X0_db[:, 1],
                                 c=['#243B0B'] * len(X0_db),
                                 alpha=0.3,
                                 cmap=plt.cm.jet)
            tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=cmt0)
            mpld3.plugins.connect(fig, tooltip)

        if len(X1_db) > 0:
            scatter2 = ax.scatter(X1_db[:, 0],
                                  X1_db[:, 1],
                                  c=['#B40404'] * len(X1_db),
                                  marker='^',
                                  alpha=0.3,
                                  cmap=plt.cm.jet)
            tooltip2 = mpld3.plugins.PointHTMLTooltip(scatter2, labels=cmt1)

            mpld3.plugins.connect(fig, tooltip2)

        ax.grid(color='white', linestyle='solid')
        ax.set_title("Kết quả thu được từ thuật toán DBSCAN", size=20)

        html_fig_db = mpld3.fig_to_html(fig, template_type='general')


        return render(request, 'homepage/statistic_with_product.html',
                      {'title': 'Thống kê', 'products': products, 'div_figure_gmm': html_fig_gmm, 'div_figure_kmeans': html_fig_kmeans,
                       'div_figure_minikmeans': html_fig_minikmeans, 'div_figure_db': html_fig_db})


    else:
        return render(request, 'homepage/statistic.html', {'title': 'Thống kê'})