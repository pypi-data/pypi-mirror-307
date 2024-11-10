from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets


class CrudViewSet(viewsets.GenericViewSet):
    """
    Base view class for CRUD operations.
    """

    queryset = None  # Should be defined in the child class
    serializer_class = None  # Should be defined in the child class
    custom_field_model = None  # Should be defined in the child class

    def get_serializer(self, *args, **kwargs):
        """
        Override get_serializer to pass `custom_field_model` in the context to the serializer.
        """
        kwargs["context"] = kwargs.get("context", {})
        kwargs["context"]["custom_field_model"] = self.custom_field_model  # Access from child class

        return super().get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
