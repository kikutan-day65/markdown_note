import django_filters
from django.db.models import Q

from .models import Article


class ArticleFilter(django_filters.FilterSet):
    ORDER_CHOICES = [
        ("-created_at", "Latest"),
        ("created_at", "Oldest"),
    ]
    ordering = django_filters.OrderingFilter(
        choices=ORDER_CHOICES,
        label="Sort by",
        empty_label=None,
    )

    search = django_filters.CharFilter(method="filter_search", lookup_expr="icontains")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value)
            | Q(content__icontains=value)
            | Q(user__username__icontains=value)
        )

    class Meta:
        model = Article
        fields = []
