class MyPagination:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context.get("page_obj")

        if page_obj:
            current = page_obj.number
            total = page_obj.paginator.num_pages
            window = 10

            if total <= window:
                page_range = range(1, total + 1)
            elif current <= 6:
                page_range = range(1, window + 1)  # 最初は 1-10 を表示
            elif current > total - 5:
                page_range = range(total - window + 1, total + 1)  # 最後は末尾固定
            else:
                page_range = range(current - 5, current + 5)  # 真ん中は常に10件表示

            context["custom_page_range"] = page_range

        return context
