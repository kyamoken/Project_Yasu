from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, CreateView, TemplateView, DeleteView, View, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from .models import Post, CustomUser, Like, Comment, CommentLike, Announcement
from .forms import PostForm, CustomUserCreationForm, ContactForm, CommentForm, AnnouncementForm


class HomePageView(TemplateView):
    template_name = 'Online_15/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        paginator = Paginator(posts, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            posts_list = list(page_obj.object_list.values('id', 'title', 'content', 'Image'))
            return JsonResponse({'posts': posts_list, 'has_next': page_obj.has_next()})

        context['page_obj'] = page_obj
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'Online_15/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # オブジェクトを取得して設定
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = self.object
            new_comment.user = request.user
            new_comment.save()
            return redirect('post_detail', pk=self.object.pk)
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'Online_15/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user




class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'Online_15/post_edit.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        messages.success(self.request, '投稿が完了しました。')
        return response

    def get_success_url(self):
        return reverse('home')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_posts = Post.objects.filter(user=self.request.user)
        paginator = Paginator(user_posts, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class CustomLogoutView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'ログアウトしました。')
        return redirect('home')


class LikePostView(LoginRequiredMixin, View):
    @method_decorator(require_POST)
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        post.likes = Like.objects.filter(post=post).count()
        post.save()

        return JsonResponse({'liked': liked, 'likes_count': post.likes})


class LikeCommentView(LoginRequiredMixin, View):
    @method_decorator(require_POST)
    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({'liked': liked, 'likes_count': comment.total_likes()})


class ContactView(FormView):
    template_name = 'Online_15/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        send_mail(
            f'お問い合わせ: {name}',
            message,
            email,
            ['kamoken0531@gmail.com'],
        )

        messages.success(self.request, '送信完了！')
        return super().form_valid(form)


class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'Online_15/announcement_list.html'
    context_object_name = 'announcements'
    ordering = ['-created_at']

class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'Online_15/announcement_form.html'
    success_url = reverse_lazy('announcement_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser