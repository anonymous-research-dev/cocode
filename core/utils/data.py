from collections import defaultdict
import json
import os
from core.utils.courses import load_course, load_material, load_material_content, load_survey_questions
from core.models import CourseState, ExerciseLogBundle, ExerciseSnapBundle, ExerciseState, MaterialState, SurveyAnswer, User
from cocode import settings


def save_course_data(value, course_id, filename):
    output_path = os.path.join(settings.EXPORT_PATH, 'course_%s' % course_id)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    file_path = os.path.join(output_path, '%s.json' % filename)
    with open(file_path, 'w') as f:
        json.dump(value, f)

def export_course_data(course_id):
    course = load_course(course_id)
    save_course_data(course, course_id, 'course')

    course_states = CourseState.objects.filter(course_id=course_id)
    save_course_data({x.user_id: x.to_dict() for x in course_states}, course_id, 'course_states')

    users = User.objects.filter(id__in=course_states.values('user_id'))
    save_course_data({x.id: x.to_dict()
                      for x in users}, course_id, 'users')

    for chapter in course['chapters']:
        for material in chapter['materials']:
            material = load_material(course_id, material['id'])
            material_content = load_material_content(course_id, material['id'])

            save_course_data(material, course_id, 'material_%s' % material['id'])
            save_course_data(material_content, course_id, 'material_content_%s' % material['id'])

            material_states = MaterialState.objects.filter(course_id=course_id)
            save_course_data({x.user_id: x.to_dict() for x in material_states}, course_id, 'material_states_%s' % material['id'])

            if material['type'] == 'exercise':
                exercise_states = ExerciseState.objects.filter(course_id=course_id)
                save_course_data({x.user_id: x.to_dict() for x in exercise_states},
                             course_id, 'exercise_states_%s' % material['id'])

                log_bundles = ExerciseLogBundle.objects.filter(course_id=course_id, material_id=material['id']).order_by('created_at')
                logs_dict = defaultdict(list)
                for log_bundle in log_bundles:
                    user_id = log_bundle.user_id
                    logs = json.loads(log_bundle.logs)
                    for log in logs:
                        logs_dict[user_id].append(log)
                save_course_data(logs_dict, course_id,
                                 'exercise_logs_dict_%s' % material['id'])
                
                snap_bundles = ExerciseSnapBundle.objects.filter(course_id=course_id, material_id=material['id']).order_by('created_at')
                snaps_dict = defaultdict(list)
                for snap_bundle in snap_bundles:
                    user_id = snap_bundle.user_id
                    snaps = json.loads(snap_bundle.snaps)
                    for snap in snaps:
                        snaps_dict[user_id].append(snap)
                save_course_data(snaps_dict, course_id,
                                 'exercise_snaps_dict_%s' % material['id'])

            elif material['type'] == 'survey':
                questions = load_survey_questions(course_id, material['id'])
                save_course_data(questions, course_id, 'questions_%s' % material['id'])

                answers = SurveyAnswer.objects.filter(
                    course_id=course_id, material_id=material['id'])
                answers_dict = defaultdict(dict)
                for answer in answers:
                    answers_dict[answer.user_id][answer.question_id] = answer.value
                save_course_data(answers_dict, course_id,
                                 'answers_%s' % material['id'])
                


