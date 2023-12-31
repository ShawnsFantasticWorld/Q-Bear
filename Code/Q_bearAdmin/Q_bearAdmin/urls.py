"""
Function Name: Background interface url configuration
Function: Background interface url configuration
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from myAdmin import designView,answerView
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'admin/', admin.site.urls),
    url('^api/design',designView.opera),#Questionnaire Designer Operations
    url('^api/answer',answerView.opera),#Questionnaire Respondent Actions
    url(r'home/', TemplateView.as_view(template_name="index.html")),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'index/', TemplateView.as_view(template_name="index.html")),
    url(r'login/', TemplateView.as_view(template_name="index.html")),
    url(r'register/', TemplateView.as_view(template_name="index.html")),
    url(r'resetpass/', TemplateView.as_view(template_name="index.html")),
    url(r'^display.*$', TemplateView.as_view(template_name="index.html")),
    url(r'thankyou/', TemplateView.as_view(template_name="index.html")),

]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
