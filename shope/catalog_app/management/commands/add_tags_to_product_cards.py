import os
import json

from django.core.management import BaseCommand

from catalog_app.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(os.path.abspath(os.path.join('fixtures', '05_tag.json')), 'r') as tag_file:
            tag_dict = json.load(tag_file)
            tags = list()
            for data in tag_dict:
                tags.append(data['fields']['name'])
            with open(os.path.abspath(os.path.join('fixtures', '07_taggeditem.json')), 'r') as taggeditem_file:
                taggeditem_dict = json.load(taggeditem_file)
                taggeditem = dict()
                for data in taggeditem_dict:
                    product_pk = data['fields']['object_id']
                    tag_name_for_product = data['fields']['tag']
                    taggeditem[product_pk] = taggeditem.get(product_pk, []) + [tag_name_for_product]

                for product_id, tag_name in taggeditem.items():
                    product = Product.objects.get(pk=product_id)
                    for tag_index in tag_name:
                        t = tags[tag_index - 1]
                        product.tag.add(t)
                    product.save()
