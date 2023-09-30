# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Diary2
from django.http import Http404
from django import forms
from .forms import DiaryForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

# 다이어리 목록을 보여주는 뷰
def diary_list(request):

    search_query = request.GET.get('search')
    # 검색어가 주어진 경우, 해당 검색어를 포함한 일기를 필터링합니다.
    if search_query:
        diary_list = Diary2.objects.filter(
            Q(content1__icontains=search_query) |
            Q(content2__icontains=search_query) |
            Q(content3__icontains=search_query) |
            Q(todo1__icontains=search_query) |
            Q(todo2__icontains=search_query) |
            Q(todo3__icontains=search_query)
        ).order_by('-date')
    else:
        # 검색어가 주어지지 않은 경우, 모든 일기를 날짜 기준으로 정렬하여 보여줍니다.
        diary_list = Diary2.objects.all().order_by('-date')

    all_diaries = Diary2.objects.all().order_by('-date')
    paginator = Paginator(all_diaries, 3)  # 페이지당 3개의 'contents'를 보여줍니다.
        
    # 페이지당 보여줄 항목 수를 정의합니다.
    items_per_page = 3
    # Paginator를 사용하여 항목을 페이지별로 나눕니다.
    paginator = Paginator(all_diaries, items_per_page)
    # 현재 페이지 번호를 가져오거나 기본값으로 1을 사용합니다.
    page_number = request.GET.get('page', 1)
    # 현재 페이지의 항목을 가져옵니다.
    diaries = paginator.get_page(page_number)
    
    context = {'diary_list': diaries}
    return render(request, 'myapp/diary_list.html', context)

    
# 새로운 폼 생성 
def create(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            form.save()  # 다이어리 저장

            # 저장 후 홈 페이지로 리디렉션
            return redirect('myapp:diary_list')

    else:
        form = DiaryForm()  # GET 요청 시 폼에 새로운 ID 초기값 설정

    diaries = Diary2.objects.all().order_by('-date')  # 새로운 content가 맨 위에 오도록 정렬
    context = {'form': form, 'diaries': diaries}
    return render(request, 'myapp/create.html', context)

def diary_update(request, diary_id):
    # diary_id에 해당하는 다이어리 객체 가져오기
    diary = get_object_or_404(Diary2, pk=diary_id)

    if request.method == 'POST':
        # POST 요청인 경우, 폼에서 제출된 데이터로 다이어리 업데이트
        form = DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            form.save()
            # 업데이트가 완료되면 다이어리 상세 페이지로 리디렉션
            return redirect('myapp:diary_list')
    else:
        # GET 요청인 경우, 다이어리 수정 폼 보여주기
        form = DiaryForm(instance=diary)

    return render(request, 'myapp/diary_update.html', {'form': form, 'diary': diary})

def diary_delete(request, diary_id):
    # diary_id에 해당하는 다이어리 객체 가져오기
    diary1 = get_object_or_404(Diary2, pk=diary_id)

    if request.method == 'POST':
        # POST 요청인 경우, 다이어리 삭제
        diary1.delete()
        # 삭제가 완료되면 다이어리 목록 페이지로 리디렉션
        messages.success(request, '다이어리가 삭제되었습니다.')  # 삭제 성공 메시지


        # 삭제가 완료되면 JSON 응답을 반환하여 페이지 리디렉션을 처리합니다.
        return redirect('myapp:diary_list')

    context = {'diary': diary1}
    return render(request, 'myapp/diary_delete.html', context)

# 다이어리 항목을 페이지별로 가져오기 위해 Django의 Paginator를 사용
from django.core.paginator import Paginator
def entries(request):
    # 데이터베이스에서 모든 다이어리 항목을 가져오고, 최신 항목이 위로 오도록 정렬
    all_entries = Diary2.objects.all().order_by('-created_at')
    # 페이지당 보여줄 항목 수를 정의 예: 3개씩 보여줍니다.
    items_per_page = 3
    # Paginator를 사용하여 항목을 페이지별로 나눕니다.
    paginator = Paginator(all_entries, items_per_page)
    # 현재 페이지 번호를 가져오거나 기본값으로 1을 사용합니다.
    page_number = request.GET.get('page', 1)
    # 현재 페이지의 항목을 가져옵니다.
    entries = paginator.get_page(page_number)
    # 컨텍스트에 entries 변수를 추가하여 템플릿으로 전달
    context = {'entries': entries}

    return render(request, 'myapp/entries.html', context)


from django.urls import reverse
def some_view(request):
    # 'diary_list' 뷰를 호출하는 URL을 생성합니다.
    diary_list_url = reverse('diary_list')
    
    # diary_list_url에 GET 요청을 보내고 결과를 확인합니다.
    response = self.client.get(diary_list_url)
    
    # response를 확인하거나 필요에 따라 다른 작업을 수행합니다.
    if response.status_code == 200:
        # 정상적인 응답을 받았을 경우
        return render(request, 'template.html', {'diary_list': response.context['diary_list']})
    else:
        # 오류 처리
        return redirect('error_page')
    
# 선택한 날짜에 해당하는 content를 JSON 형식으로 응답
def get_content(request):
    selected_date = request.GET.get('date')  # 선택한 날짜 가져오기

    # 여기서 선택한 날짜에 해당하는 content를 조회하는 로직을 작성합니다.
    # 이 예시에서는 Diary 모델을 사용하여 content를 조회합니다.
    try:
        diary = Diary2.objects.get(date=selected_date)
        content = {
            'content1': diary.content1,
            'content2': diary.content2,
            'content3': diary.content3,
            'todo1': diary.todo1,
            'todo2': diary.todo2,
            'todo3': diary.todo3,
        }
        return JsonResponse({'content': content})
    except Diary2.DoesNotExist:
        return JsonResponse({'content': 'No content found for the selected date.'})