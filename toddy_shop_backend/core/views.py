from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shared.permissions import IsAdminOrReadOnly
from shared.responses import APIResponse

from .models import (
    District,
    Facility,
    FoodCategory,
    FoodItem,
    HygieneTag,
    LicenseType,
    MediaType,
    Place,
    RatingType,
    ReviewCategory,
    ShopCategory,
    Status,
    UserRole,
)
from .serializers import (
    DistrictSerializer,
    FacilitySerializer,
    FoodCategorySerializer,
    FoodItemSerializer,
    HygieneTagSerializer,
    LicenseTypeSerializer,
    MediaTypeSerializer,
    PlaceSerializer,
    RatingTypeSerializer,
    RegisterSerializer,
    ReviewCategorySerializer,
    ShopCategorySerializer,
    StatusSerializer,
    UserRoleSerializer,
    UserSerializer,
)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return APIResponse(
            data=UserSerializer(user).data,
            message="Registration successful.",
            status=201,
        )


class LoginView(TokenObtainPairView):
    """Returns JWT access + refresh tokens."""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0])
        return APIResponse(data=serializer.validated_data, message="Login successful.")


class TokenRefreshAPIView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0])
        return APIResponse(data=serializer.validated_data, message="Token refreshed.")


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return APIResponse(data=serializer.data, message="Profile retrieved.")


# ---------------------------------------------------------------------------
# Lookup ViewSet base
# ---------------------------------------------------------------------------


class LookupViewSet(viewsets.ModelViewSet):
    """Read-only for everyone; full CRUD for admins."""

    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return APIResponse(data=serializer.data, message="Data retrieved successfully.")

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return APIResponse(data=serializer.data, message="Data retrieved successfully.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse(data=serializer.data, message="Created successfully.", status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse(data=serializer.data, message="Updated successfully.")

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return APIResponse(data=None, message="Deleted successfully.")


# ---------------------------------------------------------------------------
# Lookup ViewSets
# ---------------------------------------------------------------------------


class UserRoleViewSet(LookupViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer


class StatusViewSet(LookupViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class DistrictViewSet(LookupViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class PlaceViewSet(LookupViewSet):
    queryset = Place.objects.select_related("district").all()
    serializer_class = PlaceSerializer
    filterset_fields = ["district"]


class ShopCategoryViewSet(LookupViewSet):
    queryset = ShopCategory.objects.all()
    serializer_class = ShopCategorySerializer


class FoodCategoryViewSet(LookupViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer


class FoodItemViewSet(LookupViewSet):
    queryset = FoodItem.objects.select_related("food_category").all()
    serializer_class = FoodItemSerializer
    filterset_fields = ["food_category"]


class FacilityViewSet(LookupViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class HygieneTagViewSet(LookupViewSet):
    queryset = HygieneTag.objects.all()
    serializer_class = HygieneTagSerializer


class RatingTypeViewSet(LookupViewSet):
    queryset = RatingType.objects.all()
    serializer_class = RatingTypeSerializer


class MediaTypeViewSet(LookupViewSet):
    queryset = MediaType.objects.all()
    serializer_class = MediaTypeSerializer


class LicenseTypeViewSet(LookupViewSet):
    queryset = LicenseType.objects.all()
    serializer_class = LicenseTypeSerializer


class ReviewCategoryViewSet(LookupViewSet):
    queryset = ReviewCategory.objects.all()
    serializer_class = ReviewCategorySerializer
