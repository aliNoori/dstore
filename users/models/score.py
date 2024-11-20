from django.db import models
from users.models.customuser import CustomUser

class Score(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='userscores')
    score = models.IntegerField()
    reason = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.score} points for {self.user.username}"

    class Meta:
        verbose_name = "Score"
        verbose_name_plural = "Scores"
        ordering = ['-date_added']  # مرتب‌سازی بر اساس تاریخ ایجاد به ترتیب نزولی
