from django.db.models import Count, Q 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.shortcuts import render, get_object_or_404, redirect, reverse
from posts.models import Post, Author, PostView 
from marketing.models import SignUp
from posts.forms import CommentForm, PostCreateForm


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)  |   Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset' : queryset,
    }
    return render(request, 'search_results.html', context)



# def get_category_count():
#     queryset = Post.objects.values('categories__title').annotate(Count('categories'))
#     return queryset

def index(request):
    featured = Post.objects.filter(featured = True)
    # latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST["email"]
        new_signup = SignUp()
        new_signup.email = email
        new_signup.save()
    context={
        'object_list' : featured,
        # 'latest' : latest, 
        }    
    return render(request, 'index.html', context)


def blog(request):
    # category_count = get_category_count()
    # most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all() 
    paginator = Paginator(post_list, 4) # Paginator() accepts 2 args post_list and no's of page to show
    page_request_var = 'page'  # localhost:8000/?page=1
    page = request.GET.get(page_request_var) # request.GET gets the querystring
    try:
        paginated_queryset = paginator.page(page) # results comes according to querystring 
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1) # If querystring is not an integer then it will return 1st page
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages) # if querystring is empty then will return all pages

    context = {
        'queryset':paginated_queryset,
        # 'most_recent':most_recent,
        'page_request_var':page_request_var,
        # 'category_count':category_count,
    }
    return render(request, 'blog.html', context)

def post(request, id):
    # category_count = get_category_count()
    # most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)
        
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post 
            form.save()
            return redirect(reverse("post_detail", kwargs={'id': post.pk}))
    context = {
        'form':form,
        'post':post,
        # 'most_recent':most_recent,
        # 'category_count':category_count, 
    }
    return render(request, 'post.html', context)


def post_create(request):
    title = "Create"
    form = PostCreateForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post_detail", kwargs={
                'id' : form.instance.id
                }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


def post_update(request, id):
    title = "Update"
    post = get_object_or_404(Post, id=id)
    form = PostCreateForm(
                request.POST or None, 
                request.FILES or None, 
                instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post_detail", kwargs={
                'id' : form.instance.id
                }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post_list"))

    

def contact(request):
    return render(request, "contact.html")
     