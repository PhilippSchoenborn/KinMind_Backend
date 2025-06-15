# Standardbibliothek
# (keine)

# Drittanbieter
from rest_framework import serializers

# Lokale Importe
from kanban_app.models import Board, Task, Comment
from django.contrib.auth import get_user_model


User = get_user_model()


class BoardMemberSerializer(serializers.ModelSerializer):
    """Serializer for board members (user info)."""

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for board list view with summary fields."""
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'owner_id', 'member_count', 'ticket_count',
            'tasks_to_do_count', 'tasks_high_prio_count'
        ]

    def get_member_count(self, obj):
        """Return the number of members in the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Return the number of tasks in the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Return the number of 'to-do' tasks in the board."""
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Return the number of high priority tasks in the board."""
        return obj.tasks.filter(priority='high').count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """Serializer for board detail view with members and tasks."""
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = BoardMemberSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']

    def get_tasks(self, obj):
        """Return serialized tasks for the board."""
        return TaskSerializer(obj.tasks.all(), many=True).data


class TaskUserSerializer(serializers.ModelSerializer):
    """Serializer for user info in tasks (assignee/reviewer)."""

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks with assignee, reviewer, board id, and comment count."""
    assignee = TaskUserSerializer(read_only=True)
    reviewer = TaskUserSerializer(read_only=True)
    board = serializers.IntegerField(source='board.id', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        """Return the number of comments for the task."""
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments with author name."""
    author = serializers.CharField(source='author.fullname', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
