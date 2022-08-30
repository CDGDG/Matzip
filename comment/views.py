import re
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView
from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from .forms import CommentForm

from comment.models import Comment, CommentImage
from matzip.models import Restaurant


def commentlist(request, pk, page=1):
    data = {}

    orderby = request.GET.get("orderby", "-datetime") or "-datetime"

    comments = Comment.objects.filter(matzip=pk).order_by(orderby)
    
    paginator = Paginator(comments, 5)

    object_count = paginator.count

    page_obj = paginator.get_page(page)

    pagelist = paginator.get_elided_page_range(page, on_each_side=3)

    data['html_list'] = render_to_string("comment/includes/partial_comment_list.html", {'comments': page_obj, 'pagelist': pagelist, 'object_count': object_count, "orderby": orderby}, request=request)

    return JsonResponse(data)


class CommentCreate(View):

    def post(self, request: HttpRequest, pk):
        data = {}
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        user = request.user
        
        comment = Comment(user=user, text=text, rating=rating, matzip=Restaurant.objects.get(pk=pk))
        comment.save()

        for image in request.POST.getlist("commentimages"):
            CommentImage(comment=comment, image=image).save()

        data['success'] = True
        return JsonResponse(data)

class CommentUpdate(View):
    def get(self, request: HttpRequest, pk):
        data = {}
        comment = get_object_or_404(Comment, pk=pk)

        # 로그인 확인
        if not request.user.is_authenticated:
            data['login_ok'] = False
            data['next'] = "/matzip/list/"
            return JsonResponse(data)

        data['login_ok'] = True
        data['html_form'] = render_to_string("comment/includes/partial_comment_update.html", {"comment": comment}, request=request)

        return JsonResponse(data)

    def post(self, request: HttpRequest, pk):
        data = {}
        comment = get_object_or_404(Comment, pk=pk)

        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        return JsonResponse(data)

class CommentDelete(View):
    def post(self, request: HttpRequest, pk):
        data ={}
        comment = get_object_or_404(Comment, pk=pk)

        comment.delete()
        data['success'] = True
        return JsonResponse(data)


