from django.db import models


class FaqCategory(models.Model):
    name = models.CharField(max_length=255, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort_order',)
        verbose_name_plural = 'FAQ categories'


class FaqHeading(models.Model):
    category = models.ForeignKey('FaqCategory', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('sort_order',)
        verbose_name = 'FAQ heading'


class FaqItem(models.Model):
    heading = models.ForeignKey('FaqHeading', null=True, on_delete=models.SET_NULL, related_name='items')
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    sort_order = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('sort_order',)
        verbose_name = 'FAQ item'
