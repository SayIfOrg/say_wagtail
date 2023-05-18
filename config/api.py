from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet


# Api router to correspond to the content that managed through wagtail ecosystem
wagtailapi_router = WagtailAPIRouter("wagtailapi")

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (such as pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
wagtailapi_router.register_endpoint("pages", PagesAPIViewSet)
wagtailapi_router.register_endpoint("images", ImagesAPIViewSet)
wagtailapi_router.register_endpoint("documents", DocumentsAPIViewSet)
