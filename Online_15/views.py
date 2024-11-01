from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, CreateView, TemplateView, DeleteView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from .models import Post, CustomUser, Like
from .forms import PostForm, CustomUserCreationForm, ContactForm


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

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'Online_15/post_confirm_delete.html'
    success_url = reverse_lazy('home')

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
        user_posts = Post.objects.filter(user=self.request.user)  # 修正: author -> user
        paginator = Paginator(user_posts, 12)  # 1ページに12個の投稿を表示
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class CustomLogoutView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'ログアウトしました。')
        return redirect('home')  # リダイレクト先を指定

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

        # Likeの数を集計してpost.likesに保存する
        post.likes = Like.objects.filter(post=post).count()
        post.save()

        return JsonResponse({'liked': liked, 'likes_count': post.likes})

class ContactView(FormView):
    template_name = 'Online_15/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')  # ホームページにリダイレクト

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        send_mail(
            f'お問い合わせ: {name}',
            message,
            email,
            ['kamoken0531@gmail.com'],  # 受信するメールアドレスに変更
        )


        messages.success(self.request, '送信完了！')
        return super().form_valid(form)