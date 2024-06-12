import requests
import json
import re

# Define the Omeka API URL and the collection ID
OMEKA_API_BASE_URL = "http://georgeeliotarchive.org/api"
COLLECTION_ID = '68'  # Change this to '66' to test with the working collection

# Define the file paths for the local JSON files
AUGUST_FILE_PATH = "August1854_2.js"
PATHS_FILE_PATH = "Paths_1.js"

# Function to fetch data from Omeka API
def fetch_omeka_data(base_url, collection_id):
    items = []
    page = 1
    while True:
        url = f'{base_url}/items?collection={collection_id}&page={page}'
        response = requests.get(url)
        if response.status_code == 200:
            page_data = response.json()
            print(f"Page {page} data: {page_data}")  # Debugging line
            if not page_data:
                break  # Exit loop if no more data
            items.extend(page_data)
            page += 1
        else:
            print(f"Failed to fetch data from Omeka API: {response.status_code}")
            return []
    
    print("Raw data fetched from Omeka API:")
    print(json.dumps(items, indent=4))  # Print raw data for debugging

    # Create new dictionary with desired format and items
    data = []
    for item in items:
        if 'element_texts' in item:
            json_item = {}
            for element in item['element_texts']:
                json_item[element['element']['name']] = element['text']
            data.append(json_item)
    print("Processed data:")
    print(json.dumps(data, indent=4))
    return data

# Function to create new JSON features for August1854_2.js
def create_august_features(data):
    features = []
    for item in data:
        new_feature = {
            "type": "Feature",
            "properties": {
                "Date": item.get('Date', ''),
                "Location": item.get('Location', ''),
                "Description": item.get('Description', ''),
                "Latitude": item.get('Latitude', 0),
                "Longitude": item.get('Longitude', 0)
            },
            "geometry": {
                "type": "Point",
                "coordinates": [item.get('Longitude', 0), item.get('Latitude', 0)]
            }
        }
        features.append(new_feature)
    return features

# Function to create new JSON features for Paths_1.js
def create_paths_features(data):
    features = []
    for item in data:
        new_feature = {
            "type": "Feature",
            "properties": {
                "begin": item.get('begin', ''),
                "end": item.get('end', '')
            },
            "geometry": {
                "type": "LineString",
                "coordinates": []
            }
        }
        features.append(new_feature)
    return features

# Function to append new JSON features to JS file
def append_features_to_js(file_path, new_features):
    variable_name = 'json_August1854_7' if 'August1854_2' in file_path else 'json_Paths_1'

    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the position of the "features" array and insert new features before the closing bracket
    match = re.search(r'(var\s+' + variable_name + r'\s*=\s*\{.*"features":\s*)(\[.*\])(\s*\};)', content, re.DOTALL)
    if match:
        before_features = match.group(1)
        features_content = match.group(2)
        after_features = match.group(3)

        # Log features content for debugging
        print("Features content before updating:")
        print(features_content)

        try:
            # Convert the current features to JSON
            current_features = json.loads(features_content)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

        # Create a dictionary of new features for quick lookup by title
        new_features_dict = {f['properties']['Date']: f for f in new_features}

        # Update existing features or add new ones, and mark features to keep
        updated_features = []
        for existing_feature in current_features:
            date = existing_feature['properties'].get('Date')
            if date in new_features_dict:
                existing_feature['properties'].update(new_features_dict[date]['properties'])
                existing_feature['geometry'] = new_features_dict[date]['geometry']
                updated_features.append(existing_feature)
                del new_features_dict[date]  # Remove from new features dict as it's already added

        # Add remaining new features that were not in the existing features
        updated_features.extend(new_features_dict.values())
        
        # Convert back to JSON string
        updated_features_content = json.dumps(updated_features, indent=2)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(before_features + updated_features_content + after_features)
    else:
        # Handle the Paths_1.js case where the variable name is json_Paths_4
        match_paths = re.search(r'(var\s+json_Paths_4\s*=\s*\{.*"features":\s*)(\[.*\])(\s*\};)', content, re.DOTALL)
        if match_paths:
            before_features = match_paths.group(1)
            features_content = match_paths.group(2)
            after_features = match_paths.group(3)
            
            # Log features content for debugging
            print("Features content before updating:")
            print(features_content)

            try:
                # Convert the current features to JSON
                current_features = json.loads(features_content)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return

            # Create a dictionary of new features for quick lookup by begin
            new_features_dict = {f['properties']['begin']: f for f in new_features}

            # Update existing features or add new ones, and mark features to keep
            updated_features = []
            for existing_feature in current_features:
                begin = existing_feature['properties'].get('begin')
                if begin in new_features_dict:
                    existing_feature['properties'].update(new_features_dict[begin]['properties'])
                    existing_feature['geometry'] = new_features_dict[begin]['geometry']
                    updated_features.append(existing_feature)
                    del new_features_dict[begin]  # Remove from new features dict as it's already added

            # Add remaining new features that were not in the existing features
            updated_features.extend(new_features_dict.values())
            
            # Convert back to JSON string
            updated_features_content = json.dumps(updated_features, indent=2)
            
            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(before_features + updated_features_content + after_features)

# Main function to run the update
def main():
    omeka_data = fetch_omeka_data(OMEKA_API_BASE_URL, COLLECTION_ID)
    
    if omeka_data:  # Check if data was fetched successfully
        august_features = create_august_features(omeka_data)
        append_features_to_js(AUGUST_FILE_PATH, august_features)
        
        paths_features = create_paths_features(omeka_data)
        append_features_to_js(PATHS_FILE_PATH, paths_features)
    else:
        print("No data fetched, skipping feature creation and file update.")

if __name__ == "__main__":
    main()
