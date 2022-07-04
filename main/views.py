from django.shortcuts import render
from .models import TripNews, NewsSummery

# Create your views here.


def about(request):
    datas = TripNews.objects.all().order_by("created_at")
    # urls = NewsUrl.objects.all()
    summ = NewsSummery.objects.all()
    return render(request, 'about.html', {'news' : datas, 'summ': summ})


def index(request):
    return render(request, 'index.html')
def post(request):
    return render(request, 'post.html')
def contact(request):
    return render(request, 'contact.html')


