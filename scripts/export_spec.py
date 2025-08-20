# export_spec.py
from app import create_app
import json, sys

app = create_app()
with app.test_request_context():
    spec = app.extensions["flask-smorest"].api.spec.to_dict()
    json.dump(spec, sys.stdout, indent=2)
