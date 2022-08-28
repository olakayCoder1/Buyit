from product.models import Company , Product , ProductCategory



def get_profile_with_discount():
    return Product.objects.filter(discount_rate__gt=0)