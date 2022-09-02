from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer

from accounts.models import UserProfile

# override default serializer so that only the `plan` field is serialized,
# not the subscription_id field
class UserProfileSerializer(serializers.ModelSerializer):
    """Makes the `plan` attribute available"""

    class Meta:
        model = UserProfile
        fields = ("plan",)


class UserSerializer(UserDetailsSerializer):
    profile = UserProfileSerializer()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ("profile",)
