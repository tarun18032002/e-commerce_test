from .models import Category

def category_links(request):
    links = Category.objects.all()
    return {'links': links}
# This context processor retrieves all categories from the database and makes them available in the template context under the key 'links'.