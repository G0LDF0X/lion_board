from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Item
from django.http import HttpResponse
from django.urls import reverse_lazy
# Create your views here.

class ItemLV(ListView):
    # ListView는 기본 세팅
    # - template : 앱이름/모델명(소문자)_list.html
    # - context : object_list
    model = Item
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['name'] = 'Tiger'
        return context

class ItemDV(DetailView):
    # DetailView는 기본 세팅
    # - template : 앱이름/모델명(소문자)_detail.html
    # - context : object
    # pk를 통해서 대상 데이터를 가져옵니다!!
    # url에서 pk를 가져오는 내용이 정의되어 있어야 합니다!!
    model = Item

class ItemCV(CreateView):
    model = Item
    fields = ['title', 'content']
    success_url = reverse_lazy('spring:index')
    # - template : 앱이름/모델명(소문자)_form.html

from .forms import CommentForm
def content_comment(request, pk):
    # 해당 item pk를 가진 대상에 추가적으로 comment를 저장
    item = Item.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.item = item
            comment.save()
    elif request.method == 'GET':
        form = CommentForm()
    return render(request, 'board/item_detail.html', {'object': item, 'form': form})

class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('spring:index')

def itemLV(request):
    # 모델에서 데이터들 가져오고
    object = Item.objects.all()
    name = "Lion"
    # context에 담고
    context = {
        'object_list' : object,
        'name': name,
    }
    # 템플릿에 결합해서 페이지 반환
    return render(request=request, template_name='board/item_list.html', context=context)

def test(request):
    return HttpResponse("요청 잘 받았어")

def test1(request, pk):
    return HttpResponse(f"test1 pk: {pk} 이야")