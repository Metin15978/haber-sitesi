from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from news.forms import CommentForm
from . models import *
from login.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q ,Count
from .forms import NewsForm
# Create your views here.

def home(request):
    siyasi_haber=Categories.objects.get(category_name="Siyasi")
    ekonomik_haber=Categories.objects.get(category_name="Ekonomi")
    teknoloji_haber=Categories.objects.get(category_name="Teknoloji")
    dünya_haber=Categories.objects.get(category_name="Dünya")
    
    haber=News.objects.filter(is_delete=False,category=siyasi_haber).order_by('-created_at')[:1]
    haber_2=News.objects.filter(is_delete=False,category=ekonomik_haber).order_by('-created_at')[:1]
    haber_3=News.objects.filter(is_delete=False,category=teknoloji_haber).order_by('-created_at')[:1]
    haber_4=News.objects.filter(is_delete=False,category=dünya_haber).order_by('-created_at')[:1]


    latest_posts=News.objects.filter(is_delete=False).order_by('-created_at')[:4]

    latest_from_siyaset=News.objects.filter(is_delete=False,category=siyasi_haber).order_by('-created_at')[:1]
    latest_from_siyaset_others=News.objects.filter(is_delete=False,category=siyasi_haber).order_by('-created_at')[1:5]

    latest_from_ekonomi=News.objects.filter(is_delete=False,category=ekonomik_haber)[:4]

    latest_from_teknoloji=News.objects.filter(is_delete=False,category=teknoloji_haber).order_by('-created_at')[:1]
    latest_from_teknoloji_others=News.objects.filter(is_delete=False,category=teknoloji_haber).order_by('-created_at')[1:6]

    latest_from_dünya=News.objects.filter(is_delete=False,category=dünya_haber).order_by('-created_at')[:1]
    latest_from_dünya_others=News.objects.filter(is_delete=False,category=dünya_haber).order_by('-created_at')[1:6]

    slider=News.objects.filter(is_delete=False).order_by('-created_at')[:5]
    
    most_read = News.objects.order_by('-view_count')[:10]
    most_commented = News.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:10]
    
  
    context={
        'haber':haber,
        'haber_2':haber_2,
        'haber_3':haber_3,
        'haber_4':haber_4,
        'latest_posts':latest_posts,
        'latest_posts_siyaset':latest_from_siyaset,
        'latest_from_siyaset_others':latest_from_siyaset_others,
        'latest_from_ekonomi':latest_from_ekonomi,
        'latest_from_teknoloji':latest_from_teknoloji,
        'latest_from_teknoloji_others':latest_from_teknoloji_others,
        'latest_from_dünya':latest_from_dünya,
        'latest_from_dünya_others':latest_from_dünya_others,
        'slider':slider,
        'most_read':most_read,
        'most_commented': most_commented,
    }


    return render(request, 'news/home.html',context)


def authors(request):
    authors_list = Author.objects.filter(is_delete=False)
    paginator = Paginator(authors_list, 1)  # Sayfa başına 2 yazar

    page = request.GET.get('page')
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        # Eğer sayfa numarası bir tam sayı değilse, ilk sayfayı getir
        authors = paginator.page(1)
    except EmptyPage:
        # Eğer sayfa numarası sınırların dışında ise, son sayfayı getir
        authors = paginator.page(paginator.num_pages)

    context = {
        'authors': authors,
    }
    return render(request, 'news/authors.html', context)


def blog(request):
    query = request.GET.get('q')
    latest_posts1 = News.objects.filter(is_delete=False)

    if query:
        latest_posts1 = latest_posts1.filter(
            Q(news_title__contains=query)  
            
        )

    latest_posts2 = latest_posts1.order_by('-created_at')
    paginator=Paginator(latest_posts2,2)

    page=request.GET.get('page')

    try:
        blog = paginator.page(page)
    except PageNotAnInteger:
        blog = paginator.page(1)
    except EmptyPage:
        blog = paginator.page(paginator.num_pages)

    context = {
        'latest_posts1': blog,
        'query': query,
        'blog':blog,
    }

    return render(request, 'news/blog.html',context)


