from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBoardOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user == obj.owner or user in obj.members.all()

class IsTaskBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user in obj.board.members.all() or user == obj.board.owner

class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
