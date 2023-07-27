import yaml
import requests
import os
import json


def get_api_methods_from_swagger(url):
    # Fetch the Swagger/OpenAPI specification file
    response = requests.get(url)

    # Check if the response is in JSON or YAML format
    content_type = response.headers.get('Content-Type', '')

    if 'yaml' in content_type or 'yml' in content_type:
        api_spec = yaml.safe_load(response.text)
    elif 'json' in content_type:
        api_spec = response.json()
    else:
        raise ValueError(
            "Unsupported content type. Please provide a JSON or YAML file."
        )

    api_methods = []

    for path, path_data in api_spec['paths'].items():
        for method, method_data in path_data.items():
            api_methods.append((method.upper(), path))

    return api_methods


swagger_url = "https://scoring-api-stage.k8s.superdao.dev/openapi.json"
api_methods = get_api_methods_from_swagger(swagger_url)

# Write to a file
json_file_path = os.path.join(os.path.dirname(__file__), 'api_methods.json')
api_methods_json = json.dumps(api_methods, indent=4)
with open(json_file_path, 'w') as f:
    f.write(api_methods_json)