def categories(request, category_name):   
    category = get_object_or_404(Categories, category_name=category_name)
    category_news = News.objects.filter(category=category, is_delete=False)
    paginator = Paginator(category_news, 2)  # 1 haberlik bir sayfalamaya ayır

    page = request.GET.get('page')
    try:
        category_news = paginator.page(page)
    except PageNotAnInteger:
        # Eğer sayfa numarası bir tam sayı değilse, ilk sayfayı getir
        category_news = paginator.page(1)
    except EmptyPage:
        # Eğer sayfa numarası sınırların dışında ise, son sayfayı getir
        category_news = paginator.page(paginator.num_pages)
    
    context = {
        'category_name': category_name,
        'category_news': category_news,
    }

    return render(request, 'news/categories.html', context)






def details(request, newsSlug):
    news = get_object_or_404(News, slug=newsSlug, is_delete=False)
    user = request.user
    
    # Tüm yorumları al, en yeniden en eskiye sırala
    comments = news.comments.all().order_by('-created_at')
    comment_count = comments.count()
    
    # Yorumlar için sayfalama oluştur, her sayfada 2 yorum göster
    paginator = Paginator(comments, 2)
    page = request.GET.get('page')
    
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # Eğer sayfa numarası bir tam sayı değilse, ilk sayfayı getir
        comments = paginator.page(1)
    except EmptyPage:
        # Eğer sayfa numarası sınırların dışında ise, son sayfayı getir
        comments = paginator.page(paginator.num_pages)
    
    # Diğer haberler
    latest_posts = News.objects.filter(is_delete=False).order_by('-created_at')[:5]
    
    # Yorum ekleme formu
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = request.user
            comment.save()
            return redirect('details', newsSlug=newsSlug)
    else:
        form = CommentForm()
    
    # Haber görüntülenmesi
    if user.is_authenticated:
        if not NewsView.objects.filter(news=news, user=user).exists():
            NewsView.objects.create(news=news, user=user)
            news.view_count += 1
            news.save()
 
    context = {
        'comment_count':comment_count,
        'news': news,
        'comments': comments,
        'form': form,
        'latest_posts': latest_posts,
      
    }
    
    return render(request, 'news/details.html', context)



def profile(request, slug):
    author = Author.objects.get(slug=slug)
    author_news_list = News.objects.filter(user=author.user, is_delete=False).order_by('-created_at')
    paginator = Paginator(author_news_list, 1)  # 3 haberlik bir sayfalamaya ayır

    page = request.GET.get('page')
    try:
        author_news = paginator.page(page)
    except PageNotAnInteger:
        # Eğer sayfa numarası bir tam sayı değilse, ilk sayfayı getir
        author_news = paginator.page(1)
    except EmptyPage:
        # Eğer sayfa numarası sınırların dışında ise, son sayfayı getir
        author_news = paginator.page(paginator.num_pages)

    context = {
        'author': author,
        'author_news': author_news,
    }

    return render(request, 'news/profile.html', context)


from django.db.models import Sum

def dashboard(request):
    # Giriş yapmış kullanıcının haberlerini çek
    if request.user.is_authenticated:
        dashboard = News.objects.filter(user=request.user)
    else:
        dashboard = []

    # Her haber için yorum sayısını ve toplam görüntülenme sayısını hesapla
    news_with_comment_counts = []
    total_view_count = 0  # Toplam görüntülenme sayısını tutmak için
    total_comment_count = Comment.objects.filter(news__in=dashboard).count()
    for news in dashboard:
        comment_count = news.comments.count()
        view_count = news.view_count  # Varsayılan olarak mevcut görüntülenme sayısını alalım
        total_view_count += view_count  # Toplam görüntülenme sayısını güncelleyelim

        news_with_comment_counts.append({
            'news': news,
            'comment_count': comment_count,
            'view_count': view_count,
        })
    
    context = {
        'dashboard_with_comment_counts': news_with_comment_counts,
        'total_view_count': total_view_count,
        'total_comment_count':total_comment_count,
    }
    return render(request, 'news/dashboard.html', context)


def news_upload(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.user = request.user  # Assuming you have user authentication
            news.save()
            return redirect('blog')  # Redirect to news detail page
    else:
        form = NewsForm()
    return render(request, 'news/news_upload.html', {'form': form})




