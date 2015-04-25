from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions, authentication
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient


class KeywordSuggestion(APIView):
    """
    """
    def get(self, request, *args, **kw):
        args = self.request.GET.dict()
        keyword = args['q'].lower()
        conn = MongoClient()
        coll = conn['feed']['feeds']
        query = {"tag": {"$regex": keyword}}
        items = coll.find(query, {'tag': True, '_id': False}).distinct('tag')[:10]
        # for item in items:
        # 	print item
        # print items
        api_status=status.HTTP_200_OK
        response = Response(list(items), status=api_status)
        return response


class HeatMapData(APIView):
    """
    """
    def get(self, request, *args, **kw):
        args = self.request.GET.dict()
        keyword = args['q'].lower()
        conn = MongoClient()
        coll = conn['feed']['feeds']
        key_words = ["italian", "american"]
        tags_words = []
        for key_word in key_words:
        	tags_words.append({"tag": keyword})
        items = coll.find({'$or': tags_words}, {"location": True, "_id": False})
        # for item in items:
        # 	print item
        # print items
        api_status = status.HTTP_200_OK
        response = Response(list(items), status=api_status)
        return response


class Listings(APIView):
    """
    """
    def get(self, request, *args, **kw):
        args = self.request.GET.dict()
        conn = MongoClient()
        coll = conn['feed']['listings']
        items = coll.find({"gym": args['gym'], "parking": args['parking'], "lift": args['lift'], "rooms": args['rooms'], "property_type": args['property_type'], 'location': {'$geoWithin': {'$centerSphere': [[77.595531, 12.876028], 100 / 6378.1]}}})
        api_status=status.HTTP_200_OK
        response = Response(list(items), status=api_status)
        return response
