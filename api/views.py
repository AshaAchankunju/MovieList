from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Movie
from rest_framework import status
from api.serializers import MovieSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
# Create your views here.


class HelloWorldView(APIView):
    def get(self,request,*args,**kwargs):
        context={"message":"helloworld"}
        return Response(data=context)

class MorningView(APIView):
    def get(self,request,*args,**kwargs):
        context={"message":"Goodmorning"}
        return Response(data=context)

# url:localhost:8000/addition/
# method:post
# data={'num1':100,'num2':200}
    
class AdditionView(APIView):
    def post(self,request,*args,**kwargs):
        n1=request.data.get("num1")
        n2=request.data.get("num2")
        result=int(n1)+int(n2)
        context={"result":result}
        return Response(data=context)
    
# url:localhost:8000/bmi/
# method:post
# data={"height":120,"weight":50}

class BmiView(APIView):
    def post(self,request,*args,**kwargs):
        height_in_cm=int(request.data.get("height"))
        weight_in_kg=int(request.data.get("weight"))
        height_in_meter=height_in_cm/100
        bmi=weight_in_kg/(height_in_meter)**2
        context={"result":bmi}
        return Response(data=context)
    

# uel:localhost:8000/calories/
# method: post
# data={"height":156,"weight":76,"age":21,"gender":male|female}
    
class CalorieView(APIView):
    def post(self,request,*args,**kwargs):
        height=int(request.data.get("height"))
        weight=int(request.data.get("weight"))
        age=int(request.data.get("age"))
        gender=request.data.get("gender")
        bmr=0
        if gender=="male":
            bmr=(10*weight)+(6.25*height)-(5*age)+5
            context={"calories":bmr}
            return Response(data=context)
        elif gender=="female":
            bmr=(10*weight)+(6.25*height)-(5*age)-161
            context={"calories":bmr}
            return Response(data=context)

# class EmiView(APIView):
#     def post(self,request,*args,**kwargs):
#         p=int(request.data.get("p"))
#         r=int(request.data.get("r"))
#         n=int(request.data.get("n"))
#         emi=p*r*((1+r)*n)/(((1+r)*n)-1)


# ALBUM CRUD
# =====api for listing all albums
    # url:localhost:8000/api/albums/
    # method: get
    # data: nill
        
# ======api for creating new album
    #  url:localhost:8000/api/albums/
    # method: post
    # data:{}
        
class AlbumListView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Movie.objects.all()
        context=qs
        return Response(data=context)
    
    def post(self,request,*args,**kwargs):
        context={"message":"logic for creating a new album"}
        return Response(data=context)


class MovieListCreateView(APIView):
    def get (self, request,*args,**kwargs):
        qs=Movie.objects.all()
        serializer_instance=MovieSerializer(qs, many=True) # serialization
        return Response(data=serializer_instance.data)
    
    def post(self,request,*args,**kwargs):
        data=request.data
        serializer_instance=MovieSerializer(data=data) #deserialization
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)
    
# url:localhost:8000/api/movies/{id}
class MovieRetrieveUpdateDestroyView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            qs=Movie.objects.get(id=id)
            serializer_instance=MovieSerializer(qs)
            return Response(data=serializer_instance.data)
        except:
            context={"message":"requested resources does not exist"}
            return Response(data=context, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Movie.objects.get(id=id).delete()
            return Response(data={"message":"deleted"},status=status.HTTP_200_OK)
        except:
            return Response(data={"message":"resource not found"},status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=request.data
        movie_object=Movie.objects.get(id=id)
        serializer_instance=MovieSerializer(data=data, instance=movie_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
        else:
            return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
        

class MovieViewSetView(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Movie.objects.all()
        # localhost:8000/api/v1/movies?language={value}
        if 'language' in request.query_params:
            value=request.query_params.get("language")
            qs=qs.filter(language=value)
        # localhost:8000/api/v1/movies?genre={value}

        if 'genre' in request.query_params:
            value=request.query_params.get("genre")
            qs=qs.filter(genre=value)

        serializer_instance=MovieSerializer(qs,many=True)
        return Response(data=serializer_instance.data, status=status.HTTP_200_OK)
    
    def create(self,request,*args,**kwargs):
        data=request.data
        serializer_instance=MovieSerializer(data=data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
        else:
            return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Movie.objects.get(id=id)
        serializer_instance=MovieSerializer(qs)
        return Response(data=serializer_instance.data,status=status.HTTP_200_OK)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        movie_obj=Movie.objects.get(id=id)
        data=request.data
        serializer_instance=MovieSerializer(data=data,instance=movie_obj)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
        else:
            return Response(data=serializer_instance.data,status=status.HTTP_400_BAD_REQUEST)
        
    def destoy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Movie.objects.get(id=id)
        return Response(data={"messages":"deleted"},status=status.HTTP_200_OK)

    # url:localhost:8000/api/v1/movies/genres
    # method get
    # url without id
    @action(methods=["get"],detail=False)
    def genres(self,request,*args,**kwargs):
        qs=Movie.objects.values_list("genre",flat=True).distinct()
        return Response(data=qs)

    # url:localhost:8000/api/v1/movies/laguages
    # method get
    # url without id
    @action(methods=["get"],detail=False)
    def languages(self,request,*args,**kwargs):
        qs=Movie.objects.values_list("language",flat=True).distinct()
        return Response(data=qs)


class MovieGenreListView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Movie.objects.all().values_list("genre",flat=True).distinct()
        return Response(data=qs)

class MovieLanguageListView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Movie.objects.all().values_list("language",flat=True).distinct()
        return Response(data=qs)   