PASSWORD_MESSAGES = {
    "password_too_common": "This password is too weak. Try something longer and less predictable.",
    "password_entirely_numeric": "This password is too weak. Add some letters.",
    "password_too_short": "This password is too weak. Use at least 8 characters.",
    "password_too_similar": "This password is too similar to your personal details.",
}


def password_error_messages(form, target="new_password1"):
    errors = {}
    for field, error_list in form.errors.as_data().items():
        for err in error_list:
            if err.code in PASSWORD_MESSAGES:
                errors.setdefault(target, PASSWORD_MESSAGES[err.code])
            else:
                errors.setdefault(field, err.messages[0])
    return errors
