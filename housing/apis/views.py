from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions, authentication
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import json	

mongo_host = '45.55.230.155'

class KeywordSuggestion(APIView):
    """
    """
    def get(self, request, *args, **kw):
        args = self.request.GET.dict()
        keyword = args['q'].lower()
        conn = MongoClient(host=mongo_host)
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
        print 'args', args
        conn = MongoClient(host=mongo_host)
        coll = conn['feed']['feeds']
        key_words = ["italian", "american"]
        tags_words = []
        for key_word in key_words:
        	tags_words.append({"tag": key_word})
        items = coll.find({'$or': tags_words}, {"location": True, "weight": True, "_id": False})
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
        conn = MongoClient(host=mongo_host)
        coll = conn['feed']['listing']
        data = {}
        parm_dict = {'true': 1, 'false': 0}
        print 'args', args
        data["$or"]=[]
        if 'gym' in args:
        	data['gym'] = parm_dict[args['gym']]
        if 'parking' in args:
        	data['parking'] = parm_dict[args['parking']]
        if 'lift' in args:
        	data['lift'] = parm_dict[args['lift']]
        # if 'swimming_pool' in args:
        # 	data['swimming_pool'] = parm_dict[args['swimming_pool']]
        if 'rooms' in args:
        	rooms = args['rooms']
        	roomz = rooms.split(",")
        	for r in roomz:
        		data['$or'].append({"rooms":int(r)})
        if 'property_type' in args:
        	property_t = args['property_type']
        	property_ty = rooms.split(",")
        	for r in property_ty:
        		data['$or'].append({"property_type":int(r)})
        if 'location' in args:
        	location = json.loads(args['location'])
        	data['location'] = {'$geoWithin': {'$centerSphere': [location, 100 / 6378.1]}}	
        print 'data', data
        items = coll.find(data,{"_id":False})
        api_status=status.HTTP_200_OK
        response = Response(list(items), status=api_status)
        return response
