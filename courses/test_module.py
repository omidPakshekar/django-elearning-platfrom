from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import *
from django.contrib.contenttypes.fields import ContentType
import json

class ModuleApiTestCase(TestCase):
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

    
        
    def test_module_list(self):
        # get courses
        resp = self.client.get(f'/api/v1/module/')
        self.assertEqual(resp.status_code, 200)
        results = resp.json()['results']
        # check size of module that we get      
        self.assertEqual(len(results), 2)
        for resp in results:
            module = self.module_lookup[resp["id"]]
            self.assertEqual(resp["id"], module.id)
            self.assertEqual(resp["title"], module.title)
            self.assertEqual(resp["description"], module.description)
            self.assertEqual(resp["order"], module.order)

 
    def test_module_create_authorized(self):
        data = {
            "title" : "module3",
            "description" : "it's simple",
            "course" : self.course.id
        }
        # create new module
        resp = self.client.post('/api/v1/module/', data)
        # 201 --> request was successful and as a result, a resource has been created 
        self.assertEqual(resp.status_code, 201)
        module_id = resp.json()['id']
        # get course to check that our data is correct or not
        module = Module.objects.get(pk=module_id)
        self.assertEqual(module.title, data['title'])
        self.assertEqual(module.description, data['description'])
        self.assertEqual(module.course.id, data['course'])


    def test_module_create_unauthorized(self):
        # logout
        self.client.credentials()
        data = {
            "title" : "module3",
            "description" : "it's simple",
            "course" : self.course.id
        }
        # create new module
        resp = self.client.post('/api/v1/module/', data)
        # 403 --> indicates that the server understands the request but refuses to authorize it
        self.assertEqual(resp.status_code, 403)

            
    def test_module_update(self):
        data = {
                "course" : self.course.id,
                "title" : "change title",
                "description" : "it's description"
        }
        resp = self.client.put('/api/v1/module/1/', data)
        self.assertEqual(resp.status_code, 200)
        resp = resp.json()
        # check data result
        module = Module.objects.get(id=1)
        self.assertEqual(resp["id"], module.id)
        self.assertEqual(resp["course"], module.course.id )
        self.assertEqual(resp["title"], module.title)
        self.assertEqual(resp["description"], module.description)
        # check change content
        payload = json.dumps({
            "contents": [
                {
                    "id": 1
                },
                {
                    "id": 3
                }
            ],
            "title": "it's postmanq3",
            "course" : self.course.id,
            "description": "it's over",
        })
        resp = self.client.put('/api/v1/module/1/', data=payload, content_type='application/json')
        resp = resp.json()
        # check length of contents
        self.assertEqual(len(resp["contents_url"]), 2)
        # check data result
        module = Module.objects.get(id=1)
        self.assertEqual(resp["id"], module.id)
        self.assertEqual(resp["course"], module.course.id )
        self.assertEqual(resp["title"], module.title)
        self.assertEqual(resp["description"], module.description)

        # logout admin user
        self.client.credentials()
        # login not admin user
        auth_endpoint = "/api/v1/token/"
        data = { "email" : "test2@gmail.com", "password" : "password"}
        auth_response = self.client.post(auth_endpoint, data)
        token = auth_response.json()['access']  
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
            "course" : self.course.id,
            "title" : "change title2",
            "description" : "it's description2"
         }
        resp = self.client.put('/api/v1/module/1/', data)
        # 403 --> indicates that the server understands the request but refuses to authorize it
        self.assertEqual(resp.status_code, 403)
        # logout not admin user
        self.client.credentials()
        resp = self.client.put('/api/v1/course/1/', data)
        self.assertEqual(resp.status_code, 403)
            
    def test_module_partial_update(self):
        data = {
                "title" : "hello partial",
            }
        resp = self.client.patch('/api/v1/course/1/', data)
        self.assertEqual(resp.status_code, 200)

    def test_content_delete(self):
        # not found 
        resp = self.client.delete('/api/v1/module/1000038945/')
        self.assertEqual(resp.status_code, 404)
        # delete object
        resp = self.client.delete('/api/v1/module/1/')
        self.assertEqual(resp.status_code, 204)
        # logout admin user
        self.client.credentials()
        resp = self.client.delete('/api/v1/module/2/')
        self.assertEqual(resp.status_code, 403)    

    def test_content_list(self):
        # get modules
        id = 1
        resp = self.client.get(f'/api/v1/module/{id}/')
        self.assertEqual(resp.status_code, 200)
        results = resp.json()['contents_url']
        self.assertEqual(len(results), 3)
        # check results
        for url in results:
            resp = self.client.get(url).json()
            content = Content.objects.get(id=resp['id'])
            self.assertEqual(resp['id'], content.id)
            self.assertEqual(resp['module'], content.module.id)
            self.assertEqual(resp['object_id'], content.object_id)
            self.assertEqual(resp['order'], content.order)

        # change content
         
        data = json.dumps({
            "contents": [
                {"id" : 1},
                {"id" : 3}
            ]
        })
        resp = self.client.patch(f'/api/v1/module/{id}/', data=data, content_type='application/json')
        self.assertEqual(resp.json()['contents_url'],  ['http://testserver/api/v1/content/1/' , 'http://testserver/api/v1/content/3/'])

