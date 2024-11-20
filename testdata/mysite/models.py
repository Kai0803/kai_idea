from django.db import models

# Create your models here.
class Post(models.Model):     
    title = models.CharField(max_length=100) #紀錄文章的標題   屬性為字元
    slug = models.CharField(max_length=100) #連結本文章的網址  屬性為字元
    body = models.TextField() #紀錄文章的內容
    pub_date = models.DateTimeField(auto_now_add = True) #aut_now_add 表示自動加入系統時間
    class Meta:
        ordering = ('-pub_date',)
        
    def __str__(self):
        return self.title
