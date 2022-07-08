from django.shortcuts import render
from .models import TripNews, NewsSummery
import pandas as pd

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


def chart_data(request):
    df = pd.read_csv("./data/place_review_cnt_data.csv")
    df2 = pd.read_csv('./data/word_cnt_info.csv')
    cnt_review = list(df['리뷰수'][:7])
    names = list(df['장소'][:7])
    cnt_word = list(df2['빈도수'][:7])
    words = list(df2['단어'][:7])
    return render(request, 'post.html',
                  {'cnt_review': cnt_review, 'names' : names, 'cnt_word' : cnt_word, 'words' : words})


