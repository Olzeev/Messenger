from django.db import models
from django.utils import timezone

class User_blocked(models.Model):
    user_id = models.CharField(max_length=10)
    id_user_blocked = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user_id}->{self.id_user_blocked}"
    
    class Meta:
        verbose_name = "User blocked"
        verbose_name_plural = "Users blocked"


class Message(models.Model):
    id_sender = models.CharField(max_length=10)
    id_reciever = models.CharField(max_length=10)
    text = models.TextField(default='')
    time = models.DateField(default=timezone.now())
    attached_file = models.FileField(default='')

    def __str__(self):
        return f"{self.id_sender}->{self.id_reciever}, {self.time}"
    

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class User_info(models.Model):
    user_info_id = models.CharField(max_length=10)
    avatar = models.ImageField(upload_to=f'user_avatars/', default='user_avatars/default/default_avatar.jpg')
    status = models.TextField(default='')
    last_online_time = models.DateField(default=timezone.now())

    def __str__(self):
        return f"{self.user_info_id}"
    
    class Meta:
        verbose_name = "User info"
        verbose_name_plural = "Users' info"


class Group(models.Model):
    group_id = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    #avatar = models.FileField()
    description = models.TextField(default='')

    def __str__(self):
        return f"{self.group_id} ({self.name})"
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Group_ref(models.Model):
    group_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.group_id}->{self.user_id}"
    

    class Meta:
        verbose_name = 'Group reference'
        verbose_name_plural = 'Group references'


