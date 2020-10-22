from django.shortcuts import render, HttpResponseRedirect, HttpResponse, reverse
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import View
from .models import User, Post
from .forms import LoginForm, PostCreateForm
from django.contrib.auth import authenticate, login
from .service import get_user_posts,\
     get_user_following_objects, get_user_followers_objects,\
     save_post, follow_unfollow
from .permissions import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.dates import DateMixin
from django.contrib import messages
from django.views.generic.edit import CreateView


def redirect_blog(request):
    return redirect('login', permanent=True)


class HomeView(LoginRequiredMixin, DateMixin, TemplateView):
    template_name = 'blog/home.html'
    date_field = '-creation_date'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user_id = self.request.user.id
        context['posts'] = get_user_posts(user_id)
        context['followings'] = get_user_following_objects(user_id)
        context['followers'] = get_user_followers_objects(user_id)
        context['blogers'] = User.objects.all()
        return context


class UserDetail(LoginRequiredMixin, View):
    template_name = 'blog/user_detail.html'

    def get(self, request, id):
        print(request.user.id)
        user = User.objects.get(id=id)
        return render(request, self.template_name, context={'user': user})

    def post(self, request, id):
        follower_user = User.objects.get(id=request.user.id)
        following_user = User.objects.get(id=id)
        if follow_unfollow(follower_user.id, following_user.id):
            messages.success(request, f'Your FOLLOW on user{following_user.email}')
            return HttpResponseRedirect(request.path_info)
        messages.error(request, f'Your UNFOLLOW on user{following_user.email}')
        return HttpResponseRedirect(request.path_info)


class PostCreate(CreateView):
    template_name = 'blog/post_create.html'
    form_class = PostCreateForm
    success_url = '/post_create'

    def post(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST)
        user = User.objects.get(id=request.user.id)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            post = Post(title=title, text=text, author_name=user)
            if post:
                post.save()
                messages.success(request, 'Your post was created')
                return HttpResponseRedirect(request.path_info)
            messages.error(request, 'Your post was not created')
            return HttpResponseRedirect('/post_create')
        return HttpResponse('Form is not valid')


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    pk_url_kwarg = 'id'


class LoginView(View):
    template_name = 'blog/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        print(email, password, user)
        if user:
            login(request, user)
            return HttpResponseRedirect('/home')
        return HttpResponseRedirect('/login')


class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = '/login'
