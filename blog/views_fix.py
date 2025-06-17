from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import Profile
from .serializer import ProfileSerializer

print("views_fix.py is being imported!")

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def create_profile(request):
    """Create a new profile for the currently logged-in user"""
    try:
        # Check if profile already exists
        if hasattr(request.user, 'user_profile'):
            return Response(
                {'error': 'Profile already exists for this user'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create profile data dictionary
        profile_data = {
            'job_title': request.data.get('job_title', ''),
            'job_status': request.data.get('job_status', ''),
            'brief': request.data.get('brief', ''),
            'years_of_experience': request.data.get('years_of_experience', 0),
            'phone_number': request.data.get('phone_number', ''),
        }

        # Handle profile image if provided (supporting both field names)
        if 'profile_image' in request.FILES:
            profile_data['profile_image'] = request.FILES['profile_image']
        elif 'profile_picture' in request.FILES:
            profile_data['profile_image'] = request.FILES['profile_picture']

        # Create profile
        profile = Profile.objects.create(
            user=request.user,
            **profile_data
        )

        # Serialize and return the created profile
        serializer = ProfileSerializer(profile)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST', 'PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def edit_profile(request):
    """Update the profile of the currently logged-in user"""
    try:
        # Check if profile exists
        if not hasattr(request.user, 'user_profile'):
            return Response(
                {'error': 'Profile does not exist for this user'},
                status=status.HTTP_404_NOT_FOUND
            )

        profile = request.user.user_profile

        # Update user fields (first_name, last_name)
        user_updated = False
        if 'first_name' in request.data:
            request.user.first_name = request.data['first_name']
            user_updated = True
        if 'last_name' in request.data:
            request.user.last_name = request.data['last_name']
            user_updated = True
        
        if user_updated:
            request.user.save()

        # Update profile data
        if 'job_title' in request.data:
            profile.job_title = request.data['job_title']
        if 'job_status' in request.data:
            profile.job_status = request.data['job_status']
        if 'brief' in request.data:
            profile.brief = request.data['brief']
        if 'years_of_experience' in request.data:
            profile.years_of_experience = request.data['years_of_experience']
        if 'phone_number' in request.data:
            profile.phone_number = request.data['phone_number']

        # Handle profile image update (supporting both profile_image and profile_picture field names)
        profile_image_key = None
        if 'profile_image' in request.FILES:
            profile_image_key = 'profile_image'
        elif 'profile_picture' in request.FILES:
            profile_image_key = 'profile_picture'
        
        if profile_image_key:
            # Delete old image if it exists
            if profile.profile_image:
                profile.profile_image.delete()
            profile.profile_image = request.FILES[profile_image_key]

        # Save the updated profile
        profile.save()

        # Return the updated profile data
        serializer = ProfileSerializer(profile)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
