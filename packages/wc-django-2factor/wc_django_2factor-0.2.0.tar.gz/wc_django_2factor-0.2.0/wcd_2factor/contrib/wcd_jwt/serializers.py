from django.utils.translation import pgettext
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from wcd_2factor.confirmer import default_confirmer
from wcd_2factor.contrib.drf.fields import PrimaryKeyRelatedField
from wcd_2factor.models import ConfirmationState


class TwoFactorTokenObtainPairSerializer(TokenObtainPairSerializer):
    confirmer = default_confirmer
    confirmation_id = PrimaryKeyRelatedField(
        queryset=lambda self: (
            ConfirmationState.objects
            .filter(status=ConfirmationState.Status.CONFIRMED)
        ),
    )

    def validate(self, attrs):
        data = super().validate(attrs)
        two_factor_id = attrs['two_factor_id']
        state, confirmed = confirmer.check(two_factor_id)

        if not confirmed:
            raise ValidationError({
                'two_factor_id': pgettext('wcd_2factor', 'Wrong confirmation.'),
            })

        confirmer.use(state)
        self.state = state

        return data
