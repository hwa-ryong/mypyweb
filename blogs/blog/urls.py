from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'), # 목록
    path('<int:post_id>/', views.detail, name='detail'), #상세 페이지
    path('post/create/', views.post_create, name='post_create'),
    path('category/<str:slug>/', views.category_page,
         name='category_page'), # 카테고리별 페이지
    path('post/delete/<int:post_id>/', views.post_delete,
         name='post_delete'),  # 포스트 삭제
    path('comment/create/<int:post_id>', views.comment_create,
         name='comment_create'), #댓글 등록
    path('comment/delete/<int:comment_id>', views.comment_delete,
         name='comment_delete'), #댓글 삭제
    path('comment/modify/<int:comment_id>', views.comment_modify,
         name='comment_modify'), #댓글 수정
]