import os
import base64
import json
from core.utils.files import get_file_type
from cocode import settings

def get_course_path(course_id):
    return os.path.join(settings.COURSES_PATH, course_id)

def get_file_tree(root=None, curr_dir=''):
    tree = {
        'path': curr_dir,
        'name': os.path.basename(curr_dir),
        'dirs': {},
        'files': {},
    }
    for filename in os.listdir(root):
        file_path = os.path.join(root, filename)
        file_curr_path = os.path.join(curr_dir, filename)
        file_type = get_file_type(filename)
        if os.path.isfile(file_path):
            file_dict = {
                'path': file_curr_path,
                'name': filename,
                'type': file_type,
            }
            if get_file_type(filename) == 'text':
                file_dict['is_text'] = True
                with open(file_path, 'r') as f:
                    file_dict['value'] = f.read()
            else:
                file_dict['is_text'] = False
                with open(file_path, 'rb') as f:
                    file_dict['value'] = base64.b64encode(f.read()).decode('ascii')
            tree['files'][filename] = file_dict
        else:
            dir_dict = get_file_tree(file_path, file_curr_path)
            tree['dirs'][filename] = dir_dict
    return tree

def get_dir_from_tree(path, tree):
    path_tokens = path.split('/')
    cursor = tree
    while path_tokens:
        if path_tokens[0] not in cursor['dirs']:
            return None
        cursor = cursor['dirs'][path_tokens[0]]
        path_tokens.pop(0)
    return cursor

def get_parent_dir_from_tree(path, tree):
    path_tokens = path.split('/')
    if len(path_tokens) == 1:
        return tree
    else:
        return get_dir_from_tree('/'.join(path_tokens[:-1]), tree)

def get_file_from_tree(path, tree):
    parent = get_parent_dir_from_tree(path, tree)
    if parent is None:
        return None
    _, filename = os.path.split(path)
    if filename not in parent['files']:
        return None
    return parent['files'][filename]

def put_file_to_tree(path, tree, file):
    parent = get_parent_dir_from_tree(path, tree)
    if parent is None:
        return None
    _, filename = os.path.split(path)
    parent['files'][filename] = file
    return tree

# def get_prerequisite_materials(course, material):
#     material_ids = []
#     for chapter in course['chapters']:
#         for material in chapter['materials']:
#             if material['id'] != material['id']:
#                 material_ids.append(material['id'])
#             else:
#                 return material_ids
#     return []
 
def load_course_index():
    file_path = os.path.join(settings.COURSES_PATH, 'index.json')
    with open(file_path, 'r') as f:
        course_index = json.load(f)
    return course_index

def load_course(course_id):
    course_path = get_course_path(course_id)
    course_data_path = os.path.join(course_path, 'course.json')
    if not os.path.exists(course_data_path):
        return None
    
    with open(course_data_path, 'r') as f:
        course_data = json.load(f)
    course_data['id'] = course_id
    return course_data

def load_material(course_id, material_id):
    course_path = get_course_path(course_id)
    material_data_path = os.path.join(course_path, 'materials', material_id, 'material.json')
    if not os.path.exists(material_data_path):
        return None

    with open(material_data_path, 'r') as f:
        material_data = json.load(f)
    material_data['id'] = material_id
    return material_data
    
def load_material_content(course_id, material_id):
    course_path = get_course_path(course_id)
    content_path = os.path.join(
        course_path, 'materials', material_id, 'content.md')
    if not os.path.exists(content_path):
        return ''

    with open(content_path, 'r') as f:
        content = f.read()
    return content


def load_survey_questions(course_id, material_id):
    course_path = get_course_path(course_id)
    content_path = os.path.join(
        course_path, 'materials', material_id, 'questions.json')
    if not os.path.exists(content_path):
        return []

    with open(content_path, 'r') as f:
        questions = json.load(f)
    return questions


def load_exercise_files_dict(course_id, material_id):
    course_path = get_course_path(course_id)
    files_path = os.path.join(
        course_path, 'materials', material_id, 'files')
    if not os.path.exists(files_path):
        return None

    return get_file_tree(files_path)
    