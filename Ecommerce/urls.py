from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Product / home app
    path('', include('product.urls')),

    # Account / auth app
    path('account/', include('account.urls')),

    # ✅ Cart app
    path('cart/', include('cart.urls')),
]

# 👇 This serves media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)