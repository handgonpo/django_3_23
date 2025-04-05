from django.shortcuts import render

def Gallery(request):
    return render(request, 'gallery/gallery.html') # 127.0.0.1:8000/gallery
