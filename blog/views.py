from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import LogoutView
from django.views.generic import View
from .models import User, Post
from .forms import LoginForm, PostCreateForm
from django.contrib.auth import authenticate, login
from .service import get_user_posts,\
     get_user_following_objects, get_user_followers_objects,\
     save_post, follow_unfollow
from .permissions import LoginRequiredMixin
from django.shortcuts import redirect


def redirect_blog(request):
    return redirect('login', permanent=True)


class HomeView(LoginRequiredMixin, View):
    template_name = 'blog/home.html'

    def get(self, request):
        user_id = request.user.id
        posts = get_user_posts(user_id)
        followings = get_user_following_objects(user_id)
        followers = get_user_followers_objects(user_id)
        blogers = User.objects.all()
        context = {'posts': posts,
                   'followings': followings,
                   'followers': followers,
                   'blogers': blogers}
        return render(request, self.template_name, context=context)


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
            return HttpResponse('You are FOLLOW on this user')
        return HttpResponse(f'You are UNFOLLOW on {following_user.email}')


class PostCreate(LoginRequiredMixin, View):
    template_name = 'blog/post_create.html'

    def get(self, request):
        form = PostCreateForm
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = PostCreateForm(request.POST)
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        print(user)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            post = Post(title=title, text=text, author_name=user)
            if save_post(post):
                return HttpResponseRedirect('/home')
            return HttpResponseRedirect('/post_create')
        return HttpResponse('Form is not valid')


class PostDetail(LoginRequiredMixin, View):
    template_name = 'blog/post_detail.html'

    def get(self, request, id):
        post = Post.objects.get(id=id)
        return render(request, self.template_name, context={'post': post})


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
