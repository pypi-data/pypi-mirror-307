from pydantic import BaseModel, Field, EmailStr

from universal_watcher.core.classes.notification_platform.notification_platform_parameters import (
    NotificationPlatformParameters,
)


class EmailParameters(BaseModel, NotificationPlatformParameters):
    to: EmailStr = Field(..., description="Adresa príjemcu emailu.")
