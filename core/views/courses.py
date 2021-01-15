import json
import random
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import F, Value, Count, Max, Avg
from core.models import CourseState, MaterialState, ExerciseState, ExerciseSnapBundle, ExerciseLogBundle, SurveyAnswer, User
from core.utils.responses import JsonOkResponse, JsonErrorResponse
from core.utils.courses import load_course_index, load_course, load_material, load_material_content, load_survey_questions

def get_course_or_404(course_id):
    course = load_course(course_id)
    if course is None:
        raise Http404('The requested course is not available.')
    return course


def get_material_or_404(course_id, material_id):
    material = load_material(course_id, material_id)
    if material is None:
        raise Http404('The requested material is not available.')
    return material


def get_course_state_or_create(course, user):
    course_state, created = CourseState.objects.get_or_create(
        course_id=course['id'], user=user)
    if created:
        exp_group_id = get_course_state_exp_group_id(course)
        if exp_group_id:
            course_state.exp_group_id = exp_group_id
            course_state.save()
    return course_state


def get_exercise_state_or_create(course_id, material_id, user):
    exercise_state, _ = ExerciseState.objects.get_or_create(
        course_id=course_id, material_id=material_id, user=user)
    return exercise_state


def get_material_state_or_create(course_id, material_id, user):
    material_state, _ = MaterialState.objects.get_or_create(
        course_id=course_id, material_id=material_id, user=user)
    return material_state


def get_course_state_exp_group_id(course):
    if not course.get('allow_experiment', False):
        return ''
    if 'experiment' not in course:
        return ''

    exp_group_weight_dict = {group_id: group['weight'] for group_id, group in course['experiment']['groups'].items()}
    total_weight = sum(exp_group_weight_dict.values())

    exp_group_user_counts = CourseState.objects \
        .filter(exp_group_id__in=exp_group_weight_dict.keys()) \
        .values('exp_group_id') \
        .annotate(count=Count('exp_group_id'))
    exp_group_user_count_dict = {row['exp_group_id']: row['count'] for row in exp_group_user_counts}
    total_user_count = sum(exp_group_user_count_dict.values())

    draw_box = []
    for exp_group_id, weight in exp_group_weight_dict.items():
        expected_count = total_user_count * (weight / total_weight)
        count = exp_group_user_count_dict.get(exp_group_id, 0)
        if count < expected_count:
            draw_box.append(exp_group_id)
    if not draw_box:
        draw_box = list(exp_group_weight_dict.keys())

    return random.choice(draw_box)


def get_exp_mode(course, course_state, material):
    exp_mode = {}
    group_id = course_state.exp_group_id
    if group_id and ('experiment' in course):
        groups = course['experiment']['groups']
        if group_id in groups:
            material_mode_map = groups[group_id]['material_mode_map']
            if material['id'] in material_mode_map:
                mode_id = material_mode_map[material['id']]
                exp_mode = course['experiment']['modes'].get(mode_id, {})
    return exp_mode


def get_survey_answers(course_id, material_id, user):
    questions = load_survey_questions(course_id, material_id)
    answer_rows = SurveyAnswer.objects.filter(
        course_id=course_id, material_id=material_id, user=user)
    answers = {}
    for question in questions:
        if 'id' in question:
            answers[question['id']] = ''
    for answer_row in answer_rows:
        answers[answer_row.question_id] = answer_row.value
    return answers


def get_material_states_dict(course_id, user):
    material_states = MaterialState.objects.filter(course_id=course_id, user=user)
    material_states_dict = {}
    for material_state in material_states:
        material_states_dict[material_state.material_id] = material_state.to_dict()
    return material_states_dict


def get_material_accessible_dict(course, material_states_dict):
    accessible_dict = {}
    material_ids = []
    for chapter in course['chapters']:
        for material in chapter['materials']:
            accessible = True
            for material_id in material_ids:
                if material_id not in material_states_dict:
                    accessible = False
                    break
                elif material_states_dict[material_id]['progress'] < 100:
                    accessible = False
                    break
            accessible_dict[material['id']] = accessible
            material_ids.append(material['id'])
    return accessible_dict


def get_next_material(course, material):
    prev_material = None
    for chapter in course['chapters']:
        for curr_material in chapter['materials']:
            print('curr material id', curr_material['id'])
            if prev_material and (prev_material['id'] == material['id']):
                return curr_material
            prev_material = curr_material


def get_material_template(material):
    if material['type'] == 'exercise':
        return 'courses/exercise_show.html'
    elif material['type'] == 'article':
        return 'courses/article_show.html'
    elif material['type'] == 'survey':
        return 'courses/survey_show.html'


def course_list(request):
    course_index = load_course_index()
    
    return render(
        request,
        'courses/course_index.html',
        {
            'course_index': course_index,
        }
    )


