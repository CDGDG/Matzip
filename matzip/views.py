import base64
from typing import Optional
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View, DetailView, DeleteView
from django.http import HttpRequest, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.db.models.functions import TruncDay
import requests, json, io
from geopy.geocoders import Nominatim

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 한글 폰트 사용을 위해서 세팅
# from matplotlib import font_manager, rc
# font_path = "C:/Windows/Fonts/NGULIM.TTF"
# font = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font)

from config import settings

from matzip.models import Restaurant
from matzip.forms import RestaurantForm
from comment.models import Comment

def index(request):
    return render(request, 'index.html', )

class MatzipList(ListView):
    model = Restaurant
    template_name = "matzip.html"
    paginate_by = 9

    def get_queryset(self):
        queryset =  Restaurant.objects.filter(address__startswith=self.request.GET.get("address", ""), type__startswith=self.request.GET.get("type", "")).annotate(avg_rate=Avg('comment__rating'))

        # 정렬
        order_by = self.request.GET.get("orderby", "name") or "name"
        queryset = queryset.order_by(order_by)

        return queryset
    

    def get_context_data(self, **kwargs):
        context = super(MatzipList, self).get_context_data()
        
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=3)
        context['pagelist'] = pagelist

        context['currentPosition'] = self.request.GET.get("address", "") or ""

        context['regions'] = regions

        context['orderby'] = self.request.GET.get("orderby", "name") or "name"

        context['type'] = self.request.GET.get("type", "") or ""

        return context

class MatzipCreate(View):

    def get(self, request: HttpRequest):
        data = {}

        # 로그인 확인
        if not request.user.is_authenticated:
            data['login_ok'] = False
            data['next'] = "/matzip/list/"
            return JsonResponse(data)

        form = RestaurantForm()

        data['login_ok'] = True
        data['html_form'] = render_to_string('includes/partial_matzip_create.html', {"form": form}, request=request)
        return JsonResponse(data)

    def post(self, request: HttpRequest):
        data = {}

        form = RestaurantForm(request.POST)
        if form.is_valid():
            matzip = form.save(commit=False)
            matzip.user = request.user
            matzip.save()
            data['form_is_valid'] = True
            data['next'] = f"/matzip/detail/{matzip.pk}/"
        else:
            data['form_is_valid'] = False
            data['html_form'] = render_to_string("includes/partial_matzip_create.html", {'form', form}, request=request)

        return JsonResponse(data)

class MatzipDetail(DetailView):
    model = Restaurant
    template_name = "matzip_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.filter(matzip=context['object'].id).order_by("-id")

        paginator = Paginator(comments, 5)

        object_count = paginator.count

        page_obj = paginator.get_page(1)

        pagelist = paginator.get_elided_page_range(1, on_each_side=3)


        context["comments"] = page_obj
        context['pagelist'] = pagelist
        context['object_count'] = object_count

        # 별점 평균
        avg_rate = comments.aggregate(Avg("rating"))['rating__avg']
        context['avg_rate'] = f"{avg_rate or 0 : 0.2f}"
        context['star_position'] = 300 - (300 * (avg_rate/5)) if avg_rate else 0

        # 파이차트
        pie_ratio = comments.values('rating').annotate(total=Count("rating")).order_by("-rating")
        plt.pie([p['total'] for p in pie_ratio], labels = ["★"*p['rating'] for p in pie_ratio], autopct="%.1f%%", counterclock=False,
                startangle=90, explode=[0.05 for _ in range(len(pie_ratio))], rotatelabels=True, textprops={"color":"gold","weight":1}
                )
        io_buffer = io.BytesIO()
        plt.savefig(io_buffer, format="png", dpi=200, transparent=True)
        pie_image = u'data:img/png;base64,'+base64.b64encode(io_buffer.getvalue()).decode('utf-8')
        context['pie_image'] = pie_image
        io_buffer.close()
        plt.close()


        # 날짜별 별점 평균
        day_rate = comments.annotate(day=TruncDay("datetime")).values("day").annotate(avg=Avg("rating")).order_by("-day")
        plt.plot([d['day'] for d in day_rate], [d['avg'] for d in day_rate], color="white")
        plt.xlabel("날짜", color="white", fontsize="large")
        plt.ylabel("별점", color="white", fontsize="large")
        plt.yticks([i for i in range(1,6)], fontsize="large")
        plt.tight_layout()
        ax = plt.gca()
        ax.axes.xaxis.set_ticks([])
        ax.tick_params(color="white", labelcolor="white", direction="in")
        for spine in ax.spines.values():
            spine.set_edgecolor("white")

        day_buffer = io.BytesIO()
        plt.savefig(day_buffer, format="png", dpi=500, transparent=True)
        day_image = u'data:img/png;base64,'+base64.b64encode(day_buffer.getvalue()).decode('utf-8')
        context['day_image'] = day_image
        day_buffer.close()
        plt.close()

        return context
    

