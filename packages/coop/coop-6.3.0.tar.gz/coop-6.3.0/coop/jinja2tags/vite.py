import jinja2.ext
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django_vite.templatetags.django_vite import vite_asset, vite_hmr_client


def static_url(path):
    if settings.DEBUG:
        return f"http://localhost:3000/{path}"
    return staticfiles_storage.url(path)


class Extension(jinja2.ext.Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update(
            {
                "vite_hmr_client": vite_hmr_client,
                "vite_asset": vite_asset,
                "static": static_url,
            }
        )
