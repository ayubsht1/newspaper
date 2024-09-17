from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View, DetailView

from newspaper.forms import ContactForm
from newspaper.models import Category, Post, Tag
from django.utils import timezone
from datetime import timedelta

# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = 'aznews/home.html'
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")[:5]
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )
        context["featured_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
            ).order_by("-published_at", "-views_count")[1:4]
        
        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
            ).order_by("-published_at", "-views_count")[:7]
        
        context["recent_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:7]
        
        return context
    
class AboutView(TemplateView):
    template_name = "aznews/about.html"
   
    
class PostListView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")
    

class PostByCategoryView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            category__id=self.kwargs["category_id"],
        ).order_by("-published_at")
        return query

class PostByTagView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status="active",
            category__id=self.kwargs["tag_id"],
        ).order_by("-published_at")
        return query

from django.contrib import messages
from django.shortcuts import redirect

class ContactView(View):
    template_name = "aznews/contact.html"

    def get(self,request):
        return render(request, self.template_name)
    
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Successfully submitted your query. We will contact you soon."
            )
            return redirect("contact")  # Redirect to the same page after successful submission
        else:
            messages.error(
                request,
                "Error submitting your query. Please make sure that all fields are valid."
            )
        return render(request, self.template_name, {'form': form},)
    

class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        obj.views_count +=1
        obj.save()

        context["previous_post"]=(
            Post.objects.filter(
                published_at__isnull=False,
                status="active",
                id__lt=obj.id
            ).order_by("-id")
            .first()
        )
        context["next_post"] = (
            Post.objects.filter(
                published_at__isnull=False,
                status="active",
                id__gt=obj.id
                ).order_by("id")
                .first()
        )
        return context
    
from newspaper.forms import CommentForm

class CommentView(View):
    def post(self,request,*args,**kwargs):
        form = CommentForm(request.POST)
        post_id = request.POST["post"]
        if form.is_valid():
            form.save()
            return redirect("post-detail", post_id)
        post =Post.objects.get(pk=post_id)
        return render(
            request,
            "aznews/detail/detail.html",
            {"post":post, "form":form}
        )
    
from django.core.paginator import PageNotAnInteger, Paginator
from django.db.models import Q

class PostSearchView(View):
    template_name = "aznews/list/list.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")  # Get the query parameter safely
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
            & Q(status="active")
            & Q(published_at__isnull=False)
        ).order_by("-published_at")

        #pagination start
        page = request.GET.get("page",1)
        paginate_by = 3
        paginator = Paginator(post_list, paginate_by)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)

        #pagination end
        return render(
            request,
            self.template_name,
            {"page_obj": posts, "query": query},
        )
