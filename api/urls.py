from django.urls import path, include

from rest_framework import routers

from api import views
from api.views import auth, charge, admin

router = routers.DefaultRouter()
router.register('categories', views.ProductCategoryViewSet, basename='category')
router.register('products', views.ProductViewSet, basename='product')
router.register('patterns', views.PatternViewSet, basename='pattern')
router.register('papers', views.PaperViewSet, basename='paper')
router.register('projects', views.ProjectViewSet, basename='project')
router.register('orders', views.OrderViewSet, basename='order')
router.register('designs', views.DesignViewSet, basename='design')
router.register('shipping_options', views.ShippingOptionViewSet, basename='shipping_option')
router.register('addresses', views.AddressViewSet, basename='address')
router.register('cards', charge.CardViewSet, basename='card')
router.register('faq_categories', views.FaqCategoryViewSet, basename='faq_category')
router.register('faq_headings', views.FaqHeadingViewSet, basename='faq_heading')
# router.register('faq_items', views.FaqItemViewSet, basename='faq_item')
# router.register(r'pieces', views.PieceViewSet, basename='piece')
# router.register(r'parts', views.PartViewSet, basename='part')
# router.register(r'program_pieces', views.ProgramPieceViewSet, basename='program_piece')
# router.register(r'players', views.PlayerViewSet, basename='player')
# router.register(r'instruments', views.InstrumentViewSet, basename='instrument')

admin_router = routers.DefaultRouter()
admin_router.register('orders', admin.OrderViewSet, basename='order')

urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    path('me/', auth.MeView.as_view(), name='me'),
    path('register/', auth.RegisterView.as_view(), name='register'),
    path('register/confirm/', auth.RegisterConfirmView.as_view(), name='register-confirm'),
    # path('password_reset/check/', views.PasswordResetTokenCheckView.as_view(), name='password-reset-check-token'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('charge/', charge.StripeChargeView.as_view(), name='charge'),
    path('tax_rate/<str:postal_code>/', views.TaxRateView.as_view(), name='tax-rate'),

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
    path('admin/', include(admin_router.urls)),
]

