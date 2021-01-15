from django.http import HttpResponse, JsonResponse, Http404

ERROR_RESPONSE_DICT = {
    'get_request_illegal': {
        'data': {
            'code': 'get_request_illegal',
            'message': 'GET request is not allowed.',
        },
        'status': 405,
    },
    'post_request_illegal': {
        'data': {
            'code': 'post_request_illegal',
            'message': 'POST request is not allowed.',
        },
        'status': 405,
    },
    'permission_denied': {
        'data': {
            'code': 'permission_denied',
            'message': 'Permission denied.',
        },
        'status': 403,
    },
    'not_acceptable': {
        'data': {
            'code': 'not_acceptable',
            'message': 'Requested task is not acceptable.',
        },
        'status': 406,
    },
}


def JsonErrorResponse(code):
    return JsonResponse(**(ERROR_RESPONSE_DICT[code]))


def JsonOkResponse(data=None):
    response = {'status': 200}
    if data is not None:
        response['data'] = data
    return JsonResponse(response)


def validatePost(request):
    if request.method == 'GET':
        raise Http404('GET request is not allowed.')


def validateGet(request):
    if request.method == 'POST':
        raise Http404('POST request is not allowed.')


def NoContentResponse():
    return HttpResponse(status=204)
