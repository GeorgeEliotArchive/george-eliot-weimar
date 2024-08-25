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
        if item.get('Coverage'):
            coordinates = re.findall(r'\d+\.\d+', item['Coverage'])
            print("COORD")
            print(coordinates)
            if len(coordinates) == 2:
                new_feature = {
                    "type": "Feature",
                    "properties": {
                        "Date": item.get('Date', ''),
                        "Location": item.get('Subject', ''),
                        "Description": item.get('Description', ''),
                        "Latitude": float(coordinates[1]),
                        "Longitude": float(coordinates[0])
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(coordinates[1]), float(coordinates[0])]
                    }
                }
                print("NEW FEATURE")
                print(new_feature)
                features.append(new_feature)
    return features

# Function to create a single LineString feature for Paths_1.js
def create_paths_features(data):
    coordinates = []
    for item in data:
        if item.get('Coverage'):
            coords = re.findall(r'\d+\.\d+', item['Coverage'])
            if len(coords) == 2:
                coordinates.append([float(coords[1]), float(coords[0])])
    
    if coordinates:
        new_feature = {
            "type": "Feature",
            "properties": {
                "begin": "2",  # Start point index
                "end": "3"     # End point index
            },
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            }
        }
        return [new_feature]
    else:
        return []

# Function to write new JSON features to JS file
def write_features_to_js(file_path, new_features, variable_name):
    content = {
        "type": "FeatureCollection",
        "name": variable_name,
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": new_features
    }
    
    with open(file_path, 'w') as file:
        file.write(f'var {variable_name} = ')
        json.dump(content, file, indent=4)
        file.write(';')

# Main function to run the update
def main():
    omeka_data = fetch_omeka_data(OMEKA_API_BASE_URL, COLLECTION_ID)
    
    if omeka_data:  # Check if data was fetched successfully
        august_features = create_august_features(omeka_data)
        write_features_to_js(AUGUST_FILE_PATH, august_features, 'json_August1854_2')
        
        paths_features = create_paths_features(omeka_data)
        write_features_to_js(PATHS_FILE_PATH, paths_features, 'json_Paths_1')
    else:
        print("No data fetched, skipping feature creation and file update.")

if __name__ == "__main__":
    main()


