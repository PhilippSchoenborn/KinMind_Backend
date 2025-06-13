from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from kanban_app.models import Board, Task, Comment
from .serializers import (
    BoardSerializer, BoardDetailSerializer, TaskSerializer, CommentSerializer
)
from .permissions import IsBoardOwnerOrMember, IsTaskBoardMember, IsCommentAuthor
from django.contrib.auth import get_user_model

User = get_user_model()

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Nur Boards, bei denen der User Owner oder Member ist, ohne Duplikate
        return Board.objects.filter(members=user).union(Board.objects.filter(owner=user)).distinct()

    def retrieve(self, request, *args, **kwargs):
        try:
            board = self.get_queryset().get(pk=kwargs['pk'])
        except Board.DoesNotExist:
            return Response({'detail': 'Board not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Permission check
        if not (request.user == board.owner or request.user in board.members.all()):
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardDetailSerializer
        return BoardSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        board = Board.objects.create(title=data['title'], owner=request.user)
        member_ids = data.get('members', [])
        if request.user.id not in member_ids:
            member_ids.append(request.user.id)
        board.members.set(User.objects.filter(id__in=member_ids))
        board.save()
        out_serializer = self.get_serializer(board)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        board = self.get_object()
        self.check_object_permissions(request, board)
        title = request.data.get('title', board.title)
        members = request.data.get('members', None)
        if members is not None:
            board.members.set(User.objects.filter(id__in=members))
        board.title = title
        board.save()
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        board = self.get_object()
        if board.owner != request.user:
            return Response({'detail': 'Only the owner can delete this board.'}, status=status.HTTP_403_FORBIDDEN)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskBoardMember]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'assigned_to_me':
            return Task.objects.filter(assignee=user)
        if self.action == 'reviewing':
            return Task.objects.filter(reviewer=user)
        return Task.objects.filter(board__members=user) | Task.objects.filter(board__owner=user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        board = get_object_or_404(Board, id=data['board'])
        if request.user not in board.members.all() and request.user != board.owner:
            return Response({'detail': 'Not a board member.'}, status=status.HTTP_403_FORBIDDEN)
        assignee = data.get('assignee_id')
        reviewer = data.get('reviewer_id')
        task = Task.objects.create(
            board=board,
            title=data['title'],
            description=data.get('description', ''),
            status=data['status'],
            priority=data['priority'],
            assignee=User.objects.filter(id=assignee).first() if assignee else None,
            reviewer=User.objects.filter(id=reviewer).first() if reviewer else None,
            due_date=data.get('due_date'),
            created_by=request.user
        )
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        self.check_object_permissions(request, task)
        for field in ['title', 'description', 'status', 'priority', 'due_date']:
            if field in request.data:
                setattr(task, field, request.data[field])
        assignee_id = request.data.get('assignee_id')
        reviewer_id = request.data.get('reviewer_id')
        if assignee_id:
            task.assignee = User.objects.filter(id=assignee_id).first()
        if reviewer_id:
            task.reviewer = User.objects.filter(id=reviewer_id).first()
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.created_by != request.user and task.board.owner != request.user:
            return Response({'detail': 'Only the creator or board owner can delete this task.'}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssignedToMeTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

class ReviewingTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsTaskBoardMember]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        serializer.save(author=self.request.user, task=task)

class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id)
