import requests
import json
import re
import os

# Define the Omeka API URL and the collection ID
OMEKA_API_BASE_URL = "http://georgeeliotarchive.org/api"
COLLECTION_ID = '68'  # Change this to '66' to test with the working collection

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the file paths for the local JSON files relative to the script's directory
AUGUST_FILE_PATH = os.path.join(script_dir, "August1854_2.js")
AUGUST_PATHS_FILE_PATH = os.path.join(script_dir, "Paths_1.js")
SEPTEMBER_FILE_PATH = os.path.join(script_dir, "September1854_3.js")
SEPTEMBER_PATHS_FILE_PATH = os.path.join(script_dir, "Paths_4.js")
OCTOBER_FILE_PATH = os.path.join(script_dir, "October1854_5.js")
OCTOBER_PATHS_FILE_PATH = os.path.join(script_dir, "Paths_6.js")
NOVEMBER_FILE_PATH = os.path.join(script_dir, "November1854_7.js")
NOVEMBER_PATHS_FILE_PATH = os.path.join(script_dir, "Paths_8.js")

# Global variables for feature arrays
august_features = []
september_features = []
october_features = []
november_features = []
august_paths_features = []
september_paths_features = []
october_paths_features = []
november_paths_features = []


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

# Function to create new JSON features for the month data files
def create_features(data):
    global august_features, september_features, october_features, november_features

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

                # Check the month from the Date field
                if 'Date' in item and re.match(r'\d{4}-\d{2}-\d{2}', item['Date']):
                    month = int(item['Date'][5:7])
                    if month == 8:
                        august_features.append(new_feature)
                    elif month == 9:
                        september_features.append(new_feature)
                    elif month == 10:
                        october_features.append(new_feature)
                    elif month == 11:
                        november_features.append(new_feature)

                print("\n")

# Function to create paths features for each month
def create_paths_features(data):
    august_coordinates = []
    september_coordinates = []
    october_coordinates = []
    november_coordinates = []
    
    for item in data:
        if item.get('Coverage'):
            coords = re.findall(r'\d+\.\d+', item['Coverage'])
            if len(coords) == 2:
                if 'Date' in item and re.match(r'\d{4}-\d{2}-\d{2}', item['Date']):
                    month = int(item['Date'][5:7])
                    if month == 8:
                        august_coordinates.append([float(coords[1]), float(coords[0])])
                    elif month == 9:
                        september_coordinates.append([float(coords[1]), float(coords[0])])
                    elif month == 10:
                        october_coordinates.append([float(coords[1]), float(coords[0])])
                    elif month == 11:
                        november_coordinates.append([float(coords[1]), float(coords[0])])
    
    # Create path features for each month
    if august_coordinates:
        august_path_feature = {
            "type": "Feature",
            "properties": {
                "begin": "2",  # Start point index
                "end": "3"     # End point index
            },
            "geometry": {
                "type": "LineString",
                "coordinates": august_coordinates
            }
        }
        august_paths_features.append(august_path_feature)
    
    if september_coordinates:
        september_path_feature = {
            "type": "Feature",
            "properties": {
                "begin": "2",  # Start point index
                "end": "3"     # End point index
            },
            "geometry": {
                "type": "LineString",
                "coordinates": september_coordinates
            }
        }
        september_paths_features.append(september_path_feature)
    
    if october_coordinates:
        october_path_feature = {
            "type": "Feature",
            "properties": {
                "begin": "2",  # Start point index
                "end": "3"     # End point index
            },
            "geometry": {
                "type": "LineString",
                "coordinates": october_coordinates
            }
        }
        october_paths_features.append(october_path_feature)
    
    if november_coordinates:
        november_path_feature = {
            "type": "Feature",
            "properties": {
                "begin": "2",  # Start point index
                "end": "3"     # End point index
            },
            "geometry": {
                "type": "LineString",
                "coordinates": november_coordinates
            }
        }
        november_paths_features.append(november_path_feature)


# Function to write features to JS files
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
        create_features(omeka_data)
        create_paths_features(omeka_data)
        
        # Write features to respective JS files
        write_features_to_js(AUGUST_FILE_PATH, august_features, 'json_August1854_2')
        write_features_to_js(AUGUST_PATHS_FILE_PATH, august_paths_features, 'json_Paths_1')

        write_features_to_js(SEPTEMBER_FILE_PATH, september_features, 'json_September1854_3')
        write_features_to_js(SEPTEMBER_PATHS_FILE_PATH, september_paths_features, 'json_Paths_4')

        write_features_to_js(OCTOBER_FILE_PATH, october_features, 'json_October1854_5')
        write_features_to_js(OCTOBER_PATHS_FILE_PATH, october_paths_features, 'json_Paths_6')

        write_features_to_js(NOVEMBER_FILE_PATH, november_features, 'json_November1854_7')
        write_features_to_js(NOVEMBER_PATHS_FILE_PATH, november_paths_features, 'json_Paths_8')
    else:
        print("No data fetched, skipping feature creation and file update.")

if __name__ == "__main__":
    main()

