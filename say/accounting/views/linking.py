import uuid

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import redirect


@login_required
def linking_telebot(request, botel_username):
    """
    generates a temporary uuid corresponding to the user's id
    """
    user_pk_retrieve_fragment = uuid.uuid4()
    cache.set(str(user_pk_retrieve_fragment), request.user.pk, timeout=2 * 60)
    return redirect(
        f"https://t.me/{botel_username}/?start=linkUserPK_{user_pk_retrieve_fragment}"
    )
