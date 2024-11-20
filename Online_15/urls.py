from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from .views import PostDetailView,AnnouncementListView, AnnouncementCreateView, PostCreateView, HomePageView, SignUpView, PostDeleteView, ProfileView, LikePostView, \
    ContactView, LikeCommentView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/', include('Online_15.accounts.urls')),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('like_comment/<int:comment_id>/', LikeCommentView.as_view(), name='like_comment'),
    path('announcements/', AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/new/', AnnouncementCreateView.as_view(), name='announcement_create'),
]



# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)