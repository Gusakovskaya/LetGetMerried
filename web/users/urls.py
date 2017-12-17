from rest_framework.routers import SimpleRouter
from users import views

router = SimpleRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet, base_name='users')

urlpatterns = router.urls