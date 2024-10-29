from django.db import models
from django.contrib.auth.models import User 

class Story(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    image = models.ImageField(upload_to='story_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Contribution(models.Model):
    text = models.TextField()    
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='contributions', null=True, blank=True)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions', null=True, blank=True)
    contributed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contributor.username}'s contribution to {self.story.title}" if self.contributor else f"Anonymous contribution to {self.story.title}"