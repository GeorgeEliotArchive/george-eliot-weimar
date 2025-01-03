# George Eliot in Weimar

Welcome! The **George Eliot in Weimar Geospatial Overview**, created with QGIS, HTML, JavaScript, and Python, is designed to be “software-free” upon its release. This project connects to the George Eliot Archive’s Omeka server and implements a Python script that runs once a day to make relevant updates to items on the map if their metadata has changed within the “GE in Weimar” Omeka metadata collection. 

Additionally, the **George Eliot in Weimar Geospatial Narrative**, created with GeoStory and GeoNode, allows a story-like experience for George Eliot Archive visitors. Making edits to this project is outside of the scope of this repository.

## Overview
To update any aspect of a location—-whether it be coordinates, images, or anything else—-Archive editors can simply update the data for an entry in Omeka. This guide provides instructions on managing entries in Omeka, including adding or changing items, and explains how to manually update the QGIS map in GitHub if automatic updates fail.

*Note: a more detailed guide with images can be found in this project's official Box folder. Please email Dr. Beverley Park Rilett for access.*

## How to Update an Item in Omeka

### Step 1: Locate the Most Recent CSV Export
1. Go to the project's official Box folder.
2. Navigate to:
   - `Mapping Resources` > `Metadata` > `MostRecentProjectCSVExport`.
3. Download the CSV or Excel file for reference.

**Tip:** Use Excel’s **sort** feature to easily find entries related to a particular location or metadata field.

### Step 2: Adding or Changing Items in Omeka
1. Upload the image/video to the project’s official Box folder:
   - `Mapping Resources` > `Media` > `QGISMediaResources`.
2. Use the naming convention followed by existing items.
3. Log in to [georgeeliotarchive.org/admin](https://georgeeliotarchive.org/admin). Contact Dr. Rilett if you do not have an account.
4. Navigate to **Collections** > **George Eliot’s Weimar 1854**.
   - To view individual items, click the link under **Total Number of Items** (this text for the link you click on should be a number).
   - To edit items, find the item you want to modify and click the link that says **Edit** under that item.
   - To add a new item, click **Add an Item**.

5. Use the **Dublin Core** tab to add or edit the following fields (use entries that already exist in Omeka as a guide for formatting these fields):
   - **Title**: Descriptive title detailing the context behind a stop George Eliot made.
   - **Subject**: The name of the location Eliot visited.
   - **Description**: Journal entry or literary evidence describing Eliot’s visit.
   - **Creator**: The creator of the media item.
   - **Source**: The address of the media item uploaded to Omeka.
   - **Publisher**: George Eliot Archive.
   - **Date**: Date Eliot visited the location.
   - **Rights**: Copyright license associated with the media item, with the default as CC BY-NC-SA 4.0
   - **Relation**: The work from which the description was quoted.
   - **Format**: Type of media (Image or Video).
   - **Type**: The order in which Eliot visited locations on a given day.
   - **Identifier**: Box link to the media item in the project’s Box folder.
   - **Coverage**: Geolocation (latitude and longitude) of the location Eliot visited.

6. After updating the **Dublin Core** items:
   - Go to **Item Type Metadata** and enter the name of the resource into **Original Format** (this name should be the same as the name of the file in the project Box folder).
   - Upload the media resource under **Files** and click **Save Changes**.

7. Make sure that all changes made are reflected manually in the GeoStory project as well. To make changes, simply login to the GeoStory project and manually make updates, implementing any modifications you made in Omeka. To learn how to use GeoStory, which includes making manual changes to GeoCarousel entries and other items included in the project GeoStory, please reference the official [GeoNode Documentation.](https://docs.geonode.org/en/master/usage/geostory/index.html)

8. Likewise, if you update an item in GeoStory, make sure the update is reflected in Omeka. For example, the text entries under the videos in the GeoStory project are stored in the corresponding video's Omeka entry. Make sure that if you update the text in GeoStory, you update the same text in its corresponding Omeka entry, and vice versa.

**Important**: If you change a media item, make sure to update `Creator`, `Source`, `Rights`, `Format`, and `Identifier`. If you add a new item to a given date, adjust **Type** values accordingly.

## Manually Updating the Map in GitHub

If automatic updates fail due to network or software issues, manual updates can be made using the following steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/GeorgeEliotArchive/george-eliot-weimar.git
    ```
2. Change to the project directory:
    ```bash
    cd george-eliot-weimar
    ```
3. Run the update script:
    ```bash
    python3 QGIS/data/updateData.py
    ```
4. Prepare changes:
    ```bash
    git add .
    ```
5. Commit changes:
    ```bash
    git commit -m “initiated update script”
    ```
6. Push changes to GitHub:
    ```bash
    git push origin main
    ```

## Contributing
Only members of the George Eliot Archive Team, directed by Dr. Beverley Park Rilett at Auburn University (bdr0032@auburn.edu), are allowed to edit this project. If you encounter any issues or have suggestions for improvements, feel free to open an issue or create a pull request in the [project repository](https://github.com/GeorgeEliotArchive/george-eliot-weimar).
