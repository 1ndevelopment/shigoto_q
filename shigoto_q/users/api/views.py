from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.http import Http404
from djstripe.models import Plan, Product
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import ProductSerializer, UserSerializer

User = get_user_model()


class ProductView(APIView):
    permission_classes = []

    def get_objects(self, *args, **kwargs):
        try:
            return (
                Product.objects.prefetch_related("plan_set")
                .order_by("plan__amount")
                .filter(plan__interval="month")
            )
        except Product.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        products = self.get_objects()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
