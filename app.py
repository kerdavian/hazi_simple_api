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
  # return jsonify(projects) ezzel is működik
  return jsonify({"projects":projects})



@app.route('/project/<string:id>')
def get_project(id):
  for project in projects:
    if project["project_id"] == id:
      return jsonify(project)
  return jsonify({'message': 'project is not found!'})


@app.route('/project/<string:name>/task')
def get_all_task_in_project(name):
  for project in projects:
    if project['name'] == name:
      return jsonify({'tasks': project['tasks']})
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


@app.route('/project/<string:name>/task', methods=['POST'])
def add_task_to_projetc(name):
  request_data = request.get_json()
  for project in projects:
    if project['name'] == name:
      new_task = {
          'name': request_data['name'],
          'completed': request_data['completed']
      }
      project['tasks'].append(new_task)
      return jsonify(new_task)
  return jsonify({'message': 'project is not found!'})


if __name__ == '__main__':
  app.run(port=5000, debug=True)
