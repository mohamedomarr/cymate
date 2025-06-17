from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
import tempfile
from .models import Profile, Post, Comment, Reacts
import json

User = get_user_model()


class UserDetailsEnhancementTests(APITestCase):
    """Test cases for the enhanced /auth/user/ endpoint"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_user_details_includes_first_last_name(self):
        """Test that /auth/user/ endpoint returns first_name and last_name"""
        url = reverse('rest_user_details')  # dj-rest-auth endpoint
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'id': self.user.id,
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.assertEqual(response.data, expected_data)
    
    def test_user_details_with_empty_names(self):
        """Test endpoint with empty first_name and last_name"""
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        url = reverse('rest_user_details')
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')


class ProfileCreationTests(APITestCase):
    """Test cases for profile creation with image upload"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Delete the auto-created profile for testing
        if hasattr(self.user, 'user_profile'):
            self.user.user_profile.delete()
    
    def create_test_image(self, format='JPEG'):
        """Helper method to create a test image"""
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format=format)
        image_io.seek(0)
        return SimpleUploadedFile(
            f'test_image.{format.lower()}',
            image_io.getvalue(),
            content_type=f'image/{format.lower()}'
        )
    
    def test_create_profile_with_image(self):
        """Test creating profile with profile image"""
        test_image = self.create_test_image()
        
        data = {
            'job_title': 'Software Engineer',
            'job_status': 'Full-time',
            'brief': 'Experienced developer',
            'years_of_experience': 5,
            'phone_number': '+1234567890',
            'profile_image': test_image
        }
        
        url = reverse('profile-create')
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.job_title, 'Software Engineer')
        self.assertTrue(profile.profile_image)
    
    def test_create_profile_with_profile_picture_field(self):
        """Test creating profile using profile_picture field name"""
        test_image = self.create_test_image()
        
        data = {
            'job_title': 'Designer',
            'profile_picture': test_image  # Using alternative field name
        }
        
        url = reverse('profile-create')
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        profile = Profile.objects.get(user=self.user)
        self.assertTrue(profile.profile_image)
    
    def test_create_profile_image_size_validation(self):
        """Test profile image size validation"""
        # Create a large image (> 5MB)
        large_image = Image.new('RGB', (5000, 5000), color='red')
        image_io = io.BytesIO()
        large_image.save(image_io, format='JPEG', quality=100)
        image_io.seek(0)
        
        large_file = SimpleUploadedFile(
            'large_image.jpg',
            image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        data = {
            'job_title': 'Test',
            'profile_image': large_file
        }
        
        url = reverse('profile-create')
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_profile_invalid_file_type(self):
        """Test validation for invalid file types"""
        invalid_file = SimpleUploadedFile(
            'test.txt',
            b'This is not an image',
            content_type='text/plain'
        )
        
        data = {
            'job_title': 'Test',
            'profile_image': invalid_file
        }
        
        url = reverse('profile-create')
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileEditingTests(APITestCase):
    """Test cases for profile editing functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Ensure profile exists
        self.profile = self.user.user_profile
    
    def create_test_image(self):
        """Helper method to create a test image"""
        image = Image.new('RGB', (100, 100), color='blue')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return SimpleUploadedFile(
            'test_image.jpg',
            image_io.getvalue(),
            content_type='image/jpeg'
        )
    
    def test_edit_first_name_last_name(self):
        """Test editing user's first_name and last_name"""
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        
        url = reverse('profile-edit')
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Smith')
    
    def test_edit_profile_fields(self):
        """Test editing profile-specific fields"""
        data = {
            'job_title': 'Senior Developer',
            'job_status': 'Remote',
            'brief': 'Updated brief',
            'years_of_experience': 8,
            'phone_number': '+9876543210'
        }
        
        url = reverse('profile-edit')
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.job_title, 'Senior Developer')
        self.assertEqual(self.profile.job_status, 'Remote')
        self.assertEqual(self.profile.years_of_experience, 8)
    
    def test_edit_profile_image(self):
        """Test updating profile image"""
        test_image = self.create_test_image()
        
        data = {
            'job_title': 'Updated Title',
            'profile_image': test_image
        }
        
        url = reverse('profile-edit')
        response = self.client.put(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.profile_image)
        self.assertEqual(self.profile.job_title, 'Updated Title')
    
    def test_edit_with_profile_picture_field(self):
        """Test updating using profile_picture field name"""
        test_image = self.create_test_image()
        
        data = {
            'profile_picture': test_image
        }
        
        url = reverse('profile-edit')
        response = self.client.put(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.profile_image)
    
    def test_partial_update_patch(self):
        """Test PATCH method for partial updates"""
        data = {
            'first_name': 'UpdatedName'
        }
        
        url = reverse('profile-edit')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedName')
        self.assertEqual(self.user.last_name, 'Doe')  # Should remain unchanged


