from flask import Flask, render_template, request
from flask.json import jsonify
import pickle

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
  projects = pickle.load(pickle_file)


@app.route('/')
def home():
  name = "Elemér"
  return render_template('index.html', user_name=name)


@app.route('/project')
def get_projects():
  # ez json obj-ben adja vissza az adatokat
  return jsonify(projects)


@app.route('/project/<string:name>')
def get_project(name):
  for project in projects:
    if project['name'] == name:
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
  # lekérdezzuk a http requestbol az adatot
  request_data = request.get_json()
  new_project = {'name': request_data['name'], 'tasks': request_data['tasks']}
  projects.append(new_project)
  return jsonify(new_project)


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
  app.run(host='0.0.0.0', port=5000, debug=True)
