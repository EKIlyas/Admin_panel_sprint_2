from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, Role


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']
    queryset = FilmWork.objects.all()

    @staticmethod
    def extend_queryset(qs):
        # не совсем понял комментарий, наверное так
        qs = qs.annotate(genres_arr=ArrayAgg('genres__name', distinct=True))
        qs = qs.annotate(actors=ArrayAgg('persons__full_name', distinct=True,
                                         filter=Q(personfilmwork__role=Role.ACTOR.value)))
        qs = qs.annotate(writers=ArrayAgg('persons__full_name', distinct=True,
                                          filter=Q(personfilmwork__role=Role.WRITER.value)))
        qs = qs.annotate(directors=ArrayAgg('persons__full_name', distinct=True,
                                            filter=Q(personfilmwork__role=Role.DIRECTOR.value)))

        return qs

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.extend_queryset(qs)
        qs = qs.values('id', 'title', 'description', 'creation_date', 'rating', 'type', 'genres_arr', 'actors',
                       'writers', 'directors')
        return qs

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class Movies(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()

        if self.request.GET.get('page', None):
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
            context = {
                'count': paginator.count,
                'total_pages': paginator.num_pages,
                'prev': page.number if not page.has_previous() else page.previous_page_number(),
                'next': page.number if not page.has_next() else page.next_page_number(),
                'results': list(queryset)
            }
        else:
            context = {
                'results': list(queryset)
            }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = self.get_object()
        return context
