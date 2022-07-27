from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Course, Category
import requests

class CourseApiTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email="test@gmail.com", password="password"
        )
        self.user.is_admin =True
        self.user.is_staff = True
        self.user.save()
        # create category
        self.category = Category.objects.create(title="category1", slug="slugcategory")
        # override test client
        self.client = APIClient()
        auth_endpoint = "/api/v1/token/"
        data = { "email" : "test@gmail.com", "password" : "password"}
        auth_response = self.client.post(auth_endpoint, data)
        token = auth_response.json()['access']  
        # add credentials
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        
    def test_course_create(self):
        data = {
            "title" : "create with aghaye omid",
            "slug" : "agha",
            "overview" : "it's simple man",
            "owner" : 1,
            "category" : 1,
            "students" : [],
        }
        # create course
        resp = self.client.post('/api/v1/course/', data)
        course_id = resp.json()['id']
        # get course to check that our data is correct or not
        course = Course.objects.get(pk=course_id)
        self.assertEqual(course.title, data['title'])
        self.assertEqual(course.slug, data['slug'])
        self.assertEqual(course.overview, data['overview'])
        self.assertEqual(course.owner.id, data['owner'])
        self.assertEqual(course.category.id, data['category'])
        self.assertEqual(course.students.count(), 0)

