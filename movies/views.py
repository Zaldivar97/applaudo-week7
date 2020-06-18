from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication

from .models import Movie, Category
from .serializers import MovieSerializer, CategorySerializer


class MoviesListView(generics.ListCreateAPIView):
    # it has to be authenticated(session, oauth, jwt, etc)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # type of authentication
    authentication_classes = [SessionAuthentication]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def dispatch(self, request, *args, **kwargs):
        print('[USER]: ', self.request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        q = self.request.query_params.get('q', None)
        if q:
            qs = Movie.objects.filter(title__icontains=q)
            return qs
        return super().get_queryset(*args, **kwargs)


class MoviesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class CategoriesListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
