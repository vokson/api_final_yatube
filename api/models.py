from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Сообщество', max_length=200, blank=False, unique=True)
    # slug = models.SlugField(
    #     max_length=50, unique=True, null=False, blank=False
    # )
    # description = models.TextField('Описание', help_text='Дайте описание сообществу..')

    def __str__(self) -> str:
        return str(self.title)


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор', help_text='Выберите автора'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='posts', verbose_name='Сообщество', help_text='Выберите сообщество'
    )
    # image = models.ImageField(upload_to='posts/', null=True, blank=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        short_text = self.text[:10]
        author_name = str(self.author)
        return f'{author_name}: {short_text}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField('Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        short_text = self.text[:10]
        author_name = str(self.author)
        return f'{author_name}: {short_text}'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик', help_text='Кто подписывается?'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='Автор', help_text='На кого подписываются?'
    )

    class Meta:
        unique_together = ['user', 'following']

    def __str__(self) -> str:
        follower = self.user.username
        following = self.following.username
        return f'{follower} -> {following}'
