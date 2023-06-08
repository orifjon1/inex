from .models import Task, TaskReview
from datetime import date
from user.serializer import UserProfileSerializer

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class TaskSerializer(serializers.ModelSerializer):
    boss = serializers.ReadOnlyField(source='boss.username')
    name = serializers.ReadOnlyField(source='employee.first_name')
    last_name = serializers.ReadOnlyField(source='employee.last_name')
    remain_days = serializers.SerializerMethodField()
    all_days = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'problem', 'reason', 'event',
                  'deadline', 'boss', 'employee', 'name', 'last_name',
                  'remain_days', 'all_days', 'status',
                  'financial_help', 'created_at', 'updated', 'is_active'
                  ]
        read_only_fields = ('status', 'created_at', 'updated', 'financial_help', 'is_active')

    def validate_employee(self, value):
        boss = self.context['request'].user
        if boss and boss.status == 'manager' and value and value.sector != boss.sector:
            raise ValidationError(
                {
                    'status': False,
                    'message': 'Bunday xodim sizning bo\'limingizda mavjud emas!'
                }
            )
        return value

    def validate_deadline(self, value):
        if value <= date.today():
            raise ValidationError(
                {
                    'status': False,
                    'message': 'Topshiriq Muddati - bugungi sanadan keyingi sana bo\'lishi kerak!'
                })
        return value

    def get_remain_days(self, obj):
        return obj.remain_days

    def get_all_days(self, obj):
        return obj.all_days


class TaskReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = TaskReview
        fields = ['content', 'created', 'user']
        read_only_fields = ('user', 'created')

    def validate(self, attrs):
        content = attrs.get('content', None)
        if content == '':
            raise ValidationError(
                {
                    'status': False,
                    'message': 'Izoh yo\'q'
                }
            )
        else:
            return attrs
