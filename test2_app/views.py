from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import Test2NewsForm, CommentForm
from .models import Test2News, Comment
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Test2News
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
# Create your views here.

class IndexView(ListView):
    template_name = 'index.html'

    queryset = Test2News.objects.order_by('-posted_at')
    
    paginate_by = 9

class CreateNewsView(CreateView):
    
    form_class = Test2NewsForm
    
    template_name = "post_news.html"
    
    success_url = reverse_lazy('test2_app:post_done')
    
    def form_valid(self, form):
        # 本来すぐにDBへ保存してしまうが、取得して保存したいため、一旦falseに変更する
        postdata = form.save(commit=False)
        #送られてきた値のユーザーIDを取得
        postdata.user = self.request.user
        # DBへ保存
        postdata.save()
        
        return super().form_valid(form)

class PostSuccessView(TemplateView):
    
    template_name = 'post_success.html'

class CategoryView(ListView):
    
    template_name = 'index.html'
    
    paginate_by = 9
    
    def get_queryset(self):
        
        category_id = self.kwargs['category']
        
        categories = Test2News.objects.filter(
            category=category_id).order_by('-posted_at')
        
        return categories

class UserView(ListView):
    
    template_name  = 'index.html'
    
    paginate_by = 9
    
    def get_queryset(self):
        
        user_id = self.kwargs['user']
        
        user_list = Test2News.objects.filter(
            user=user_id).order_by('-posted_at')
        
        return user_list

class DetailView(DetailView):
    
    template_name = 'detail.html'
    
    model = Test2News
    

class MypageView(ListView):
    
    template_name = 'mypage.html'
    
    paginate_by = 9
    
    def get_queryset(self):
        
        queryset = Test2News.objects.filter(
            user=self.request.user).order_by('-posted_at')
        
        return queryset

class NewsDeleteView(DeleteView):
    
    model = Test2News
    
    template_name = 'news_delete.html'
    
    success_url = reverse_lazy('test2_app:mypage')
    
    def delete(self, request, *args, **kwargs):
        
        return super().delete(request, *args, **kwargs)

class NewsEditView(UpdateView):
    
    model = Test2News
    
    template_name = 'news_edit.html'
    
    form_class = Test2NewsForm
    
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context["categories"] = Test2News.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return context
    
    def get_success_url(self):
        return reverse_lazy("test2_app:index")

class CommentCreateView(CreateView):
    
    model = Comment
    
    form_class = CommentForm
    
    template_name = 'post_comment.html'
    
    def form_valid(self, form):
        # 本来すぐにDBへ保存してしまうが、取得して保存したいため、一旦falseに変更する
        postdata = form.save(commit=False)
        # URLから記事ID（pk）を取得してコメントに紐付ける
        post_id = self.kwargs['pk']
        postdata.post_id = post_id
        #送られてきた値のユーザーIDを取得
        postdata.user = self.request.user
        # DBへ保存
        postdata.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        # コメント作成後、記事の詳細ページにリダイレクト
        return reverse_lazy("test2_app:news_detail", kwargs={'pk': self.kwargs['pk']})