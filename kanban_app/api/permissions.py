# Standardbibliothek
# (keine)

# Drittanbieter
from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    """Permission: User must be board owner or member."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.owner or user in obj.members.all()


class IsTaskBoardMember(BasePermission):
    """Permission: User must be board owner or member for a task."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user in obj.board.members.all() or user == obj.board.owner


class IsCommentAuthor(BasePermission):
    """Permission: User must be the author of the comment."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
