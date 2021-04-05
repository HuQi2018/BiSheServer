from django.shortcuts import render

nav_tag = [{"name":"动作","left":"左显示区","right":"右显示区"},{"name":"爱情","left":"左显示区","right":"右显示区"},
           {"name":"科幻","left":"左显示区","right":"右显示区"},{"name":"喜剧","left":"左显示区","right":"右显示区"},]

# userData = {"userName":"Admin","userAvatar":"a6055ac0-2e08-4612-9f4f-a8145f67727b.jpg"}
userData = ""
# Create your views here.
def index(request):
    return render(request, 'index.html', {"page":"index.html","nav_tag": nav_tag ,"userData": userData})

def register(request):
    return render(request, 'register.html', {"page":"register.html","nav_tag": nav_tag ,"userData": userData})

def category(request):
    return render(request, 'category.html', {"page":"category.html","nav_tag": nav_tag ,"userData": userData})

def search(request):
    return render(request, 'search.html', {"page":"search.html","nav_tag": nav_tag ,"userData": userData})

def movie(request):
    return render(request, 'movie.html', {"page":"movie.html","nav_tag": nav_tag ,"userData": userData})

def userInfo(request):
    return render(request, 'userInfo.html', {"page":"userInfo.html","nav_tag": nav_tag ,"userData": userData})
