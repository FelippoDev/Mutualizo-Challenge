import re

def password_regex_validation(password):
        if re.match(
                r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()\-_=+{};:,<.>/?])(?!.*\s).{8,}$', password):
            return True
        return False