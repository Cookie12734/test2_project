from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
# Create your models here.

class Category(models.Model):
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20)
    
    def __str__(self):
        return self.title

class Test2News(models.Model):
    
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
        )
    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリー',
        on_delete=models.PROTECT
        )
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
        )
    post = models.TextField(
        verbose_name='記事本文',
        default=""

    )
    image1 = models.ImageField(
        verbose_name='タイトル画像',
        upload_to = 'photos',
        blank = True,
        null = True,
        )
    
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add = True
        )

    updated_at = models.DateTimeField(
        verbose_name='更新日時',
        null=True,
        blank=True,
        help_text='編集が行われた場合にセットされます。'
    )

    def save(self, *args, **kwargs):

        if self.pk:
            try:
                orig = Test2News.objects.get(pk=self.pk)
            except Test2News.DoesNotExist:
                orig = None
            changed = False
            if orig:
                fields_to_check = ['title', 'post', 'image1_id', 'category_id']
                for f in fields_to_check:
                    if getattr(orig, f, None) != getattr(self, f, None):
                        changed = True
                        break
            if changed:
                self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Test2News,
        verbose_name="対象記事",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name="ユーザー",
        on_delete=models.CASCADE
    )
    text = models.CharField(
        verbose_name="コメント",
        max_length=300
    )
    created_at = models.DateTimeField(
        verbose_name="作成日時",
        auto_now_add=True
    )

