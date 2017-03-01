from .models import Place

def place_processor(request):
    places = Place.objects.all()
    return {
        'all_places': places,
    }


