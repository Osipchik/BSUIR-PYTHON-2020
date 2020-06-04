from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from . import render_twit
from ..managers import get_objects_or_none, prepare_tweet
from ..models import Tweet, Bookmark


@login_required(login_url='/accounts/login/')
@require_http_methods(["GET"])
def bookmarks(request):
    twits = []
    for i in get_objects_or_none(Bookmark, user_id=request.user.id):
        prepare_tweet(i.tweet, request.user.id)
        twits.append(i.tweet)

    context = {'twits': twits, 'bookmarks_count': len(twits)}

    if request.is_ajax():
        return JsonResponse({
            "result": True,
            "main": render_to_string(
                request=request,
                template_name='pages/bookmarks.html',
                context=context
            )
        })
    else:
        return render(request, 'pages/extends/bookmarks.html', context)


@login_required(login_url='/accounts/login/')
@require_http_methods(["POST"])
def add_bookmark(request, twit_id):
    query = get_objects_or_none(Tweet, id=twit_id)
    if query.count() == 0:
        return HttpResponse(status=404)

    tweet = query[0]
    bookmark = Bookmark(user=request.user, tweet=tweet)
    bookmark.save()

    prepare_tweet(tweet, request.user.id)

    return JsonResponse(render_twit(request, tweet))


@login_required(login_url='/accounts/login/')
@require_http_methods(["DELETE"])
def remove_bookmark(request, twit_id):
    query = get_objects_or_none(Bookmark, tweet_id=twit_id, user_id=request.user.id)
    if query.count() == 0:
        return HttpResponse(status=404)

    bookmark = query[0]
    bookmark.delete()

    twit = get_objects_or_none(Tweet, id=twit_id)[0]
    prepare_tweet(twit, request.user.id)

    return JsonResponse(render_twit(request, twit))
