from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from save_moves.apis.save_to_db import insert_db

# for get requests use: http://127.0.0.1:8000/save_moves/chessgamelog
# CHECK IF FILTERING WORKS

# http://127.0.0.1:8000/rest_apis/postdata
@api_view(['POST'])
def postData(request):
    print(request.method)
    print(request.data)

    requestDict = request.data

    print(requestDict)

    insert_db(requestDict)

    return Response(
        data=requestDict,
        status=status.HTTP_200_OK
    )