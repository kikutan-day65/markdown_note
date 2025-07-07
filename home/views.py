import markdown
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from home.utils.filepath import temp_article_images_path
from home.utils.image_processing import process_article_images

from .filters import ArticleFilter
from .forms import ArticleForm
from .messages import (
    ARTICLE_CREATE_SUCCESS,
    ARTICLE_DELETE_SUCCESS,
    ARTICLE_UPDATE_SUCCESS,
)
from .models import Article, ArticleImage
from .paginations import MyPagination


class HomeView(MyPagination, FilterView):
    template_name = "home/home.html"
    model = Article
    context_object_name = "articles"
    ordering = ["-created_at"]
    paginate_by = 10
    filterset_class = ArticleFilter


class ArticleDetailView(DetailView):
    template_name = "home/article_detail.html"
    model = Article
    context_object_name = "article_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        markdown_text = self.object.content
        html_content = markdown.markdown(
            markdown_text,
            extensions=[
                "extra",
                "codehilite",
                "toc",
                "admonition",
                "smarty",
            ],
        )
        context["article_html"] = html_content
        return context


class ArticleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "home/article_form.html"
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("home:home_page")
    login_url = reverse_lazy("user:login")
    success_message = ARTICLE_CREATE_SUCCESS

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        article = form.save()
        article = process_article_images(article, user.id)
        article.modified_at = None
        article.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = False
        return context

    def form_invalid(self, form):
        for field, error in form.errors.items():
            error_message = strip_tags(error)
            messages.error(self.request, error_message)
        return super().form_invalid(form)


class ArticleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "home/article_form.html"
    model = Article
    form_class = ArticleForm
    context_object_name = "article"
    success_message = ARTICLE_UPDATE_SUCCESS
    login_url = reverse_lazy("user:login")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse("home:article_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context

    def form_valid(self, form):
        user = form.instance.user
        article = form.instance
        article = process_article_images(article, user.id)
        article.modified_at = timezone.now()
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, error in form.errors.items():
            error_message = strip_tags(error)
            messages.error(self.request, error_message)
        return super().form_invalid(form)


class ArticleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "common/delete.html"
    model = Article
    context_object_name = "article"
    success_url = reverse_lazy("home:home_page")
    success_message = ARTICLE_DELETE_SUCCESS
    login_url = reverse_lazy("user:login")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_invalid(self, form):
        for field, error in form.errors.items():
            error_message = strip_tags(error)
            messages.error(self.request, error_message)
        return super().form_invalid(form)


def upload_article_images(request):
    if request.method == "POST" and request.FILES.get("image"):
        temp_image = request.FILES["image"]
        temp_image_path = temp_article_images_path(request.user, temp_image.name)
        saved_image = default_storage.save(temp_image_path, temp_image)
        image_url = settings.MEDIA_URL + saved_image
        print(image_url)

        return JsonResponse(
            {
                "success": True,
                "url": image_url,
            }
        )

    return JsonResponse({"success": False, "error": "No image uploaded"}, status=400)
