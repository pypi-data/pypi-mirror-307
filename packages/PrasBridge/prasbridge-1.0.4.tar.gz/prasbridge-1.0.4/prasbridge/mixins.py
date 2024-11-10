from django.contrib.auth.hashers import check_password, make_password

class UserMixin:
    """Mixin class providing user-specific utility methods."""
    
    def set_password(self, raw_password):
        """Hashes the user's password and stores it."""
        self._password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Checks if the provided password matches the stored hashed password."""
        return check_password(raw_password, self._password)

    def get_full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