class MatzipUpdate(View):

    def get(self, request: HttpRequest, pk):
        data = {}
        matzip = get_object_or_404(Restaurant, pk=pk)

        # 로그인 확인
        if not request.user.is_authenticated:
            data['login_ok'] = False
            data['next'] = "/matzip/list/"
            return JsonResponse(data)

        form = RestaurantForm(instance=matzip)
        form.id = matzip.id
        form.addr = matzip.address

        data['login_ok'] = True
        data['html_form'] = render_to_string('includes/partial_matzip_update.html', {"form": form}, request=request)
        return JsonResponse(data)

    def post(self, request: HttpRequest, pk):
        data = {}

        matzip = get_object_or_404(Restaurant, pk=pk)
        form = RestaurantForm(request.POST, instance=matzip)

        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            data['next'] = f"/matzip/detail/{pk}/"
        else:
            data['form_is_valid'] = False
            data['html_form'] = render_to_string('includes/partial_matzip_update.html', {"form": form}, request = request)

        return JsonResponse(data)

class MatzipDelete(DeleteView):
    model = Restaurant
    success_url = reverse_lazy('Matzip:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class MatzipNear(View):
    def get(self, request: HttpRequest, address):
        context = {}
        nearlist = Restaurant.objects.filter(address__startswith=address).values()
        context['nears'] = list(nearlist)
        return JsonResponse(context)
        


regions = {
    '서울특별시' : ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
    '인천광역시' : ["계양구", "남동구", "동구", "미추홀구", "부평구", "서구", "연수구", "중구"],
    '부산광역시' : ["강서구", "금정구", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
    '대전광역시' : ["대덕구", "동구", "서구", "유성구", "중구"],
    '대구광역시' : ["남구", "달서구", "달서군", "동구", "북구", "서구", "수성구", "중구"],
    '울산광역시' : ["남구", "동구", "북구", "중구", "울주군"],
    '광주광역시' : ["광산구", "남구", "동구", "북구", "서구"],
    '제주특별자치도' : ["서귀포시", "제주시"],
    '세종특별자치시' : ["세종특별자치시"],
    '경기도' : ["고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "여주시", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시", "가평군", "양평군", "연천군"],
    '강원도' : ["강릉시", "동해시", "삼척시", "속초시", "원주시", "춘천시", "태백시", "고성군", "양구군", "양양군", "영월군", "인제군", "정선군", "철원군", "평창군", "홍천군", "화천군", "횡성군"],
    '충청북도' : ["제천시", "청주시", "충주시", "괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "증평군", "진천군"],
    '충청남도' : ["계룡시", "공주시", "논산시", "당진시", "보령시", "서산시", "아산시", "천안시", "금산군", "부여군", "서천군", "예산군", "청양군", "태안군", "홍성군"],
    '경상북도' : ["경산시", "경주시", "구미시", "김천시", "문경시", "상주시", "안동시", "영주시", "영천시", "포항시", "고령군", "군위군", "봉화군", "성주군", "영덕군", "영양군", "예천군", "울릉군", "울진군", "의성군", "청도군", "청송군", "칠곡군"],
    '경상남도' : ["거제시", "김해시", "밀양시", "사천시", "양산시", "진주시", "창원시", "통영시", "거창군", "고성군", "남해군", "산청군", "의령군", "창녕군", "하동군", "함안군", "함양군", "합천군"],
    '전라북도' : ["군산시", "김제시", "남원시", "익산시", "전주시", "정읍시", "고창군", "무주군", "부안군", "순창군", "완주군", "임실군", "장수군", "진안군"],
    '전라남도' : ["광양시", "나주시", "목포시", "순천시", "여수시", "강진군", "고흥군", "곡성군", "구례군", "담양군", "무안군", "보성군", "신안군", "영광군", "영암군", "완도군", "장성군", "장흥군", "진도군", "함평군", "해남군", "화순군"],
}
