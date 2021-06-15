from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Matches, Payment, Chat, ChatListView, MatchDetail

urlpatterns = [
    path('', views.index, name="home"),
    path('signup/', views.Signup, name="Signup"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('community', views.community, name="community"),
    path('profile/', views.profile, name="profile"),
    path('qualities/', views.qualities, name="qualities"),
    path('success/', views.success, name="success"),
    path('page/', views.page, name="page"),
    path('status/', views.status, name="status"),
    path('matches/', Matches.as_view(), name="matches"),
    path('payment/<slug:slug>/', Payment.as_view(), name="payment"),
    path('policy/', views.policy, name="policy"),
    path('login/', views.loginPage, name="login"),
    path('subscription/', views.subscription, name="subs"),
    path('logout/', views.logoutuser, name="logout"),
    path('redirect/', views.redirect_page, name="redirect"),
    path('send/', views.send, name="send"),
    path('account-info/', views.account_info, name="account_info"),
    path('pass_change/', views.pass_change, name="pass_change"),
    path('close_account/', views.close_account, name="close_account"),
    path('detail/', views.profile_detail, name="detail"),
    path('settings/', views.profile_setting, name="setting"),
    path('chat/', Chat.as_view(), name="chat"),
    path('current/<slug:slug>/', ChatListView.as_view(), name="current"),
    path('match_detail/<slug:slug>/', MatchDetail.as_view(), name="match_detail"),
    path('recieve_msg/', views.recieve_msg, name="recieve"),
    path('recieve/<slug:slug>/', views.receive, name="recieve"),
    path('forget_password/', views.forget_password, name="forget_password"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)