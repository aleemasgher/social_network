from user.models import User
from social.models import Post, Like
from rest_framework.authtoken.models import Token

env = environ.Env()
env.read_env('.env')
number_of_users = env.int("NUMBER_OF_USERS")
max_posts_per_user = env.int("MAX_POSTS_PER_USER")
max_likes_per_user = env.int("MAX_LIKES_PER_USER")


class UserBot:

    def user_and_post_creation(self):
        for _ in range(number_of_users):
            uid = uuid.uuid4()
            signup_body = {"username": f"test-{uid}", "email": f"test{uid}@gmail.com", "first_name": f"test-{uid}",
                           "last_name": f"test-{uid}", "password": "String123@"
                           }
            signup_headers = {"accepts": "Accept: application/json"}
            signup_url = "http://127.0.0.1:8000/api/v1/signup/"
            signup_res = requests.post(signup_url, json=signup_body, headers=signup_headers)
            if signup_res:
                login_url = "http://127.0.0.1:8000/api/v1/login/"
                login_body = {'username': signup_res.json()['email'], "password": "String123@"}
                login_header = {"accepts": "Accept: application/json"}
                login_res = requests.post(login_url, json=login_body, headers=login_header)
                if login_res:
                    for _ in range(max_posts_per_user):
                        post_url = "http://127.0.0.1:8000/api/v1/post/"
                        post_body = {"user": signup_res.json()['id'], "title": "test", "content": "content"}
                        post_header = {"Authorization": f"Token {login_res.json()['token']}",
                                       "accepts": "Accept: application/json"}
                        post_res = requests.post(post_url, json=post_body, headers=post_header)
        return {"response": "Users and Posts are created"}

    def like_functionality(self):
        count = 0
        max_post_user = ""
        user_posts_without_like = []
        for user in User.objects.all():
            particular_user_post = Post.objects.filter(user=user).count()
            if particular_user_post:
                if particular_user_post > count:
                    count = particular_user_post
                    max_post_user = user
        user_token = Token.objects.get(user_id=max_post_user.id)
        for _ in range(max_likes_per_user):
            particular_user_like = Like.objects.filter(user=max_post_user).count
            if particular_user_like >= max_likes_per_user:
                break

            for post in Post.objects.all():
                like_url = "http://127.0.0.1:8000/api/v1/like/"
                post_body = {"user": max_post_user.id, "post": post.get("id")}
                post_header = {"Authorization": f"Token {user_token.key}", "accepts": "Accept: application/json"}
                like_res = requests.post(like_url, json=post_body, headers=post_header)
                if particular_user_like >= max_likes_per_user:
                    break

    def no_post_with_zero_like(self):
        for post in Post.objects.all():
            if not Like.objects.filter(post=post).first:
                self.like_functionality()



user = UserBot()
user.user_and_post_creation()
user.like_functionality()
user.no_post_with_zero_like()