class ProfileSerializerTests(TestCase):
    """Test cases for ProfileSerializer enhancements"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.profile = self.user.user_profile
    
    def test_serializer_includes_user_names(self):
        """Test that ProfileSerializer includes first_name and last_name"""
        from .serializer import ProfileSerializer
        
        serializer = ProfileSerializer(self.profile)
        data = serializer.data
        
        self.assertIn('first_name', data)
        self.assertIn('last_name', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
    
    def test_serializer_includes_profile_picture_alias(self):
        """Test that ProfileSerializer includes profile_picture field as alias"""
        from .serializer import ProfileSerializer
        
        serializer = ProfileSerializer(self.profile)
        data = serializer.data
        
        self.assertIn('profile_picture', data)
        self.assertIn('profile_image', data)


class AuthenticationIntegrationTests(APITestCase):
    """Integration tests for authentication and profile management"""
    
    def test_full_user_workflow(self):
        """Test complete workflow: register, login, get user details, create/edit profile"""
        # 1. Register user
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        register_url = reverse('rest_register')
        register_response = self.client.post(register_url, register_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        # 2. Get token from registration response
        token = register_response.data.get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        # 3. Check user details endpoint
        user_details_url = reverse('rest_user_details')
        user_response = self.client.get(user_details_url)
        self.assertEqual(user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_response.data['first_name'], 'New')
        self.assertEqual(user_response.data['last_name'], 'User')
        
        # 4. Update profile
        user = User.objects.get(username='newuser')
        # Delete auto-created profile for testing
        if hasattr(user, 'user_profile'):
            user.user_profile.delete()
        
        profile_data = {
            'job_title': 'Developer',
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        create_profile_url = reverse('profile-create')
        profile_response = self.client.post(create_profile_url, profile_data)
        self.assertEqual(profile_response.status_code, status.HTTP_201_CREATED)
        
        # 5. Edit profile
        edit_data = {
            'job_title': 'Senior Developer',
            'first_name': 'Final',
            'last_name': 'Name'
        }
        
        edit_profile_url = reverse('profile-edit')
        edit_response = self.client.put(edit_profile_url, edit_data)
        self.assertEqual(edit_response.status_code, status.HTTP_200_OK)
        
        # 6. Verify changes
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Final')
        self.assertEqual(user.last_name, 'Name')
        self.assertEqual(user.user_profile.job_title, 'Senior Developer')


class UserCreationTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('testpass123'))


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_creation(self):
        """Test that a profile is automatically created when a user is created"""
        self.assertTrue(hasattr(self.user, 'user_profile'))
        self.assertIsInstance(self.user.user_profile, Profile)

    def test_profile_str_method(self):
        """Test the string representation of Profile"""
        expected = f"{self.user.username}'s Profile"
        self.assertEqual(str(self.user.user_profile), expected)


class CommentEnhancementTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            post_type='post'
        )
    
    def test_comment_includes_user_names(self):
        """Test that comments include first_name and last_name"""
        comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test comment'
        )
        
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post_data = response.data['post']
        self.assertEqual(len(post_data['comments']), 1)
        
        comment_data = post_data['comments'][0]
        self.assertEqual(comment_data['first_name'], 'John')
        self.assertEqual(comment_data['last_name'], 'Doe')
        self.assertEqual(comment_data['user'], 'testuser')
        self.assertEqual(comment_data['content'], 'Test comment')


class PostDeletionTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        self.user_token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.other_token = Token.objects.create(user=self.other_user)
        
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            post_type='post'
        )
    
    def test_owner_can_delete_post(self):
        """Test that post owner can delete their post"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        
        url = reverse('post-edit', kwargs={'post_id': self.post.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
    
    def test_admin_can_delete_post(self):
        """Test that admin can delete any post"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        
        url = reverse('post-edit', kwargs={'post_id': self.post.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
    
    def test_non_owner_cannot_delete_post(self):
        """Test that non-owner cannot delete post"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
        
        url = reverse('post-edit', kwargs={'post_id': self.post.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())


class TagFilteringTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create posts with different tags
        self.post1 = Post.objects.create(
            title='Tech Post',
            content='Tech content',
            author=self.user,
            post_type='post'
        )
        self.post1.tags.add('technology', 'python')
        
        self.post2 = Post.objects.create(
            title='AI Post',
            content='AI content',
            author=self.user,
            post_type='blog'
        )
        self.post2.tags.add('ai', 'technology')
        
        self.post3 = Post.objects.create(
            title='Sports Post',
            content='Sports content',
            author=self.user,
            post_type='post'
        )
        self.post3.tags.add('sports', 'football')
    
    def test_filter_by_single_tag(self):
        """Test filtering posts by a single tag"""
        url = reverse('post-list') + '?tags=technology'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posts = response.data['posts']['results']
        self.assertEqual(len(posts), 2)  # post1 and post2 have 'technology' tag
        
        post_titles = [post['title'] for post in posts]
        self.assertIn('Tech Post', post_titles)
        self.assertIn('AI Post', post_titles)
        self.assertNotIn('Sports Post', post_titles)
    
    def test_filter_by_multiple_tags(self):
        """Test filtering posts by multiple tags"""
        url = reverse('post-list') + '?tags=technology,sports'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posts = response.data['posts']['results']
        self.assertEqual(len(posts), 3)  # All posts match either tag
    
    def test_filter_by_nonexistent_tag(self):
        """Test filtering by tag that doesn't exist"""
        url = reverse('post-list') + '?tags=nonexistent'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posts = response.data['posts']['results']
        self.assertEqual(len(posts), 0)
    
    def test_no_tag_filter_returns_all_posts(self):
        """Test that without tag filter, all posts are returned"""
        url = reverse('post-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posts = response.data['posts']['results']
        self.assertEqual(len(posts), 3)


class ReactionBreakdownTests(APITestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='pass123'
        )
        
        self.token1 = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user1,
            post_type='post'
        )
        
        # Create different reactions
        Reacts.objects.create(user=self.user1, post=self.post, react='Love')
        Reacts.objects.create(user=self.user2, post=self.post, react='Love')
        Reacts.objects.create(user=self.user3, post=self.post, react='Dislike')
    
    def test_reaction_breakdown_in_post_detail(self):
        """Test that post detail returns reaction breakdown"""
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post_data = response.data['post']
        
        expected_reactions = {
            'Love': 2,
            'Dislike': 1,
            'Thunder': 0
        }
        self.assertEqual(post_data['reactions'], expected_reactions)
    
    def test_reaction_breakdown_in_post_list(self):
        """Test that post list returns reaction breakdown"""
        url = reverse('post-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posts = response.data['posts']['results']
        self.assertEqual(len(posts), 1)
        
        expected_reactions = {
            'Love': 2,
            'Dislike': 1,
            'Thunder': 0
        }
        self.assertEqual(posts[0]['reactions'], expected_reactions)


class NewReactionTypesTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user,
            post_type='post'
        )
    
    def test_valid_reaction_types(self):
        """Test that only Love, Dislike, Thunder are accepted"""
        valid_reactions = ['Love', 'Dislike', 'Thunder']
        
        for reaction in valid_reactions:
            url = reverse('post-interact', kwargs={'pk': self.post.id})
            data = {
                'action_type': 'react',
                'react_type': reaction
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_reaction_types(self):
        """Test that old reaction types are rejected"""
        invalid_reactions = ['like', 'love', 'angry', 'sad', 'haha', 'wow']
        
        for reaction in invalid_reactions:
            url = reverse('post-interact', kwargs={'pk': self.post.id})
            data = {
                'action_type': 'react',
                'react_type': reaction
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('Invalid reaction type', response.data['error'])
    
    def test_reaction_toggle(self):
        """Test that reacting with same type toggles (removes) the reaction"""
        # First reaction
        url = reverse('post-interact', kwargs={'pk': self.post.id})
        data = {
            'action_type': 'react',
            'react_type': 'Love'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Reacts.objects.filter(user=self.user, post=self.post).exists())
        
        # Same reaction again (should remove)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Reacts.objects.filter(user=self.user, post=self.post).exists())
    
    def test_reaction_change(self):
        """Test that reacting with different type changes the reaction"""
        # First reaction
        url = reverse('post-interact', kwargs={'pk': self.post.id})
        data = {
            'action_type': 'react',
            'react_type': 'Love'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Change to different reaction
        data['react_type'] = 'Dislike'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        reaction = Reacts.objects.get(user=self.user, post=self.post)
        self.assertEqual(reaction.react, 'Dislike')
