import os
import pkg_resources


def find_bluepy_helper():
    try:
        # Get the bluepy package location
        bluepy_location = pkg_resources.get_distribution("bluepy").location
        # Construct the full path to bluepy-helper
        bluepy_helper_path = os.path.join(bluepy_location, 'bluepy', 'bluepy-helper')

        if os.path.isfile(bluepy_helper_path):
            return bluepy_helper_path
        else:
            return "bluepy-helper not found in the expected location."
    except pkg_resources.DistributionNotFound:
        return "bluepy package not found."


if __name__ == "__main__":
    print(find_bluepy_helper())
