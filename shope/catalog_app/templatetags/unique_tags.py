from django import template
from taggit.models import Tag

register = template.Library()


@register.simple_tag(name='unique_tags')
def get_uniques_tags_from_model_tag():
    """Функция для получения только уникальных тегов из модели"""
    return Tag.objects.all().distinct()
