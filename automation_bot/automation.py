from rest_framework.response import Response
import requests
import environ
import uuid
from user.models import User
from social.models import Post, Like
from rest_framework.authtoken.models import Token

env = environ.Env()
env.read_env('.env')
number_of_users = env.int("NUMBER_OF_USERS")
max_posts_per_user = env.int("MAX_POSTS_PER_USER")
max_likes_per_user = env.int("MAX_LIKES_PER_USER")


class UserBot:

    def user_create(self):
        signup_res = None
        for _ in range(number_of_users):
            uid = uuid.uuid4()
            signup_body = {"username": f"test-{uid}", "email": f"test{uid}@gmail.com", "first_name": f"test-{uid}",
                           "last_name": f"test-{uid}", "password": "String123@"
                           }
            signup_headers = {"accepts": "Accept: application/json"}
            signup_url = "http://127.0.0.1:8000/api/v1/signup/"
            signup_res = requests.post(signup_url, json=signup_body, headers=signup_headers)
        return signup_res.json()

    def user_login(self):
        get_user = self.user_create()
        user = User.objects.get(id=get_user.get("id"))
        login_url = "http://127.0.0.1:8000/api/v1/login/"
        login_body = {'username': user.email, "password": "String123@"}
        login_header = {"accepts": "Accept: application/json"}
        login_res = requests.post(login_url, json=login_body, headers=login_header)
        return login_res.json()

    def create_post(self):
        post_res = None
        login_user = self.user_login()
        user = Token.objects.get(key=login_user.get("token")).user
        for _ in range(max_posts_per_user):
            post_url = "http://127.0.0.1:8000/api/v1/post/"
            post_body = {"user": user.id, "title": "test", "content": "content"}
            post_header = {"Authorization": f"Token {login_user.get('token')}", "accepts": "Accept: application/json"}
            post_res = requests.post(post_url, json=post_body, headers=post_header)
        return post_res.json()

    def like_post(self):
        login_user = self.user_login()
        user = Token.objects.get(key=login_user.get("token")).user
        post = self.create_post()
        for _ in range(max_likes_per_user):
            like_url = "http://127.0.0.1:8000/api/v1/like/"
            post_body = {"user": user.id, "post": post.get("id")}
            post_header = {"Authorization": f"Token {login_user.get('token')}", "accepts": "Accept: application/json"}
            like_res = requests.post(like_url, json=post_body, headers=post_header)

    def particular_post_liked_cannot_like_his_own_post(self):
        for user in User.objects.all():
            for post in Post.objects.all():
                if Like.objects.filter(user=user, post=post):
                    continue
                else:
                    if Post.objects.filter(user=user):
                        continue
                    else:
                        instance = Like(user=user, post=post)
                        instance.save()
        return Response({"response": "All posts liked by user one time"})


user = UserBot()
user.create_post()
user.like_post()
user.particular_post_liked_cannot_like_his_own_post()
