# Multilingual Setup with `gettext_lazy`

To set up a multilingual Django project using `gettext_lazy`, follow these steps:

1. **Install `gettext`**:
    Ensure you have `gettext` installed on your system. This is required for generating translation files.

2. **Update `settings.py`**:
    Add the following settings to your `settings.py` file:

    ```python
    from django.utils.translation import gettext_lazy as _

    LANGUAGES = [
         ('en', _('English')),
         ('es', _('Spanish')),
         # Add other languages here
    ]

    LOCALE_PATHS = [
         os.path.join(BASE_DIR, 'locale'),
    ]

    MIDDLEWARE = [
         'django.middleware.locale.LocaleMiddleware',
         # Other middleware
    ]
    ```

3. **Mark strings for translation**:
    Use `gettext_lazy` to mark strings for translation in your Django models, views, and templates. For example:

    ```python
    from django.utils.translation import gettext_lazy as _

    class MyModel(models.Model):
         name = models.CharField(max_length=100, verbose_name=_('Name'))
    ```

4. **Create translation files**:
    Run the following commands to create and compile translation files:

    ```bash
    django-admin makemessages -l es  # Replace 'es' with the language code
    django-admin compilemessages
    ```

5. **Translate strings**:
    Edit the `.po` files in the `locale` directory to provide translations for the marked strings.

6. **Use translations in templates**:
    Load the translation tags in your templates and use the `{% trans %}` tag to translate strings:

    ```html
    {% load i18n %}
    <h1>{% trans "Welcome" %}</h1>
    ```

By following these steps, you can set up a multilingual Django project using `gettext_lazy`.