from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import *
from django.contrib.contenttypes.fields import ContentType
import json

class ContentApiTestCase(TestCase):
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
        # create another non admin 
        self.user3 = get_user_model().objects.create_user(
            username="test3", email="test3@gmail.com", password="password"
        )
        # create category
        self.category = Category.objects.create(title="category1", slug="slugcategory")
        self.category2 = Category.objects.create(title="category2", slug="slugcategory2")
        # create course
        self.course = Course.objects.create(title = "title1", slug = "title1",
                    overview = "it's title", owner = self.user, category = self.category)


        module_list = [
           Module.objects.create(
                title = "module1",
                description = "it's simple man",
                order = 1,
                course = self.course
           ),
           Module.objects.create(
                title = "module2",
                description = "it's simple",
                order = 2,
                course = self.course
           ),
        ]

        self.text = Text.objects.create(owner=self.user, title='title one', content='this is text1')
        text2 = Text.objects.create(owner=self.user, title='title two', content='this is text2')
        text3 = Text.objects.create(owner=self.user, title='title three', content='this is text3')

        self.content_list = [
            Content.objects.create(module=module_list[0], content_type=ContentType.objects.get(model='text'), object_id=1),
            Content.objects.create(module=module_list[0], content_type=ContentType.objects.get(model='text'), object_id=2),
            Content.objects.create(module=module_list[0], content_type=ContentType.objects.get(model='text'), object_id=3),
        ]
        self.content_lookup = {content.id: content for content in self.content_list}

        # set students for course1
        # course_list[0].students.set([2])
        # # create course lookup
        self.module_lookup = {module.id: module for module in module_list}
        # override test client
        self.client = APIClient()
        auth_endpoint = "/api/v1/token/"
        data = { "email" : "test@gmail.com", "password" : "password"}
        auth_response = self.client.post(auth_endpoint, data)
        token = auth_response.json()['access']  
        # add credentials
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)



        
    def test_content_list(self):
        # get courses
        resp = self.client.get(f'/api/v1/content/')
        self.assertEqual(resp.status_code, 200)
        results = resp.json()['results']
        # check size of content that we get      
        self.assertEqual(len(results), 3)
        for resp in results:
            content = self.content_lookup[resp["id"]]
            self.assertEqual(resp["id"], content.id)
            self.assertEqual(resp["order"], content.order)
            self.assertEqual(resp["content_type"], content.content_type.id)
            self.assertEqual(resp["order"], content.order)
            self.assertEqual(resp["module"], content.module.id)
            self.assertEqual(resp["object_id"], content.object_id)

 
    def test_content_create_authorized(self):
        # create text object
        text_list = [
            Text.objects.create(owner=self.user, title='title four', content='this is text4'),
            Text.objects.create(owner=self.user, title='title five', content='this is text5')
        ]
        data = {
            "description" : "it's 1",
            "title" : "it's simple",
            "course" : self.course.id,
            "object_id" : text_list[1].id,
            "module": 1,
            "content_type": ContentType.objects.get(model='text').id
        }
        # create new module
        resp = self.client.post('/api/v1/content/', data)
        # 201 --> request was successful and as a result, a resource has been created 
        
        self.assertEqual(resp.status_code, 201)
        content_id = resp.json()['id']
        # get course to check that our data is correct or not
        content = Content.objects.get(pk=content_id)
        data = resp.json()
        self.assertEqual(content.id, data['id'])
        self.assertEqual(content.order, data['order'])
        self.assertEqual(content.module.id, data['module'])
        self.assertEqual(content.content_type.id, data['content_type'])
        self.assertEqual(content.object_id, data['object_id'])
 
    def test_content_create_unauthorized(self):
        # logout
        self.client.credentials()
        # create text object
        text_list = [
            Text.objects.create(owner=self.user, title='title four', content='this is text4'),
            Text.objects.create(owner=self.user, title='title five', content='this is text5')
        ]
        data = {
            "description" : "it's 1",
            "title" : "it's simple",
            "course" : self.course.id,
            "object_id" : text_list[1].id,
            "module": 1,
            "content_type": ContentType.objects.get(model='text').id
        }
        # create new module
        resp = self.client.post('/api/v1/content/', data)
        #  403 --> user dosnt create
        self.assertEqual(resp.status_code,  403)
        # login not admin user
        auth_endpoint = "/api/v1/token/"
        data = { "email" : "test2@gmail.com", "password" : "password"}
        auth_response = self.client.post(auth_endpoint, data)
        token = auth_response.json()['access']  
        # add credentials
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        resp = self.client.put('/api/v1/module/1/', data)
        # 403 --> indicates that the server understands the request but refuses to authorize it
        self.assertEqual(resp.status_code, 403)


    # def test_module_create_unauthorized(self):
    #     # logout
    #     self.client.credentials()
    #     data = {
    #         "title" : "module3",
    #         "description" : "it's simple",
    #         "course" : self.course.id
    #     }
    #     # create new module
    #     resp = self.client.post('/api/v1/module/', data)
    #     # 403 --> indicates that the server understands the request but refuses to authorize it
    #     self.assertEqual(resp.status_code, 403)
