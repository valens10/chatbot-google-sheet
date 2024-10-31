from .models import UserData, UserScoring 
from rest_framework.response import Response
from .serializers import UserDataSerializer, UserScoringSerializer, generate_random_scores
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class UserScoringList(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = UserScoringSerializer
    queryset = UserScoring.objects.all()

    def get_queryset(self):
        queryset = UserScoring.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class UserScoringDetail(GenericAPIView, RetrieveModelMixin):
    """
    Retrieve scoring information for a specific user based on user ID.
    """
    serializer_class = UserScoringSerializer
    queryset = UserScoring.objects.all()

    def get_queryset(self):
        return UserScoring.objects.all()

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            # Check if UserData exists for the given user_id
            user_data = UserData.objects.get(id=user_id)
            user_scoring = self.get_queryset().get(user=user_data)
            serializer = self.get_serializer(user_scoring)
            return Response(serializer.data, status=200)
        
        except UserData.DoesNotExist:
            return Response({'error': 'User data not found.'}, status=404)
        
        except UserScoring.DoesNotExist:
            return Response({'error': 'User scoring data not found.'}, status=404)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)


@api_view(['POST', 'PATCH'])
def handle_user_data(request):
    users_data = request.data

    if not isinstance(users_data, list):
        return Response({"error": "Request data must be a list of users."}, status=status.HTTP_400_BAD_REQUEST)

    user_responses = []

    for user_data in users_data:
        user_id = user_data.get('id')
        user_response = process_single_user_data(user_data, user_id)
        user_responses.append(user_response)

    return Response(user_responses, status=status.HTTP_200_OK)

def process_single_user_data(user_data, user_id=None):
    try:
        # Update existing user if ID is provided
        if user_id:
            user = UserData.objects.get(id=user_id)
            serializer = UserDataSerializer(user, data=user_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                scoring = create_or_update_scoring(user)
                return {'user': serializer.data, 'scoring': UserScoringSerializer(scoring).data}
            else:
                return {"error": serializer.errors}

        # Create a new user if not found
        serializer = UserDataSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save(id=user_id if user_id else None)
            scoring = create_or_update_scoring(user)
            return {'user': serializer.data, 'scoring': UserScoringSerializer(scoring).data}
        else:
            return {"error": serializer.errors}

    except UserData.DoesNotExist:
        serializer = UserDataSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save(id=user_id)
            scoring = create_or_update_scoring(user)
            return {'user': serializer.data, 'scoring': UserScoringSerializer(scoring).data}
        else:
            return {"error": serializer.errors}
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": "An unexpected error occurred."}


def create_or_update_scoring(user):
    scores = generate_random_scores()
    scoring, created = UserScoring.objects.update_or_create(user=user, defaults=scores)
    return scoring
