from products.models import Product, Category

sample_products = [
    {
        "name": "Nike Air Max 270",
        "brand": "Nike",
        "price": 12999,
        "category": "Sneakers",
        "description": "Lightweight sneakers with Air cushioning",
        "image": "products/nike_air_max_270.jpg",
        "stock": 50
    },
    {
        "name": "Adidas Ultraboost 22",
        "brand": "Adidas",
        "price": 15999,
        "category": "Running",
        "description": "Premium running shoes with Boost foam",
        "image": "products/adidas_ultraboost_22.jpg",
        "stock": 40
    },
    {
        "name": "Puma RS-X",
        "brand": "Puma",
        "price": 9999,
        "category": "Casual",
        "description": "Comfortable and stylish chunky sneakers",
        "image": "products/puma_rsx.jpg",
        "stock": 30
    },
    {
        "name": "Reebok Nano X3",
        "brand": "Reebok",
        "price": 11999,
        "category": "Training",
        "description": "Designed for cross-training",
        "image": "products/reebok_nano_x3.jpg",
        "stock": 25
    },
    {
        "name": "Skechers GoWalk 7",
        "brand": "Skechers",
        "price": 7999,
        "category": "Walking",
        "description": "Lightweight walking shoes",
        "image": "products/skechers_gowalk_7.jpg",
        "stock": 60
    }
]

def run():
    for p in sample_products:
        category_obj = Category.objects.get(name=p["category"])
        Product.objects.create(
            name=p["name"],
            brand=p["brand"],
            description=p["description"],
            price=p["price"],
            category=category_obj,
            image=p["image"],
            stock=p["stock"]
        )
    print("Products added successfully!")
run()