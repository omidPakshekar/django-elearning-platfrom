from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import *
import requests
from django.contrib.contenttypes.fields import ContentType

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
        # create another non admin 
        self.user3 = get_user_model().objects.create_user(
            username="test3", email="test3@gmail.com", password="password"
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
           Course.objects.create(
                title = "create with aghaye amir",
                slug = "title3",
                overview = "it's simple",
                owner = self.user2,
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

        
    # def test_course_create(self):
    #     data = {
    #         "title" : "create with aghaye omid",
    #         "slug" : "agha",
    #         "overview" : "it's simple man",
    #         "owner" : 1,
    #         "category" : 1,
    #         "students" : [2],
    #     }
    #     # create course
    #     resp = self.client.post('/api/v1/course/', data)
    #     # 201 -> created
    #     self.assertEqual(resp.status_code, 201)
    #     course_id = resp.json()['id']
    #     # get course to check that our data is correct or not
    #     course = Course.objects.get(pk=course_id)
    #     self.assertEqual(course.title, data['title'])
    #     self.assertEqual(course.slug, data['slug'])
    #     self.assertEqual(course.overview, data['overview'])
    #     self.assertEqual(course.owner.id, data['owner'])
    #     self.assertEqual(course.category.id, data['category'])
    #     self.assertEqual(course.students.count(), 1)

    # def test_course_creation_unauthorized(self):
    #     # logout
    #     self.client.credentials()
    #     data = {
    #         "title" : "unathorized",
    #         "slug" : "unathorized2",
    #         "overview" : "it's simple man",
    #         "owner" : 1,
    #         "category" : 1,
    #         "students" : [2],
    #     }
    #     # create course
    #     resp = self.client.post('/api/v1/course/', data)
    #     # 403 -> unathorized
    #     self.assertEqual(resp.status_code, 403)
        

    # def test_course_list(self):
    #     # get courses
    #     resp = self.client.get('/api/v1/course/')
    #     self.assertEqual(resp.status_code, 200)
    #     results = resp.json()['results']
    #     # check size of course that we get
    #     self.assertEqual(len(results), 3)
    #     for course_dict in results:
    #         course = self.course_lookup[course_dict["id"]]
    #         self.assertEqual(course.title, course_dict['title'])
    #         self.assertEqual(course.slug, course_dict['slug'])
    #         self.assertEqual(course.overview, course_dict['overview'])
    #         self.assertEqual(course.owner.id, course_dict['owner'])
    #         self.assertEqual(course.category.id, course_dict['category'])
                    
    # def test_course_update(self):
    #     data = {
    #             "title" : "hello world",
    #             "slug" : "title1",
    #             "overview" : "it's title",
    #             "owner" : 1,
    #             "category" : 2,
    #             "students" : [2],
    #     }
    #     resp = self.client.put('/api/v1/course/1/', data)
    #     self.assertEqual(resp.status_code, 200)
    #     # logout admin user
    #     self.client.credentials()
    #     # login not admin user
    #     auth_endpoint = "/api/v1/token/"
    #     data = { "email" : "test2@gmail.com", "password" : "password"}
    #     auth_response = self.client.post(auth_endpoint, data)
    #     token = auth_response.json()['access']  
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    #     data = {
    #             "title" : "hello2",
    #             "slug" : "title1",
    #             "overview" : "it's title",
    #             "owner" : 1,
    #             "category" : 2,
    #             "students" : [2],
    #     }
    #     resp = self.client.put('/api/v1/course/1/', data)
    #     # only admin, staff and owner can update
    #     self.assertEqual(resp.status_code, 403)
    #     # logout admin user
    #     self.client.credentials()
    #     resp = self.client.put('/api/v1/course/1/', data)
    #     self.assertEqual(resp.status_code, 403)
            
    # def test_course_partial_update(self):
    #     data = {
    #             "title" : "hello partial",
    #         }
    #     resp = self.client.patch('/api/v1/course/1/', data)
    #     self.assertEqual(resp.status_code, 200)

    # def test_course_owner_list(self):
    #     # get course that we are owner of that course
    #     resp = self.client.get('/api/v1/course/mine/')
    #     self.assertEqual(resp.status_code, 200)
    #     results = resp.json()
    #     self.assertEqual(len(results), 2)
    #     for course_dict in results:
    #         course = self.course_lookup[course_dict["id"]]
    #         self.assertEqual(course.title, course_dict['title'])
    #         self.assertEqual(course.slug, course_dict['slug'])
    #         self.assertEqual(course.overview, course_dict['overview'])
    #         self.assertEqual(course.owner.email, course_dict['owner']['email'])
    #         self.assertEqual(course.category.id, course_dict['category'])

    # def test_course_students(self):
    #     # get course that we are joined
    #     # logout admin user
    #     self.client.credentials()
    #     # login not admin user
    #     auth_endpoint = "/api/v1/token/"
    #     data = { "email" : "test2@gmail.com", "password" : "password"}
    #     auth_response = self.client.post(auth_endpoint, data)
    #     token = auth_response.json()['access']  
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    #     resp = self.client.get('/api/v1/course/students/')
    #     results = resp.json()
    #     self.assertEqual(len(results), 1)
    #     course = Course.objects.get(id=1)
    #     self.assertEqual(course.id, results[0]['id'] )
    #     self.assertEqual(course.title, results[0]['title'] )
    #     self.assertEqual(course.overview, results[0]['overview'] )
    #     self.assertEqual(course.owner.email, results[0]['owner']['email'])
    
    # def test_course_delete(self):
    #     # not found 
    #     resp = self.client.delete('/api/v1/course/1000038945/')
    #     self.assertEqual(resp.status_code, 404)
    #     # delete object
    #     resp = self.client.delete('/api/v1/course/1/')
    #     self.assertEqual(resp.status_code, 204)
    #     # logout admin user
    #     self.client.credentials()
    #     resp = self.client.delete('/api/v1/course/2/')
    #     self.assertEqual(resp.status_code, 403)



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

        self.text = Text.objects.create(owner=self.user, title='title one', content='thtis is text')
        self.content_list = [
            Content.objects.create(module=module_list[0], content_type=ContentType.objects.get(model='text'), object_id=1)
        ]
        
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
        # get course id to find it's module
        id = self.course.id
        # get courses
        resp = self.client.get(f'/api/v1/course/{id}/')
        self.assertEqual(resp.status_code, 200)
        results = resp.json()
        # check size of module that we get
        self.assertEqual(len(results['modules_url']), 2)
        for url in results['modules_url']:
            resp = self.client.get(url).json()
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
            
    def test_course_partial_update(self):
        data = {
                "title" : "hello partial",
            }
        resp = self.client.patch('/api/v1/course/1/', data)
        self.assertEqual(resp.status_code, 200)










