from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from .views import PostDetailView,AnnouncementListView, AnnouncementCreateView, PostCreateView, HomePageView, SignUpView, PostDeleteView, ProfileView, LikePostView, \
    ContactView, LikeCommentView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'), # ここでhome.htmlを表示する TOPページ
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'), # ここでpost_detail.htmlを表示する 投稿詳細
    path('post/new/', PostCreateView.as_view(), name='post_new'), # ここでpost_edit.htmlを表示する 新規投稿
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'), # ここでpost_confirm_delete.htmlを表示する 投稿削除
    path('login/', auth_views.LoginView.as_view(), name='login'), # ここでlogin.htmlを表示する ログイン
    path('signup/', SignUpView.as_view(), name='signup'), # ここでsignup.htmlを表示する 新規登録
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), # ここでログアウト
    path('accounts/', include('Online_15.accounts.urls')), # ここでaccounts/urls.pyを読み込む
    path('profile/', ProfileView.as_view(), name='profile'), # ここでprofile.htmlを表示する プロフィール
    path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('contact/', ContactView.as_view(), name='contact'), # ここでcontact.htmlを表示する お問い合わせ
    path('like_comment/<int:comment_id>/', LikeCommentView.as_view(), name='like_comment'), # ここでlike_comment.htmlを表示する コメントいいね
    path('announcements/', AnnouncementListView.as_view(), name='announcement_list'), # ここでannouncement_list.htmlを表示する お知らせ一覧
    #path('announcements/new/', AnnouncementCreateView.as_view(), name='announcement_create'),  ここでannouncement_form.htmlを表示する お知らせ作成
]



# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)