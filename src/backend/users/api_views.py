from http import HTTPMethod

from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Friendship, User
from .permissions import IsAuthenticatedOrAdminForUsers
from .serializers import (
    FriendAcceptDeclineSerializer,
    FriendRequestSerializer,
    UserRetrieveSerializer,
    UserSignUpSerializer,
)
from .services import FriendRequestServices, FriendshipServices


class UserSingUpViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин вью-сет для регистрации.
    """

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (permissions.AllowAny,)


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин вью-сет для объектов 'User'.
    """

    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsAuthenticatedOrAdminForUsers,)
    lookup_field = "username"

    def get_friend_request_serializer(self, *args, **kwargs):
        serializer_class = FriendRequestSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_accept_friend_request_serializer(self, *args, **kwargs):
        serializer_class = FriendAcceptDeclineSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(
        methods=[HTTPMethod.GET],
        detail=False,
        url_path="me",
    )
    def users_own_profile(self, request):
        """Просмотр своего профиля."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=[HTTPMethod.POST, HTTPMethod.DELETE],
        detail=True,
        lookup_field="username",
        url_path="send_friend_request",
    )
    def send_friend_request(self, request, username):
        """Отправление запроса дружбы."""
        user = get_object_or_404(User, username=username)
        serializer = self.get_friend_request_serializer(data=model_to_dict(user))
        serializer.is_valid(raise_exception=True)
        if request.method == HTTPMethod.POST:
            FriendRequestServices(request).send_friend_request(user=user)
            return Response(
                {"message": f"Вы отправили запрос дружбы пользователю {username}!"},
                status=status.HTTP_201_CREATED,
            )
        if request.method == HTTPMethod.DELETE:
            FriendRequestServices(request).cancel_friend_request(user=user)
            return Response(
                {"message": f"Вы отозвали запрос дружбы к пользователю {username}!"},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(
        methods=["post"],
        detail=True,
        lookup_field="username",
        url_path="accept_friend_request",
    )
    def accept_friend_request(self, request, username):
        """Принятие запроса дружбы."""
        user = get_object_or_404(User, username=username)
        serializer = self.get_accept_friend_request_serializer(data=model_to_dict(user))
        serializer.is_valid(raise_exception=True)
        FriendRequestServices.accept_friend_request(self, user)
        return Response(
            {"message": f"Вы приняли запрос дружбы от пользователя {username}!"},
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=[HTTPMethod.DELETE],
        detail=True,
        lookup_field="username",
        url_path="decline_friend_request",
    )
    def decline_friend_request(self, request, username):
        """Отклонение запроса дружбы."""
        user = get_object_or_404(User, username=username)
        serializer = self.get_accept_friend_request_serializer(data=model_to_dict(user))
        serializer.is_valid(raise_exception=True)
        FriendRequestServices.decline_friend_request(self, user)
        return Response(
            {"message": f"Вы отклонили запрос дружбы от пользователя {username}!"},
            status=status.HTTP_201_CREATED,
        )


class FriendshipViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserRetrieveSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = "username"

    def get_queryset(self):
        """Запрос возвращающий друзей пользователя."""
        query = self.request.user.friends_list
        return query

    def destroy(self, request, *args, **kwargs):
        """Удаление из друзей."""
        user = get_object_or_404(User, username=kwargs["username"])
        get_object_or_404(
            Friendship,
            another_user=user,
            current_user=request.user,
        )
        FriendshipServices(request).remove_friend(user)
        return Response(
            {"message": f"Вы удалили пользователя {user.username} из друзей!"},
            status=status.HTTP_204_NO_CONTENT,
        )
