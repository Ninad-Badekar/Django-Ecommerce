from products.models import Category



def catego():
    categories = ["Sneakers", "Running", "Casual", "Training", "Walking"]
    for c in categories:
        Category.objects.get_or_create(name=c)

catego()