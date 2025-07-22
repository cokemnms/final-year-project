from .models import ScrapPost

def get_saved_scrap_posts(user):
    return ScrapPost.objects.filter(savedscrapposts__user=user)
