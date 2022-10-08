from rest_framework import serializers
from ..models.comments import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coment
        fields = ['id', 'user', 'youtube_vid_id', 'text', 'date']