from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from port.views import Main  # 메인 페이지 뷰

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view(), name='main'),  # 메인 페이지 직접 연결 port.views.py의 Main.as_view()를 사용
    path('user/', include(('user.urls', 'user'), namespace='user')),  # 네임스페이스 등록
    path('port/', include(('port.urls', 'port'), namespace='port')),  # 네임스페이스 등록
    path('interaction/', include(('interaction.urls', 'interaction'), namespace='interaction')),  #interaction도 네임스페이스 등록//앱이 여러개일때 추천
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
