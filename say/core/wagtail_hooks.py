from django_vite.templatetags.django_vite import vite_asset, vite_hmr_client
from wagtail import hooks


VITE_SCRIPTS = "".join((vite_hmr_client(), vite_asset("static_src/main.ts")))


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return "".join((VITE_SCRIPTS,))
