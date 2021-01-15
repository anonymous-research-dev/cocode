from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import translation


def core_landing(request):
    return render(request, 'core/landing.html', {})

def core_document_show(request, path):
    language = translation.get_language()
    return render(
        request,
        'core/document.html',
        {
            'document_path': 'documents/en/%s' % path,
            'local_document_path': 'documents/%s/%s' % (language, path),
        }
    )
