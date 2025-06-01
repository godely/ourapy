import json

def parse_openapi_spec(spec_content):
    """
    Parses the OpenAPI specification and extracts relevant information.

    Args:
        spec_content (str): The string content of the openapi_spec.json file.

    Returns:
        tuple: A tuple containing two dictionaries:
               - paths_data: Information about each path and its methods.
               - components_schemas_data: Information about component schemas.
    """
    try:
        spec = json.loads(spec_content)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        raise ValueError(f"Failed to parse OpenAPI spec: {e}")

    paths_data = {}
    if "paths" in spec and isinstance(spec["paths"], dict):
        for path_string, path_item in spec["paths"].items():
            paths_data[path_string] = {}
            for method, method_details in path_item.items():
                if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]:
                    paths_data[path_string][method.upper()] = {
                        "tags": method_details.get("tags", []),
                        "summary": method_details.get("summary"),
                        "operationId": method_details.get("operationId"),
                        "parameters": [],
                        "responses": {}
                    }

                    if "parameters" in method_details and isinstance(method_details["parameters"], list):
                        for param in method_details["parameters"]:
                            paths_data[path_string][method.upper()]["parameters"].append({
                                "name": param.get("name"),
                                "in": param.get("in"),
                                "required": param.get("required"),
                                "schema": param.get("schema")
                            })

                    if "responses" in method_details and isinstance(method_details["responses"], dict):
                        for status_code, response_details in method_details["responses"].items():
                            paths_data[path_string][method.upper()]["responses"][status_code] = {
                                "description": response_details.get("description"),
                                "content": response_details.get("content", {}).get("application/json", {}).get("schema")
                            }
    else:
        print("Warning: 'paths' attribute not found or is not a dictionary in the OpenAPI spec.")


    components_schemas_data = {}
    if "components" in spec and "schemas" in spec["components"] and isinstance(spec["components"]["schemas"], dict):
        for schema_name, schema_details in spec["components"]["schemas"].items():
            components_schemas_data[schema_name] = schema_details
    else:
        print("Warning: 'components.schemas' attribute not found or is not a dictionary in the OpenAPI spec.")

    return paths_data, components_schemas_data

if __name__ == "__main__":
    try:
        with open("openapi_spec.json", "r") as f:
            openapi_content = f.read()
    except FileNotFoundError:
        print("Error: openapi_spec.json not found.")
        exit(1)
    except IOError as e:
        print(f"Error reading openapi_spec.json: {e}")
        exit(1)

    parsed_paths, parsed_schemas = parse_openapi_spec(openapi_content)

    if parsed_paths is not None and parsed_schemas is not None:
        # You can optionally print or process the extracted data here
        # For now, just acknowledge completion as per the task requirement.
        print("OpenAPI specification parsed successfully.")
        # Example: Print all paths
        # print("\nPaths:")
        # for path, methods in parsed_paths.items():
        #     print(f"  {path}: {list(methods.keys())}")
        #
        # Example: Print all component schema names
        # print("\nComponent Schemas:")
        # for schema_name in parsed_schemas.keys():
        #     print(f"  {schema_name}")
    else:
        print("OpenAPI specification parsing failed.")
