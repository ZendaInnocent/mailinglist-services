from accounts.forms import UserCreationForm


def test_invalid_user_registration_form():
    form = UserCreationForm(
        {
            'email': 'testuser2@test.com',
            'name': 'Test User',
            'password1': 'hoonoruru',
        }
    )

    assert not form.is_valid()


def test_arise_password_dont_match():
    form = UserCreationForm(
        {
            'email': 'testuser@test.com',
            'name': 'Test User',
            'password1': 'hoonoruru',
            'password2': 'hoonodruru',
        }
    )

    assert not form.is_valid()
