from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate
from .models import User, Role, UserProfile, Organization, WellnessType

from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from .models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        mobile = validated_data["mobile"]
        password = validated_data["password"]

        # ❌ Username already exists
        if AuthUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "username": "Username already exists"
            })

        # ❌ Email already exists
        if AuthUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "email": "Email already registered"
            })

        # ❌ Mobile already exists (IMPORTANT 🔥)
        if User.objects.filter(mobile=mobile, is_delete=False).exists():
            raise serializers.ValidationError({
                "mobile": "Mobile number already registered"
            })

        # ✅ Create Auth user
        auth_user = AuthUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ✅ Create custom User with mobile
        User.objects.create(
            auth_user=auth_user,
            mobile=mobile
        )

        return auth_user



# ---------------- Login Serializer ----------------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        attrs['user'] = user
        return attrs
from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from .models import User as LernevoUser

class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        # If you add role later, update this
        return "Member"

    def update(self, instance, validated_data):
        auth_user = instance.auth_user

        if "username" in validated_data:
            auth_user.username = validated_data["username"]

        if "email" in validated_data:
            auth_user.email = validated_data["email"]

        auth_user.save()

        if "mobile" in validated_data:
            instance.mobile = validated_data["mobile"]
            instance.save()

        return instance
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["profile_image"]


from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["id", "created_at", "is_resolved"]

from .models import Enquiry
from rest_framework import serializers

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"


from .models import DemoBooking
from rest_framework import serializers

class DemoBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoBooking
        fields = "__all__"




from rest_framework import serializers
from .models import *

# ---------------- SIMPLE SERIALIZERS ----------------

class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumePersonalInfo
        exclude = ['resume']
        extra_kwargs = {field: {'required': False, 'allow_blank': True, 'allow_null': True}
                        for field in ['full_name','job_title','email','phone','location','linkedin','github','photo']}


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeSummary
        exclude = ['resume']
        extra_kwargs = {
            'text': {'required': False, 'allow_blank': True, 'allow_null': True}
        }


class ExperienceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ResumeExperience
        exclude = ['resume']
        extra_kwargs = {field: {'required': False, 'allow_blank': True, 'allow_null': True}
                        for field in ['company','role','duration','location','description']}


class UGEducationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    graduatedYear = serializers.CharField(
        source='graduated_year',
        required=False,
        allow_blank=True
    )

    class Meta:
        model = ResumeUGEducation
        exclude = ['resume']
        extra_kwargs = {field: {'required': False, 'allow_blank': True, 'allow_null': True}
                        for field in ['college','degree','branch','graduated_year','gpa','highlights']}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['graduatedYear'] = data.pop('graduated_year', '')
        return data


class SchoolEducationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    schoolName = serializers.CharField(source='school_name', required=False, allow_blank=True)
    passingYear = serializers.CharField(source='passing_year', required=False, allow_blank=True)

    class Meta:
        model = ResumeSchoolEducation
        exclude = ['resume']
        extra_kwargs = {field: {'required': False, 'allow_blank': True, 'allow_null': True}
                        for field in ['school_name','board','stream','passing_year','percentage','highlights']}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['schoolName'] = data.pop('school_name', '')
        data['passingYear'] = data.pop('passing_year', '')
        return data


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ResumeSkill
        exclude = ['resume']
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True, 'allow_null': True},
            'level': {'required': False, 'allow_null': True},
            'badge': {'required': False, 'allow_blank': True, 'allow_null': True},
        }


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ResumeProject
        exclude = ['resume']
        extra_kwargs = {field: {'required': False, 'allow_blank': True, 'allow_null': True}
                        for field in ['name','tech','description','link','date']}


class CertificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ResumeCertification
        exclude = ['resume']
        extra_kwargs = {field: {'required': False, 'allow_blank': True, 'allow_null': True}
                        for field in ['name','issuer','date','credential_id','description']}


class LanguageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ResumeLanguage
        exclude = ['resume']
        extra_kwargs = {
            'language': {'required': False, 'allow_blank': True, 'allow_null': True},
            'proficiency': {'required': False, 'allow_blank': True, 'allow_null': True},
            'stars': {'required': False, 'allow_null': True},
        }


class OptionalSectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ResumeOptionalSection
        exclude = ['resume']
        extra_kwargs = {
            'title': {'required': False, 'allow_blank': True, 'allow_null': True},
            'content': {'required': False, 'allow_blank': True, 'allow_null': True},
        }


