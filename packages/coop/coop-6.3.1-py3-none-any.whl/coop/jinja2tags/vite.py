import jinja2.ext
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django_vite.templatetags.django_vite import vite_asset, vite_asset_url, vite_hmr_client


def static_url(path):
    if settings.DEBUG:
        vite_config = getattr(settings, "DJANGO_VITE", {})
        if vite_config.get("dev_mode", False):
            # Server running in debug and we're loading from the vite dev server, fetch from public
            return vite_asset_url(path)
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
