from django.shortcuts import render

def page_not_found(request, exception):
    return render(request, 'page/404.html', status=404)

def page_error(request):
    return render(request, 'page/500.html', status=500)