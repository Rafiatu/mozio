from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from locations.models import Polygon, Coordinate
from locations.serializers import PolygonSerializer, CoordinatesSerializer


class LocationsView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PolygonSerializer

    def list(self, request):
        try:
            data = Polygon.objects.filter(provider=request.user)
            serializer = self.serializer_class(data, many=True)
            return Response(
                {"message": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        polygon = get_object_or_404(Polygon, id=pk)
        serializer = self.serializer_class(polygon)
        return Response(
            {"message": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            coordinates_list = serializer.validated_data["coordinates"]
            del serializer.validated_data["coordinates"]
            polygon = Polygon.objects.create(
                provider=request.user, **serializer.validated_data
            )
            # coords = CoordinatesSerializer(data=coordinates_list, many=True)
            # coords.is_valid(raise_exception=True)
            # coords.save()
            # print(coords)
            # polygon.coordinates.set(coords)
            for points in coordinates_list:
                coordinates = Coordinate.objects.get_or_create(**points)
                polygon.coordinates.add(coordinates)
            return Response(
                {
                    "message": f"successully created new geojson Polygon {serializer.validated_data.get('name')}",
                    "data": self.serializer_class(polygon).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, pk):
        polygon = get_object_or_404(Polygon, id=pk)
        if request.user != polygon.provider:
            return Response(
                {"error": "You are not authorized to update this Polygon."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(polygon, data=request.data, partial=True)
        if serializer.is_valid():
            if "coordinates" in serializer.validated_data:
                coordinates_list = serializer.validated_data["coordinates"]
                del serializer.validated_data["coordinates"]
                for points in coordinates_list:
                    coordinates = Coordinate.objects.get_or_create(**points)
                    polygon.coordinates.add(coordinates)
            serializer.save()
            return Response(
                {
                    "message": f"successully updated geojson Polygon {serializer.data.get('name')}",
                    "data": serializer.data,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk):
        polygon = get_object_or_404(Polygon, id=pk)
        if request.user != polygon.provider:
            return Response(
                {"error": "You are not authorized to delete this Polygon."},
                status=status.HTTP_403_FORBIDDEN,
            )
        polygon.delete()
        return Response(
            {"Response": "Task Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["POST"])
    def coordinates(self, request, *args, **kwargs):
        serializer = CoordinatesSerializer(data=request.data)
        if serializer.is_valid():
            coordinates = get_object_or_404(
                Coordinate,
                latitude=serializer.validated_data["latitude"],
                longitude=serializer.validated_data["longitude"],
            )
            try:
                polygons = Polygon.objects.filter(coordinates=coordinates)
                polygons_data = self.serializer_class(polygons, many=True)
                return Response(
                    {"message": "success", "data": polygons_data.data},
                    status=status.HTTP_200_OK,
                )
            except Exception as error:
                return Response(
                    {"error": str(error)}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
