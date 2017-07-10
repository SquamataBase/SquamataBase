# May need to change depending on your installations
SPATIALITE_LIBRARY_PATH = '/usr/local/lib/mod_spatialite.dylib'

# Check that coordinates fall within administrative boundary prior to saving
VALIDATE_COORDINATES = True

# If food records have no georeferenced locality sample a random point within
# the administrative boundary associated with the food record
ALLOW_RANDOM_COORDINATES = True