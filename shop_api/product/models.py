from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    @property
    def products_count(self):
        count = self.products.count()
        return count

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, null=True)


    @property
    def rating(self):
        stars_list = [review.stars for review in self.reviews.all()]
        if not stars_list:
            return 0
        average_mark = round(sum(stars_list) / len(stars_list), 2)
        return average_mark

    def __str__(self):
        return self.title


STARS = (
    (1, '*'),
    (2, '* ' * 2),
    (3, '* ' * 3),
    (4, '* ' * 4),
    (5, '* ' * 5),
)


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(default=5, choices=STARS, null=True)

    def __str__(self):
        return self.product.title



