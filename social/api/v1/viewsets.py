from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from social.models import Post, Like
from social.api.v1.serializers import PostSerializer, LikeSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]


class LikeViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        like_instance = Like.objects.filter(user=request.user,
                                            post=serializer.validated_data['post']
                                            )
        if like_instance:
            return Response({'response': 'You are already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'response': "Post liked"}, status=status.HTTP_200_OK)


class UnlikeViewSet(mixins.DestroyModelMixin, GenericViewSet):
    queryset = Like.objects.all()

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        del_instance = Like.objects.filter(id=instance.id, user=user).first()
        if del_instance:
            del_instance.delete()
            return Response({"response": "Post Unliked"}, status=status.HTTP_200_OK)
        return Response({'response': "No matching item"}, status=status.HTTP_204_NO_CONTENT)