# ---------------- MAIN SERIALIZER ----------------

class ResumeSerializer(serializers.ModelSerializer):

    personal_info = PersonalInfoSerializer(required=False)
    summary = SummarySerializer(required=False)

    experiences = ExperienceSerializer(many=True, required=False)
    ug_education = UGEducationSerializer(many=True, required=False)
    school_education = SchoolEducationSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    certifications = CertificationSerializer(many=True, required=False)
    languages = LanguageSerializer(many=True, required=False)
    optional_sections = OptionalSectionSerializer(many=True, required=False)

    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['user']

    # 🔥 CLEAN EMPTY DATA
    def clean_items(self, items):
        clean = []
        for item in items:
            item.pop('id', None)
            item = {k: v for k, v in item.items() if v not in ["", None]}
            if item:
                clean.append(item)
        return clean

    # 🔥 CREATE
    def create(self, validated_data):

        user = validated_data.pop('user', None)
        if not user:
            raise serializers.ValidationError("User is required")

        personal_data = validated_data.pop('personal_info', None)
        summary_data = validated_data.pop('summary', None)

        exp_data = self.clean_items(validated_data.pop('experiences', []))
        ug_data = self.clean_items(validated_data.pop('ug_education', []))
        school_data = self.clean_items(validated_data.pop('school_education', []))
        skill_data = self.clean_items(validated_data.pop('skills', []))
        proj_data = self.clean_items(validated_data.pop('projects', []))
        cert_data = self.clean_items(validated_data.pop('certifications', []))
        lang_data = self.clean_items(validated_data.pop('languages', []))
        optional_data = self.clean_items(validated_data.pop('optional_sections', []))

        resume = Resume.objects.create(user=user, **validated_data)

        if personal_data:
            ResumePersonalInfo.objects.create(resume=resume, **personal_data)

        if summary_data:
            ResumeSummary.objects.create(resume=resume, **summary_data)

        for item in exp_data:
            ResumeExperience.objects.create(resume=resume, **item)

        for item in ug_data:
            ResumeUGEducation.objects.create(resume=resume, **item)

        for item in school_data:
            ResumeSchoolEducation.objects.create(resume=resume, **item)

        for item in skill_data:
            ResumeSkill.objects.create(resume=resume, **item)

        for item in proj_data:
            ResumeProject.objects.create(resume=resume, **item)

        for item in cert_data:
            ResumeCertification.objects.create(resume=resume, **item)

        for item in lang_data:
            ResumeLanguage.objects.create(resume=resume, **item)

        for item in optional_data:
            ResumeOptionalSection.objects.create(resume=resume, **item)

        return resume

    # 🔥 UPDATE (FINAL FIX)
    def update(self, instance, validated_data):

        validated_data.pop('user', None)

        personal_data = validated_data.pop('personal_info', None)
        summary_data = validated_data.pop('summary', None)

        exp_data = self.clean_items(validated_data.pop('experiences', []))
        ug_data = self.clean_items(validated_data.pop('ug_education', []))
        school_data = self.clean_items(validated_data.pop('school_education', []))
        skill_data = self.clean_items(validated_data.pop('skills', []))
        proj_data = self.clean_items(validated_data.pop('projects', []))
        cert_data = self.clean_items(validated_data.pop('certifications', []))
        lang_data = self.clean_items(validated_data.pop('languages', []))
        optional_data = self.clean_items(validated_data.pop('optional_sections', []))

        # UPDATE MAIN
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # PERSONAL INFO
        if personal_data is not None:
            ResumePersonalInfo.objects.update_or_create(
                resume=instance,
                defaults=personal_data
            )

        # SUMMARY
        if summary_data is not None:
            ResumeSummary.objects.update_or_create(
                resume=instance,
                defaults=summary_data
            )

        # REPLACE FUNCTION
        def replace(model, items):
            model.objects.filter(resume=instance).delete()
            for item in items:
                model.objects.create(resume=instance, **item)

        replace(ResumeExperience, exp_data)
        replace(ResumeUGEducation, ug_data)
        replace(ResumeSchoolEducation, school_data)
        replace(ResumeSkill, skill_data)
        replace(ResumeProject, proj_data)
        replace(ResumeCertification, cert_data)
        replace(ResumeLanguage, lang_data)
        replace(ResumeOptionalSection, optional_data)

        return instance