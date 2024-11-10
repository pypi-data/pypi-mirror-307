# django-cognito-saml

Library to implement django authentication using cognito (via pyjwt).

Assumptions made:

- Using `authorization code` flow. Implicit grant is insecure as the access token is transferred over in the request parameters without encryption.

## Settings

The following settings should be set in your settings file against a `COGNITO_CONFIG` dictionary.

| Setting             | Description                                                                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ENDPOINT**        | Either the hosted domain or custom domain for your cognito app                                                                                          |
| **CLIENT_ID**       | CLIENT_ID of your application in your user pool                                                                                                         |
| **CLIENT_SECRET**   | CLIENT_SECRET of your application in your user pool                                                                                                     |
| **JWKS_URI**        | The JWKS URI of your user pool. Used to verify the JWT.                                                                                                 |
| **REDIRECT_URI**    | **OPTIONAL** It is possible to share one cognito app with multiple websites via a proxy.                                                                |
| **RESPONSE_HOOK**   | **OPTIONAL** Post authentication hook to modify the response (perhaps to add headers). Specify it as a django import_string.                            |
| **REQUIRED_GROUPS** | **OPTIONAL** Specify when using `SuperUserBackend` to restrict the ability to login to saml users with `custom:groups` containing all `REQUIRED_GROUPS. |

## Installation

1. Add the above settings to your settings.

```settings.py
COGNITO_CONFIG = {
    "ENDPOINT": "",
    "CLIENT_ID": "",
    "CLIENT_SECRET": "",
    "JWKS_URI": "",
    "REDIRECT_URI": "",
    "RESPONSE_HOOK": ""
    "REQUIRED_GROUPS": []
}
```

2. Define your authentication backend. Subclass off `django_cognito_saml.backends.CognitoUserBackend`.

   Define the `username` field of your user by customizing the `authenticate` method. If you wish
   to add additional fields to the user or modify the user's permissions, override the `configure_user`
   method. The `configure_user` method has access to `self.cognito_jwt` which contains the decoded
   jwt token with the cognito saml assertions.

   Set `create_unknown_user = False` if you want to disable automatic creation of users.

```python
class CustomCognitoBackend(CognitoUserBackend):
    # Change this to False if you do not want to create a remote user.
    create_unknown_user = True

    def authenticate(  # type: ignore[override]
        self, request: HttpRequest, cognito_jwt: dict[str, Any], **kwargs: Any
    ) -> Optional[AbstractBaseUser]:
        # Customizing the username field used to create the user
        remote_user = cognito_jwt["username"]
        user = super().authenticate(request, remote_user=remote_user, **kwargs)
        return user

    def configure_user(  # type: ignore[override]
        self, request: HttpRequest, user: AbstractBaseUser, created: bool = True
    ) -> AbstractBaseUser:
        # Configuring the user post login
        if created:
            user.name = self.cognito_jwt["name"]
            user.save()
        return user


```

3. Add `SuperUserBackend` to your authentication backends.

```python
AUTHENTICATION_BACKENDS = (
    ...
    "django_cognito_saml.backends.SuperUserBackend",
    ...
)
```

4. Add the cognito saml urls to your `urls.py`

```python
urls = [
    ...
    path("/", include("django_cognito_saml.urls")),
]
```
