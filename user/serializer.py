import re
import string
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.text import gettext_lazy as _

from .models import CustomUser, Sector
from rest_framework import serializers


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name']

    def validate_name(self, name):
        if name != '':
            name = name.capitalize()
            return name
        else:
            raise ValidationError(
                {
                    'status': False,
                    'message': f'Bo\'lim nomi to\'ldirilishi shart ! '
                }
            )


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'sector', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super(UserSignUpSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        username = attrs.get('username', None)
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(
                {
                    'status': False,
                    'message': f'{username} - boshqa foydalanuvchi tomonidan foydalanilgan \n'
                               f' boshqa username kiriting !'
                }
            )
        return attrs

    def validate_username(self, username):
        if username != '':
            username = username.lower()
            return username
        else:
            raise ValidationError(
                {
                    'status': False,
                    'message': f'username to\'ldirilishi shart ! '
                }
            )


class UserProfileSerializer(serializers.ModelSerializer):
    total_workers = serializers.SerializerMethodField(read_only=True)
    sector_boss = serializers.SerializerMethodField(read_only=True)
    boss = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'sector', 'status',
            'first_name', 'last_name', 'email',
            'shior', 'main_task', 'birth_date',
            'phone_number', 'boss', 'sector_boss', 'photo',
            'total_workers'
        ]
        extra_kwargs = {'sector': {'read_only': True}, 'status': {'read_only': True}}

    def to_representation(self, instance):
        data = super(UserProfileSerializer, self).to_representation(instance)
        data['total_workers'] = self.get_total_workers(instance)
        data['boss'] = str(self.get_boss(instance))
        data['sector_boss'] = str(self.get_sector_boss(instance))
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.main_task = validated_data.get('main_task', instance.main_task).capitalize()
        instance.shior = validated_data.get('shior', instance.shior).capitalize()
        instance.first_name = validated_data.get('first_name', instance.first_name).capitalize()
        instance.last_name = validated_data.get('last_name', instance.last_name).capitalize()
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance

    def validate(self, attrs):
        username = attrs.get('username', None)
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(
                {
                    'status': False,
                    'message': f'{username} - boshqa foydalanuvchi tomonidan foydalanilgan \n'
                               f' boshqa username kiriting !'
                }
            )
        return attrs

    def validate_phone_number(self, value):
        value = self.phone(value)
        return value

    def phone(self, value):
        pattern = re.compile(r'^\+998\d{2}\d{3}\d{2}\d{2}$')
        value = "+998" + str(value)
        if re.fullmatch(pattern, value):
            return value
        else:
            raise ValidationError(
                {
                    'status': False,
                    'message': "Telefon raqam xato kiritildi!"
                }
            )

    def get_boss(self, obj):
        if obj.status == 'employee' or obj.status == 'manager':
            boss = CustomUser.objects.filter(status='director').first()
            return string.capwords(f'{boss.first_name} {boss.last_name}')
        else:
            return ' '

    def get_sector_boss(self, obj):
        if obj.status == 'employee':
            boss = CustomUser.objects.filter(Q(status='manager') & Q(sector=obj.sector)).first()
            return string.capwords(f'{boss.first_name} {boss.last_name}')
        return ' '

    def get_total_workers(self, obj):
        if obj.status == "manager":
            workers = CustomUser.objects.filter(Q(status='employee') & Q(sector=obj.sector))
            return workers.count()
        elif obj.status == "director":
            workers = CustomUser.objects.all().exclude(status='director')
            workers = workers.exclude(status='admin')
            return workers.count()
        else:
            return 0


class UserStatSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    doing = serializers.SerializerMethodField()
    finished = serializers.SerializerMethodField()
    canceled = serializers.SerializerMethodField()
    changed = serializers.SerializerMethodField()
    missed = serializers.SerializerMethodField()
    doing_percent = serializers.SerializerMethodField()
    missed_percent = serializers.SerializerMethodField()
    canceled_percent = serializers.SerializerMethodField()
    finished_percent = serializers.SerializerMethodField()
    changed_percent = serializers.SerializerMethodField()
    # sector = SectorSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'sector', 'status',
                  'total', 'doing', 'finished', 'canceled', 'missed', 'changed',
                  'doing_percent', 'missed_percent', 'finished_percent', 'canceled_percent', 'changed_percent']
        extra_kwargs = {'status': {'read_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total'] = self.get_total(instance)
        data['doing'] = self.get_doing(instance)
        data['finished'] = self.get_finished(instance)
        data['canceled'] = self.get_canceled(instance)
        data['changed'] = self.get_changed(instance)
        data['missed'] = self.get_missed(instance)
        data['doing_percent'] = self.get_doing_percent(instance)
        data['missed_percent'] = self.get_missed_percent(instance)
        data['canceled_percent'] = self.get_canceled_percent(instance)
        data['finished_percent'] = self.get_finished_percent(instance)
        data['changed_percent'] = self.get_finished_percent(instance)
        return data

    def get_total(self, obj):
        if obj.status != "director" and obj.status != 'admin':
            total = obj.accepted_tasks.all().count()
            return total
        return 0

    def get_doing(self, obj):
        if obj.status != "director" and obj.status != 'admin':
            done_tasks = obj.accepted_tasks.all()
            x = 0
            for i in done_tasks:
                if i.status == 'doing':
                    x += 1
            return x
        return 0

    def get_finished(self, obj):
        if obj.status != "director" and obj.status != 'admin':
            done_tasks = obj.accepted_tasks.all()
            x = 0
            for i in done_tasks:
                if i.status == 'finished':
                    x += 1
            return x
        return 0

    def get_canceled(self, obj):
        if obj.status != "director" and obj.status != 'admin':
            done_tasks = obj.accepted_tasks.all()
            x = 0
            for i in done_tasks:
                if i.status == 'canceled':
                    x += 1
            return x
        return 0

    def get_changed(self, obj):
        if obj.status != "director" and obj.status != 'admin':
            done_tasks = obj.accepted_tasks.all()
            x = 0
            for i in done_tasks:
                if i.is_changed:
                    x += 1
            return x
        return 0

    def get_missed(self, obj):
        if obj.status != "director" and obj.status != 'admin':
            done_tasks = obj.accepted_tasks.all()
            x = 0
            for i in done_tasks:
                if i.status == 'missed':
                    x += 1
            return x
        return 0

    def get_doing_percent(self, obj):
        total = self.get_total(obj)
        doing = self.get_doing(obj)
        if total != 0 and doing is not None:
            perc = (doing * 100.0) / total
            perc = round(perc, 2)
            return perc
        else:
            return 0

    def get_missed_percent(self, obj):
        total = self.get_total(obj)
        doing = self.get_missed(obj)
        if total != 0 and doing is not None:
            perc = (doing * 100.0) / total
            perc = round(perc, 2)
            return perc
        else:
            return 0

    def get_finished_percent(self, obj):
        total = self.get_total(obj)
        doing = self.get_finished(obj)
        if total != 0 and doing is not None:
            perc = (doing * 100.0) / total
            perc = round(perc, 2)
            return perc
        else:
            return 0

    def get_canceled_percent(self, obj):
        total = self.get_total(obj)
        doing = self.get_canceled(obj)
        if total != 0 and doing is not None:
            perc = (doing * 100.0) / total
            perc = round(perc, 2)
            return perc
        else:
            return 0

    def get_changed_percent(self, obj):
        total = self.get_total(obj)
        doing = self.get_changed(obj)
        if total != 0 and doing is not None:
            perc = (doing * 100.0) / total
            perc = round(perc, 2)
            return perc
        else:
            return 0
