from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register('categories', views.ProductCategoryViewSet, basename='category')
router.register('products', views.ProductViewSet, basename='product')
router.register('projects', views.ProjectViewSet, basename='project')
# router.register(r'pieces', views.PieceViewSet, basename='piece')
# router.register(r'parts', views.PartViewSet, basename='part')
# router.register(r'program_pieces', views.ProgramPieceViewSet, basename='program_piece')
# router.register(r'players', views.PlayerViewSet, basename='player')
# router.register(r'instruments', views.InstrumentViewSet, basename='instrument')

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.MeView.as_view(), name='me'),
    # url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # url(r'^register/confirm/$', views.RegisterConfirmView.as_view(), name='register-confirm'),
    # url(r'^skill_levels/$', views.SkillLevelsView.as_view(), name='skill-levels'),
    #
    # url(r'^randomize/(?P<program_id>[0-9]+)/$', views.RandomizeView.as_view(), name='randomize'),
    # url(r'^assignments/(?P<program_id>[0-9]+)/$', views.AssignmentsView.as_view(), name='assignments'),
    # url(r'^library/$', views.SearchLibraryView.as_view(), name='search-library'),
    # url(r'^settings/$', views.SaveSettingsView.as_view(), name='save-settings'),
    # url(r'^settings/password/$', views.UpdatePasswordView.as_view(), name='update-password'),
    #
    # url(r'^password_reset/check/', views.PasswordResetTokenCheckView.as_view(), name='password-reset-check-token'),
    # url(r'^password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    #
    path('', include(router.urls)),
]

