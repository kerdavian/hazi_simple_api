import pickle
import json


# with open("projects.json") as json_file:
#   data = json.load(json_file)
#   with open("projects.pickle", "wb") as pickle_file:
#     pickle.dump(data, pickle_file)


with open("projects.pickle", "rb") as pickle_file:
  pkl = pickle.load(pickle_file)

print(pkl['projects'])

  # for p in pkl["projects"]:
  #   print(p["project_id"])