def course_show(request, course_id):
    course = get_course_or_404(course_id)
    course_state = get_course_state_or_create(course, request.user)
    material_states_dict = get_material_states_dict(course_id, request.user)
    material_accessible_dict = get_material_accessible_dict(
        course, material_states_dict)

    return render(
        request,
        'courses/course_show.html',
        {
            'course': course,
            'course_state': course_state,
            'material_states_dict': material_states_dict,
            'material_accessible_dict': material_accessible_dict,
        }
    )


def course_experiment(request, course_id):
    course = get_course_or_404(course_id)

    if not course.get('allow_experiment', False):
        raise PermissionDenied('Experiment access is now allowed for this course.')

    if request.user and request.user.is_authenticated and request.user.is_restricted:
        user = request.user
    else:
        user = User.create_experiment_user()
        auth.login(request, user,
                   backend='django.contrib.auth.backends.ModelBackend')

    return redirect('course_show', course_id=course_id)


def course_state_maps(request, course_id):
    course = get_course_or_404(course_id)
    material_states_dict = get_material_states_dict(course_id, request.user)
    material_accessible_dict = get_material_accessible_dict(
        course, material_states_dict)

    return JsonOkResponse(data={
        'material_states_dict': material_states_dict,
        'material_accessible_dict': material_accessible_dict,
    })


def material_show(request, course_id, material_id):
    course = get_course_or_404(course_id)
    course_state = get_course_state_or_create(course, request.user)
    material_states_dict = get_material_states_dict(course_id, request.user)
    material_accessible_dict = get_material_accessible_dict(
        course, material_states_dict)
    material = get_material_or_404(course_id, material_id)
    next_material = get_next_material(course, material)
    exp_mode = get_exp_mode(course, course_state, material)

    if not material_accessible_dict[material_id]:
        raise PermissionDenied('Prerequisites for this material are not met.')

    content = load_material_content(course_id, material_id)
    
    context = {
        'course': course,
        'course_state': course_state,
        'material_states_dict': material_states_dict,
        'material_accessible_dict': material_accessible_dict,
        'material': material,
        'next_material': next_material,
        'exp_mode': exp_mode,
        'content': content,
    }

    if material['type'] == 'exercise':
        context['exercise_state'] = get_exercise_state_or_create(course_id, material_id, request.user)

    if material['type'] == 'survey':
        context['questions'] = load_survey_questions(course_id, material_id)
        context['answers'] = get_survey_answers(
            course_id, material_id, request.user)

    return render(
        request,
        get_material_template(material),
        context,
    )


def material_state(request, course_id, material_id):
    if request.method == 'POST':
        params = json.loads(request.body)
        material_state = get_material_state_or_create(course_id, material_id, request.user)
        if 'progress' in params:
            material_state.progress = max(material_state.progress, params['progress'])
        if 'star' in params:
            material_state.star = max(material_state.star, params['star'])
        if 'value' in params:
            material_state.value = params['value']
        material_state.save()
        return JsonOkResponse()
    else:
        raise Http404('Unexpected method.')


def exercise_snaps(request, course_id, material_id):
    if request.method == 'GET':
        user_snaps_dict = ExerciseSnapBundle.get_user_snaps_dict(
            course_id, material_id)
        data = {'user_snaps_dict': user_snaps_dict}
        return JsonOkResponse(data=data)
    elif request.method == 'POST':
        params = json.loads(request.body)
        if 'snaps' in params:
            snap_bundle = ExerciseSnapBundle(
                course_id=course_id,
                material_id=material_id,
                snaps=json.dumps(params['snaps']),
                user=request.user,
            )
            snap_bundle.save()
        return JsonOkResponse()
    else:
        raise Http404('Unexpected method.')


def exercise_logs(request, course_id, material_id):
    if request.method == 'POST':
        params = json.loads(request.body)
        if 'logs' in params:
            log_bundle = ExerciseLogBundle(
                course_id=course_id,
                material_id=material_id,
                logs=json.dumps(params['logs']),
                user=request.user,
            )
            log_bundle.save()
        return JsonOkResponse()
    else:
        raise Http404('Unexpected method.')

def survey_answers(request, course_id, material_id):
    if request.method == 'GET':
        answers = get_survey_answers(course_id, material_id, request.user)
        data = {'answers': answers}
        return JsonOkResponse(data=data)
    elif request.method == 'POST':
        params = json.loads(request.body)
        if 'answers' in params:
            for question_id, value in params['answers'].items():
                try:
                    answer = SurveyAnswer.objects.get(course_id=course_id, material_id=material_id, question_id=question_id, user=request.user)
                    answer.value = value
                    answer.save()
                except SurveyAnswer.DoesNotExist:
                    answer = SurveyAnswer(
                        course_id=course_id, material_id=material_id, question_id=question_id, value=value, user=request.user)
                    answer.save()
        return JsonOkResponse()
    else:
        raise Http404('Unexpected method.')
