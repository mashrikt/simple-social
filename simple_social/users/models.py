from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer."
        ),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_email_verified = models.BooleanField(
        _("email verified"),
        null=True,
        help_text=_(
            "Designates whether this user has a valid email address."
        ),
    )
    is_date_joined_local_holiday = models.BooleanField(
        _("date joined local holiday"),
        null=True,
        help_text=_(
            "Designates whether it was a local holiday on the day the user signed up."
        ),
    )
    registration_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text=_(
            "Designates the IP address of the user during sign up."
        ),
    )
    is_registration_ip_routable = models.BooleanField(blank=True, null=True)
    location_data = models.JSONField(blank=True, default=dict)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        pass

    def validate_email(self):
        from .tasks import validate_email
        validate_email.delay(self.email)

    def enhance_geolocation(self):
        # The two tasks are chained. get_user_location_data will run first and then after completion
        # has_user_registered_on_a_holiday will run
        from .tasks import get_user_location_data, has_user_registered_on_a_holiday
        (get_user_location_data.si(self.email) | has_user_registered_on_a_holiday.si(self.email)).delay()
