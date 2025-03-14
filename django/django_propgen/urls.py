"""django_propgen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from pprint import pprint as pp


from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
import proposal


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="home.html"),
        {# 'pdfs': ['main.pdf'],
        'producedmedia': proposal.models.Setting.get_default('dirs', 'producedmedia'),
         })
]

from proposal.urls import router, vrouters
from proposal.urls import urlpatterns as proposal_urlpatterns

# print(router.urls)
urlpatterns += router.urls
for vr in vrouters:
    urlpatterns += vr.urls

urlpatterns += proposal_urlpatterns
# pp(urlpatterns)

    
# Markdown URLs:
import markdownx

urlpatterns += [
     url(r'^markdownx/', include('markdownx.urls')),
    ]

# Serve uploaded media files:

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
