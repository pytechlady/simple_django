import json

from marshmallow import ValidationError
from django.views.generic import View

from techtest.author.models import Author
from techtest.author.schemas import AuthorSchema
from techtest.utils import json_response


class AuthorListView(View):
  
    def get(self, request, author_id=None):
        if author_id:
            try:
                author = Author.objects.get(id=author_id)
                return json_response(AuthorSchema().dump(author))
            except:
                return json_response({"error" : "This author does not exist"}, status=400)
        else:
            authors = Author.objects.all()
            return json_response(AuthorSchema().dump(authors, many=True))

    def post(self, request):
        try:
            author = AuthorSchema().load(json.loads(request.body))
        except ValidationError as e:
            return json_response(e.messages, status=400)
        return json_response(AuthorSchema().dump(author), status=201)
    
    def put(self, request, author_id):
        try:
            author_data = json.loads(request.body)
            author = Author.objects.get(id=author_id)
            author.first_name = author_data['first_name']
            author.last_name = author_data['last_name']
            author.save()
        except ValidationError as e:
            return json_response(e.messages, status=400)
        return json_response(AuthorSchema().dump(author), status=200)   

    def delete(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            author.delete()
            return json_response(None, status=204)
        except Author.DoesNotExist:
            return json_response({"error" : "This author does not exist"}, status=400)
