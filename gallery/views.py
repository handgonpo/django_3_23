from django.shortcuts import render

def Gallery_Main(request):
    return render(request, 'base.html') # 127.0.0.1:8000/gallery
