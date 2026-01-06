from rest_framework import serializers
from .models import Internship, SubjectType, ToolsType, StipendType, ProjectType
import boto3
from django.conf import settings


class SubjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectType
        fields = ['id', 'name']


class ToolsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolsType
        fields = ['id', 'name']


class StipendTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StipendType
        fields = ['id', 'name']


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ['id', 'name']


class InternshipSerializer(serializers.ModelSerializer):
    subject_type = SubjectTypeSerializer(read_only=True)
    stipend_type = StipendTypeSerializer(read_only=True)
    project_type = ProjectTypeSerializer(read_only=True)
    tools_type = ToolsTypeSerializer(many=True, read_only=True)


    subject_type_id = serializers.PrimaryKeyRelatedField(
        queryset=SubjectType.objects.all(),
        source='subject_type',
        write_only=True
    )
    stipend_type_id = serializers.PrimaryKeyRelatedField(
        queryset=StipendType.objects.all(),
        source='stipend_type',
        write_only=True
    )
    project_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectType.objects.all(),
        source='project_type',
        write_only=True
    )
    tools_type_ids = serializers.PrimaryKeyRelatedField(
        queryset=ToolsType.objects.all(),
        source='tools_type',
        many=True,
        write_only=True
    )

    image = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = [
            'id', 'title', 'details', 'mode_type', 'working_hours',
            'office_location', 'duration',
            'start_date', 'end_date', 'certificate', 'mentorship','image','status',
            'subject_type', 'stipend_type', 'project_type', 'tools_type',
            'subject_type_id', 'stipend_type_id', 'project_type_id', 'tools_type_ids',
        ]


    def get_image(self, obj):
        if obj.image:
            s3 = boto3.client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': obj.image.name},
                ExpiresIn=3600  
            )
            return url
        return None
