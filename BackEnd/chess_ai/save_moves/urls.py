from .apis.save_moves_api import ChessGameLogViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'chessgamelog', ChessGameLogViewSet)
urlpatterns = router.urls