from django.views.generic import ListView, DetailView
from .models import Venue, Sport
from django.db.models import Q

class VenueListView(ListView):
    model = Venue
    template_name = 'venue_list/venue_list.html'
    context_object_name = 'venues'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the sport types list from the Sport model
        context['sport_types'] = Sport.objects.all()

        sport_type = self.request.GET.get('sport_type', '')
        location = self.request.GET.get('location', '')
        queryset = Venue.objects.all()

        if sport_type:
            # Use Q objects to handle multiple sport types
            sport_type_query = Q()
            for sport in sport_type.split(','):
                sport_type_query |= Q(sport_types__name__icontains=sport.strip())

            queryset = queryset.filter(sport_type_query)

        if location:
            queryset = queryset.filter(location__icontains=location)

        context['venues'] = queryset
        return context


class VenueDetailView(DetailView):
    model = Venue
    template_name = 'venue_list/venue_detail.html'
    context_object_name = 'venue'