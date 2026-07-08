from django.shortcuts import render
from .models import Profile

def profile_view(request):
    profile = Profile.objects.first()
    links = profile.links.filter(is_active=True) if profile else []
    
    context = {
        'profile': profile,
        'links': links,
    }
    return render(request, 'core/profile.html', context)
