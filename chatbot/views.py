from .models import UserData, UserScoring 
from .serializers import UserDataSerializer, UserScoringSerializer, generate_random_scores
import logging

logger = logging.getLogger(__name__)

def handle_user_data(users_data):
    
    if not isinstance(users_data, list):
        return {"error": "Request data must be a list of users."}

    user_responses = []

    for user_data in users_data:
        user_id = user_data.get('id')
        user_response = process_single_user_data(user_data, user_id)
        user_responses.append(user_response)

    return user_responses


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

        # Create a new user if no ID is provided or user not found
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
