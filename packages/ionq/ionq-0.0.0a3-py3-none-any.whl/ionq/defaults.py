from importlib.metadata import version
import os

# Specify the version of the IonQ API that this SDK targets.
API_VERSION = "0.4"

# Get the version of the current package
SDK_VERSION = version(os.path.basename(os.path.dirname(__file__)))

# Construct the default API URL by incorporating the specified API version into the base URL.
DEFAULT_API_URL = f"https://api.ionq.co/v{API_VERSION}"
