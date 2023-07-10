from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone

from blog.forms import PostForm, CommentForm
from blog.models import Post, Category, Comment


def index(request):
    #최신글 3개 보내기
    new_post = Post.objects.order_by('-pub_date')[0:3]

    post_list = Post.objects.all()
    # 게시글 총 개수
    total_post = len(post_list)

    categories = Category.objects.all()

    context = {
        'new_post': new_post,
        'total_post': total_post,
        'categories': categories
    }
    return render(request, 'blog/index.html', context)

# 포스트 목록
def post_list(request):
    post_list = Post.objects.order_by('-pub_date') # 포스트 전체 검색
    categories = Category.objects.all() #카테고리 전체 검색

    #게시글 총 개수
    total_post = len(post_list)

    #검색 처리
    kw = request.GET.get('kw', '')  #입력폼의 넘어온 키워드
    if kw:
        post_list = post_list.filter(
            Q(title__icontains=kw) |   #제목 검색
            Q(content__icontains=kw) | #내용 검색
            Q(author__username__icontains=kw) #글쓴이 검색
        ).distinct()

    # 페이지 처리
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 5)  # 페이당 포스트 개수 - 5
    page_obj = paginator.get_page(page)

    context = {
        'post_list': page_obj,
        'categories': categories,
        'total_post': total_post,
        'kw': kw
    }
    return render(request, 'blog/post_list.html', context)

# 상세 페이지
def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    categories = Category.objects.all()  # 카테고리 전체 검색

    post_list = Post.objects.all()
    # 게시글 총 개수
    total_post = len(post_list)

    context = {
        'post': post,
        'categories': categories,
        'total_post': total_post
    }
    return render(request, 'blog/detail.html', context)

# 글쓰기
@login_required(login_url='common:login')
def post_create(request):
    categories = Category.objects.all()  #전테 카테고리 가져옴
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES) #(일반속성, 파일)
        if form.is_valid(): #유효하다면
            post = form.save(commit=False)
            post.pub_date = timezone.now()  # 현재 시간
            post.author = request.user  #로그인한 사람이 글쓴이임
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()  #비어있는 폼
    context = {'form': form, 'categories': categories}
    return render(request, 'blog/post_form.html', context)

# 카테고리별 페이지 처리 메서드
def category_page(request, slug):
    current_category = Category.objects.get(slug=slug) #현재 카테고리 검색
    post_list = Post.objects.filter(category=current_category) # 현 카테고리의 포스트들
    post_list = post_list.order_by('-pub_date')  #날짜순 내림차순
    categories = Category.objects.all() #전체 카테고리

    all_post_list = Post.objects.all()  # 전체 게시글 목록
    total_post = len(all_post_list)     # 게시글 총 개수

    # 검색 처리
    kw = request.GET.get('kw', '')  # 입력폼의 넘어온 키워드
    if kw:
        post_list = post_list.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw)  # 글쓴이 검색
        ).distinct()


    # 페이지 처리
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 5)  # 페이당 포스트 개수 - 5
    page_obj = paginator.get_page(page)

    context = {
        'current_category': current_category,
        'post_list': page_obj,
        'categories': categories,
        'total_post': total_post
    }
    return render(request, 'blog/post_list.html', context)

@login_required(login_url='common:login')
def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)  #삭제할 포스트
    post.delete()
    return redirect('blog:post_list')

# 댓글 등록
@login_required(login_url='common:login')
def comment_create(request, post_id):
    post = Post.objects.get(id=post_id)   # 댓글 쓰기위한 포스트 1개 가져옴
    if request.method == "POST":
        form = CommentForm(request.POST)  # 입력된 댓글 가져옴
        if form.is_valid():
            comment = form.save(commit=False)  #가저장(content)
            comment.author = request.user     #로그인한 글쓴이
            comment.pub_date = timezone.now()  # 작성일
            comment.post = post
            form.save()    #실제 저장 - db에 저장
    return redirect('blog:detail', post_id=post_id)

# 댓글 삭제
@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    # 삭제할 댓글 1개 가져오기
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('blog:detail', post_id=comment.post.id)

# 댓글 수정
@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    # 수정할 댓글 1개 가져오기
    comment = Comment.objects.get(id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment) # 수정한 내용 가져옴
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()  #수정한 날짜 및 시간
            comment.save()
            return redirect('blog:detail', post_id=comment.post_id)

    else:
        form = CommentForm(instance=comment)  #댓글에 입력된 내용
    context = {'form': form}
    return render(request, 'blog/comment_form.html', context)




