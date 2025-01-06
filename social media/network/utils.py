from django.core.paginator import Paginator

def paginate_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return paginator, page
    