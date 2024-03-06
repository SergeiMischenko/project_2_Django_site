from django.contrib.sitemaps import Sitemap

from funnytail.models import Breed, Cats, TagPosts


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Cats.published.all()

    def lastmod(self, obj):
        return obj.time_update


class BreedSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Breed.objects.all()


class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return TagPosts.objects.all()
