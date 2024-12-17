def test_create_random_password():
    from src.adapters.primary.auth.sign_up import create_random_password

    password = create_random_password()
    assert len(password) == 8
