from django.contrib import admin
from .models import Board, Task, Comment

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
    search_fields = ('title',)
    filter_horizontal = ('members',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'board', 'status', 'priority', 'assignee', 'reviewer', 'due_date')
    search_fields = ('title',)
    list_filter = ('status', 'priority', 'board')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'author', 'created_at')
    search_fields = ('content',)
    list_filter = ('task', 'author')
