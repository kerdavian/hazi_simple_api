from os import error
from flask import Flask, render_template, request
from flask.json import jsonify
import pickle
import uuid
import json


def save_data(data):
  with open('projects.json', 'w') as json_file:
    json.dump(data, json_file)
    with open("projects.pickle", "wb") as pickle_file:
      pickle.dump(data, pickle_file)


def which_project(projects, id):
  for i in range(len(projects)-1):
    print(projects[i]['project_id'])
    if projects[i]['project_id'] == id:
      return i


def filter_list_of_dicts(list_of_dicts, fields):
  filtered = []
  for dict in list_of_dicts:
    in_dict = {}
    for key, value in dict.items():
      if key in fields:
        in_dict[key] = value
    filtered.append(in_dict)
  
  return filtered


def try_check(body_request, fields):
  '''
  Levizsgállja 
  hogy van-e 'fields' key,
  hogy üres-e body,
  hogy a megadott a fieldek valóban léteznek-e,
  hogy nem üres listát küldtünk-e
  Ha itt bárhol hibát kapunk akkor visszadja a teljes listát
  '''
  body_request['fields'] == 'fields'
  request.get_json() == None
  filtered_fields = []
  for field in body_request['fields']:
    if field in fields:
      filtered_fields.append(field)
  
  # ha üres a 'filtered_fields' viszatérünk egy nullával
  if len(filtered_fields) == 0:
    return 0
  else:
    # egyébként a szűrt listát adjuk vissza
    return filter_list_of_dicts(projects, filtered_fields)


project_fields = ["name","creation_date", "completed", "project_id", "tasks"]

task_fields = ["name", "completed","checklist", "task_id"]


app = Flask(__name__)

# projects = [{
#     'name': 'my project',
#     'tasks': [{
#         'name': 'my_task',
#         'completed': False
#     }]
# }]

projects = []
with open("projects.pickle", "rb") as pickle_file:
  pkl = pickle.load(pickle_file)
  projects = pkl["projects"]


@app.route('/')
def home():
  name = "Elemér"
  return render_template('index.html', user_name=name)


@app.route('/project')
def get_projects():
  # ez json obj-ben adja vissza az adatokat
  body_request = request.get_json()
  try:
    fields = try_check(body_request, project_fields)
    # ha üres a fields
    if fields == 0:
      raise error
  except:
    return jsonify({"projects":projects})

  return jsonify({"projects":fields})


@app.route('/project/<string:id>')
def get_project(id):
  for project in projects:
    if project["project_id"] == id:
      return jsonify(project)
  return jsonify({'message': 'project is not found!'})


@app.route('/project/<string:id>/task')
def get_all_task_in_project(id):
  for project in projects:
    if project['project_id'] == id:
      body_request = request.get_json()
      try:
        fields = try_check(body_request, task_fields)
         #ha üres a fields
        if fields == 0:
          raise error
      except:
        return jsonify({"tasks":project['tasks']})

  return jsonify({"projects":fields})
      
 
      

  return jsonify({'message': 'project is not found!'})


@app.route('/project', methods=['POST'])
def create_project():
  new_project_id = uuid.uuid4().hex[:24]

  # lekérdezzuk a http requestbol az adatot
  request_data = request.get_json()

  new_project = {'name': request_data['name'], 'creation_date':request_data['creation_date'], 'completed': request_data['completed'], 'project_id': new_project_id,'tasks': request_data['tasks'],  }
  projects.append(new_project)

  save_data({"projects": projects})
  
  # return jsonify(new_project)
  return jsonify({ 'message': f'project created with id: {new_project_id}' })


@app.route('/project/<string:id>/task', methods=['POST'])
def add_task_to_projetc(id):
  request_data = request.get_json()
  for project in projects:
    if project['project_id'] == id:
      new_task_id = uuid.uuid4().hex[:24]
      new_task = {
          'name': request_data['name'],
          'task_id':new_task_id,
          'completed': request_data['completed'],
          'checklist': request_data['checklist']
      }
      
      projects[which_project(projects, id)]['tasks'].append(new_task)
      save_data({'projects': projects})

      return jsonify({ 'message': f'new task was created with id: {new_task_id}' })
  return jsonify({'message': 'project is not found!'})

@app.route('/project/<string:id>/complete',methods=['POST'])
def project_complete(id):
  request_data =  request.get_json()
  for project in projects:
    if project['project_id'] == id:
      if project['completed'] == request_data['completed']: #Most akkor is 200-al tér vissza, ha False-ról Falsra állítottak egy projectet
        return "", 200
    
      completed_project = {'name': project['name'], 'creation_date' : project['creation_date'], 'completed' : request_data['completed'], 'project_id' : project['project_id'],'tasks': project['tasks']}

      projects[which_project(projects, id)] = completed_project

      save_data({'projects': projects})

      return jsonify(completed_project)




if __name__ == '__main__':
  app.run(port=5000, debug=True)
