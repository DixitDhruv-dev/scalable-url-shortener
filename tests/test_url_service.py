from app.services.url_service import generate_short_code


def test_generate_short_code_length():
    code = generate_short_code()

    assert len(code) == 7
    assert code.isalnum()