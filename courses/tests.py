from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Course, Category
import requests

class CourseApiTestCase(TestCase):
    def setUp(self):
        # craete admin user
        self.user = get_user_model().objects.create_user(
            username='test', email="test@gmail.com", password="password"
        )
        self.user.is_admin =True
        self.user.is_staff = True
        self.user.save()
        # create not admin user
        self.user2 = get_user_model().objects.create_user(
            username="test2", email="test2@gmail.com", password="password"
        )
        # create category
        self.category = Category.objects.create(title="category1", slug="slugcategory")
        self.category2 = Category.objects.create(title="category2", slug="slugcategory2")
        # create course list
        course_list = [
            Course.objects.create(
                title = "title1",
                slug = "title1",
                overview = "it's title",
                owner = self.user,
                category = self.category
            ),
            Course.objects.create(
                title = "create with aghaye omid",
                slug = "title2",
                overview = "it's simple man",
                owner = self.user,
                category = self.category2
           ),

        ]
        # set students for course1
        course_list[0].students.set([2])
        # create course lookup
        self.course_lookup = {course.id: course for course in course_list}
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
            "students" : [2],
        }
        # create course
        resp = self.client.post('/api/v1/course/', data)
        # 201 -> created
        self.assertEqual(resp.status_code, 201)
        course_id = resp.json()['id']
        # get course to check that our data is correct or not
        course = Course.objects.get(pk=course_id)
        self.assertEqual(course.title, data['title'])
        self.assertEqual(course.slug, data['slug'])
        self.assertEqual(course.overview, data['overview'])
        self.assertEqual(course.owner.id, data['owner'])
        self.assertEqual(course.category.id, data['category'])
        self.assertEqual(course.students.count(), 1)

    def test_course_creation_unauthorized(self):
        # logout
        self.client.credentials()
        data = {
            "title" : "unathorized",
            "slug" : "unathorized2",
            "overview" : "it's simple man",
            "owner" : 1,
            "category" : 1,
            "students" : [2],
        }
        # create course
        resp = self.client.post('/api/v1/course/', data)
        # 403 -> unathorized
        self.assertEqual(resp.status_code, 403)
        

    def test_course_list(self):
        # get courses
        resp = self.client.get('/api/v1/course/')
        self.assertEqual(resp.status_code, 200)
        results = resp.json()['results']
        # check size of course that we get
        self.assertEqual(len(results), 2)
        for course_dict in results:
            course = self.course_lookup[course_dict["id"]]
            self.assertEqual(course.title, course_dict['title'])
            self.assertEqual(course.slug, course_dict['slug'])
            self.assertEqual(course.overview, course_dict['overview'])
            self.assertEqual(course.owner.email, course_dict['owner']['email'])
            self.assertEqual(course.category.id, course_dict['category'])
                    
    