import base64
import json
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from core.models import ExerciseState
from core.utils.responses import JsonOkResponse, JsonErrorResponse
from core.utils.courses import get_file_from_tree, put_file_to_tree

def get_exercise_state(user, course_id, material_id):
    exercise_state = get_object_or_404(
        ExerciseState, user=user, course_id=course_id, material_id=material_id)
    return exercise_state


def exercise_state_files(request, course_id, material_id):
    exercise_state = get_exercise_state(request.user, course_id, material_id)
    if request.method == 'GET':
        return JsonOkResponse(exercise_state.value)
    elif request.method == 'POST':
        params = json.loads(request.body)
        exercise_state.value = json.dumps(params.get('value', r'{}'))
        exercise_state.save()
        return JsonOkResponse()
    else:
        raise Http404('Unexpected method.')


def exercise_state_file(request, course_id, material_id, path):
    exercise_state = get_exercise_state(request.user, course_id, material_id)
    tree = json.loads(exercise_state.value)
    if request.method == 'GET':
        file = get_file_from_tree(path, tree)
        if file is None:
            raise Http404('File not found.')
        if file['is_text']:
            return HttpResponse(file['value'])
        else:
            data = base64.b64decode(file['value'].encode('ascii'))
            return HttpResponse(data, content_type='application/octet-stream')
    elif request.method == 'POST':
        params = json.loads(request.body)
        file = params['file']
        tree = put_file_to_tree(path, tree, file)
        if tree is None:
            return JsonErrorResponse('not_acceptable')
        exercise_state.value = json.dumps(tree)
        exercise_state.save()
        return JsonOkResponse()
    else:
        raise Http404('Unexpected method.')
    

def exercise_state_seconds(request, course_id, material_id):
    exercise_state = get_exercise_state(request.user, course_id, material_id)
    if request.method == 'GET':
        seconds = exercise_state.get_seconds_dict()
        return JsonOkResponse(data=seconds)
    elif request.method == 'POST':
        params = json.loads(request.body)
        edited = False
        if 'edit_seconds' in params:
            exercise_state.edit_seconds = params['edit_seconds']
            edited = True
        if 'open_seconds' in params:
            exercise_state.open_seconds = params['open_seconds']
            edited = True
        if edited:
            exercise_state.save()
        return JsonOkResponse()
    else:
        raise Http404('Unexpected method.')


def exercise_state_reset(request, course_id, material_id):
    exercise_state = get_exercise_state(request.user, course_id, material_id)
    if request.method == 'POST':
        exercise_state.set_default_value()
        return JsonOkResponse()
    else:
        raise Http404('Unexpected method.')
