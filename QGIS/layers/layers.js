var wms_layers = [];


        var lyr_OSMStandard_0 = new ol.layer.Tile({
            'title': 'OSM Standard',
            //'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: ' &middot; <a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors, CC-BY-SA</a>',
                url: 'http://tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
        });
var format_Paths_1 = new ol.format.GeoJSON();
var features_Paths_1 = format_Paths_1.readFeatures(json_Paths_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_Paths_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_Paths_1.addFeatures(features_Paths_1);
var lyr_Paths_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_Paths_1, 
                style: style_Paths_1,
                popuplayertitle: "Paths",
                interactive: true,
                title: '<img src="styles/legend/Paths_1.png" /> Paths'
            });
var format_DestinationsTest_2 = new ol.format.GeoJSON();
var features_DestinationsTest_2 = format_DestinationsTest_2.readFeatures(json_DestinationsTest_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_DestinationsTest_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_DestinationsTest_2.addFeatures(features_DestinationsTest_2);
var lyr_DestinationsTest_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_DestinationsTest_2, 
                style: style_DestinationsTest_2,
                popuplayertitle: "DestinationsTest",
                interactive: true,
                title: '<img src="styles/legend/DestinationsTest_2.png" /> DestinationsTest'
            });

lyr_OSMStandard_0.setVisible(true);lyr_Paths_1.setVisible(true);lyr_DestinationsTest_2.setVisible(true);
var layersList = [lyr_OSMStandard_0,lyr_Paths_1,lyr_DestinationsTest_2];
lyr_Paths_1.set('fieldAliases', {'begin': 'begin', 'end': 'end', });
lyr_DestinationsTest_2.set('fieldAliases', {'Date': 'Date', 'Name': 'Name', 'Latitude': 'Latitude', 'Longitude': 'Longitude', 'Photos': 'Photos', });
lyr_Paths_1.set('fieldImages', {'begin': 'TextEdit', 'end': 'TextEdit', });
lyr_DestinationsTest_2.set('fieldImages', {'Date': 'TextEdit', 'Name': 'TextEdit', 'Latitude': 'TextEdit', 'Longitude': 'TextEdit', 'Photos': 'TextEdit', });
lyr_Paths_1.set('fieldLabels', {'begin': 'no label', 'end': 'no label', });
lyr_DestinationsTest_2.set('fieldLabels', {'Date': 'inline label - always visible', 'Name': 'no label', 'Latitude': 'hidden field', 'Longitude': 'hidden field', 'Photos': 'no label', });
lyr_DestinationsTest_2.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});