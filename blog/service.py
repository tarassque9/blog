from .models import User, Follower, Post
from .tasks import send_post_notification


def get_user_followers_emails(user_id: int) -> list:
    following_objects = Follower.objects.filter(following_id=user_id)
    return [User.objects.get(id=el.following_id).email for el in following_objects]


def get_user_following_objects(user_id: int) -> list:
    following_objects = Follower.objects.filter(follower_id=user_id)
    return [User.objects.get(id=obj.following_id) for obj in following_objects]


def get_user_followers_objects(user_id: int) -> list:
    follower_objects = Follower.objects.filter(following_id=user_id)
    return [User.objects.get(id=obj.follower_id) for obj in follower_objects]


def get_user_posts(user_id):
    following_objects = get_user_following_objects(user_id)
    post_users_id = [obj.id for obj in following_objects]
    res = []
    for id in post_users_id:
        try:
            post = Post.objects.get(author_name_id=id)
            res.append(post)
        except Post.DoesNotExist:
            continue
    return res


def save_post(post_obj) -> bool:
    if post_obj:
        post_obj.save()
        post_link = f'http://127.0.0.1:8000/post_detail/{post_obj.id}'
        emails_list = get_user_followers_emails(post_obj.id)
        if emails_list:
            #send_post_notification(emails_list, post_link)
            return True
    return False


def follow_unfollow(follower_user_id: int, following_user_id: int) -> bool:
    try:
        """ unfollow """
        obj = Follower.objects.get(follower_id=follower_user_id, 
                                   following_id=following_user_id)
        obj.delete()
        return False
    except Follower.DoesNotExist:
        """ follow """
        obj = obj = Follower(follower_id=follower_user_id, 
                             following_id=following_user_id)
        obj.save()
        return True
