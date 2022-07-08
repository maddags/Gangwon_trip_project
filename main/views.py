from django.shortcuts import redirect, render
from .models import TripNews, NewsSummery
import pandas as pd
import mlflow
import warnings

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
    word_dict = pd.read_csv("./data/word_list.csv")
    cnt_review = list(df['리뷰수'][:7])
    names = list(df['장소'][:7])
    cnt_word = list(df2['빈도수'][:7])
    words = list(df2['단어'][:7])
    word_dict = list(word_dict["장소"])
    word_dict = word_dict
    return render(request, 'post.html',
                  {'cnt_review': cnt_review, 'names' : names, 'cnt_word' : cnt_word, 'words' : words,"word_dict" : word_dict
                  })




# 예측하기
def prediction(request):
    place_list = pd.read_csv("../data/Gangwon_place_list.csv", encoding ="utf-8-sig")
    user = pd.read_csv("../data/user_answer_form.csv")
    if request.method == 'POST':
        selected_place =  request.POST.getlist("loc")
        print(selected_place)
        for place in selected_place:
            if place in user.columns:
                user.at[0,place] = 1

    if __name__ == '__main__':
        warnings.filterwarnings("ignore")
        logged_model = 'runs:/e47700ff63224201a8473eb7fc3380f5/best_estimator'

        loaded_model = mlflow.pyfunc.load_model(logged_model)
        test_x = pd.read_csv("../data/example_user1.csv")
        pred = loaded_model.predict(test_x)
        
        predict_places = []
        for loc in pred:
            predict_places.append(place_list.iloc[loc,:])
    
    return render(request,"recommend.html",{"predict_places" : predict_places})