from pytest_django.asserts import assertRaisesMessage

from accounts.models import User


def test_can_save_users(client):
    User.objects.create_user(
        email='test1@user.com',
        name='test user 1',
        password='helootheree',
    )
    User.objects.create_user(
        email='test2@user.com',
        name='test user 2',
        password='helootheree',
    )

    users = User.objects.all()

    assert len(users) == 2


def test_raise_message_when_create_user_with_invalid_email():
    assertRaisesMessage(
        ValueError,
        'Users must have an email address',
        User.objects.create_user,
        email='',
        name='odsif',
    )


def test_user_string_representation():
    user = User.objects.create(
        email='some@web.com', name='Someone', password='odufsohdof'
    )

    assert str(user) == user.email


def test_staff_property_for_non_superuser():
    user = User.objects.create_user(
        email='test@user.com',
        name='test user',
    )

    assert not user.is_staff


def test_staff_property():
    superuser = User.objects.create_superuser(
        email='superuser@admin.com', name='super user'
    )
    assert superuser.is_staff
