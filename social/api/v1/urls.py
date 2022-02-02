from django.urls import path, include
from social.api.v1.viewsets import PostViewSet, LikeViewSet, UnlikeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("post", PostViewSet, basename="post")
router.register("like", LikeViewSet, basename="like")
router.register("unlike", UnlikeViewSet, basename="unlike")

urlpatterns = [
    path("", include(router.urls))
]
