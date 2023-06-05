from marshmallow import validate, ValidationError
from marshmallow import fields
from marshmallow import Schema
from marshmallow.decorators import post_load, pre_load

from techtest.articles.models import Article
from techtest.regions.models import Region
from techtest.regions.schemas import RegionSchema

from techtest.author.models import Author
from techtest.author.schemas import AuthorSchema

from techtest.utils import json_response

        
class ArticleSchema(Schema):
    class Meta(object):
        model = Article

    id = fields.Integer()
    title = fields.String(validate=validate.Length(max=255))
    content = fields.String()
    regions = fields.Method(
        required=False, serialize="get_regions", deserialize="load_regions"
    )
    authors = fields.Nested(AuthorSchema, allow_none=True, many=False, required=False)
    
    def get_regions(self, article):
        return RegionSchema().dump(article.regions.all(), many=True)

    def load_regions(self, regions):
        return [
            Region.objects.get_or_create(id=region.pop("id", None), defaults=region)[0]
            for region in regions
        ]
              
    @pre_load
    def load_authors(self, data, **kwargs):
        author_id = data.get('authors')
        if author_id is not None:
            if isinstance(author_id, dict) and 'id' in author_id:
                try:
                    author = Author.objects.get(id=author_id['id'])
                    data['authors'] = {
                        'id': author.id,
                        'first_name': author.first_name,
                        'last_name': author.last_name
                    }
                except Author.DoesNotExist:
                    data['authors'] = None
            else:
                data['authors'] = None

        return data

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        regions = data.pop("regions", None)
        article, _ = Article.objects.update_or_create(
            id=data.pop("id", None), defaults=data
        )
        if isinstance(regions, list):
            article.regions.set(regions)
        return article
        
