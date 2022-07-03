import datetime

ROLE_CHOICES = (
    (
        "super_admin",
        "Super Admin",
    ),  # is_staff=True, is_superuser=True = Application Super Admin
    (
        "admin",
        "Admin",
    ),  # is_staff=True, is_superuser=False = Application Admin
    (
        "company_admin",
        "Company Admin",
    ),  # is_staff=False, is_superuser=False = Company Admin
    (
        "agent",
        "Agent",
    ),  # is_staff=False, is_superuser=False = Company Employee
)

TOKEN_TYPE_CHOICES = (
    ("verification", "Email Verification"),
    ("pwd_reset", "Password Reset"),
)

YEAR_CHOICES = [(y, y) for y in range(1970, datetime.date.today().year + 1)]
