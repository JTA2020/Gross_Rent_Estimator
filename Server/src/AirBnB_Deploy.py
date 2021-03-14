# load the model from disk
import pickle
import numpy as np
filename = 'mvp_model.sav'

loaded_model = pickle.load(open(filename, 'rb'))
beds = 2
baths = 1
occupancy_rate = 0.6
days_rented = 365*occupancy_rate
result = loaded_model.predict(np.array([beds,baths]).reshape(1, -1))
print("The average monthly AirBnB value for this listing is in the ballpark of: ", result[0]*days_rented/12)