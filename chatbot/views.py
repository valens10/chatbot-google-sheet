from django.shortcuts import render
from rest_framework.response import Response
from .services import get_all_rows

def photo_wall():
  photos = get_all_rows("Test sheet")
  print('photos', photos)
  return Response(photos)

photo_wall()


