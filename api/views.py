from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Story, Contribution
from django.db.models import Prefetch
from .serializers import RegisterSerializer, StorySerializer, ContributionSerializer, UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetUser(APIView):
    def get(self, request):
        user = request.user
        serialiser = UserSerializer(user)
        return Response (serialiser.data, status=status.HTTP_200_OK)
    
class StoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stories = Story.objects.prefetch_related(
                Prefetch('contributions', queryset=Contribution.objects.all())
                ).all()
        serializer = StorySerializer(stories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id):
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            raise NotFound(detail="Story not found!", code=status.HTTP_404_NOT_FOUND)
        serializer = StorySerializer(story)
        return Response(serializer.data)

class ContributionCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, story_id):
        try:
            story = Story.objects.get(id=story_id)
            story.content = story.content + " " + request.data['text']
            story.save()
        except Story.DoesNotExist:
            return Response({"error": "Story not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if story.is_complete:
            return Response({"error": "This story is complete and cannot accept more contributions."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        serializer = ContributionSerializer(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.story = story
            obj.contributor = request.user
            obj.save()
            
            if story.contributions.count() >= 4:
                story.is_complete = True
                story.save()
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
