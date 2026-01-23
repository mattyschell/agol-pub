import arcpy
import csv
import sys
import re

# sometimes metadata lovers wish to ogle the metadata in a geodatabase
# these lovers do not love the GUI so much
# what they do love is a spreadsheet
# this here extracts all metadata from a geodatabase
#    (all = tables, fcs see getallobjects() below)
# and outputs a .csv for ogling
# its in this repo because publishing to AGOL without metadata is bad
# 
# set GDB=C:\Temp\abc.gdb
# set CSV=C:\Temp\metadata-abc.csv
# set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
# CALL %PROPY% %BASEPATH%\extract-metadata.py %GDB% %CSV%


def get_relationshipclasses(workspace):

    relclasses = []
    walk = arcpy.da.Walk(workspace
                        ,datatype="RelationshipClass")

    for dirpath, dirnames, filenames in walk:
        for relationshipclass in filenames:
            relclasses.append(relationshipclass)

    return relclasses

def get_topologies(workspace):

    # consider combining all of these to limit arcpy.da.Walk calls
    topologies = []
    walk = arcpy.da.Walk(workspace
                        ,datatype="Topology")

    for dirpath, dirnames, filenames in walk:
        for topology in filenames:
            topologies.append(topology)

    return topologies

def get_tables():

    return arcpy.ListTables()

def get_feature_datasets():
    
   return arcpy.ListDatasets()

def get_feature_classes():

    feature_classes = arcpy.ListFeatureClasses()

    for dataset in arcpy.ListDatasets():
        dataset_fcs = arcpy.ListFeatureClasses(feature_dataset = dataset)

        #add feature classes to ongoing list
        for fc in dataset_fcs:
            feature_classes.append(fc)

    return feature_classes

def getallobjects(workspace):

    return get_tables() + get_feature_classes() 
         #+ get_feature_datasets() \
         #+ get_feature_classes() \
         #+ get_relationshipclasses(workspace) \
         #+ get_topologies(workspace)


if __name__ == '__main__':

    gdb_in = sys.argv[1]
    csv_out = sys.argv[2]

    arcpy.env.workspace = gdb_in

    existingobjects = getallobjects(arcpy.env.workspace)

    # List to store metadata
    metadata_list = []
    

    for existingobject in existingobjects:

        metadata = {}
        # Get the metadata object
        metadata_obj = arcpy.metadata.Metadata(existingobject)

        metadata['object'] = existingobject
        metadata['summary'] = metadata_obj.summary if metadata_obj.summary else 'N/A'
        metadata['description'] = metadata_obj.description if metadata_obj.description else 'N/A'
        metadata['cleandescription'] = re.sub(r'<.*?>', '', metadata['description'])


        metadata_list.append(metadata)

    with open(csv_out, 'w', newline='') as csvfile:
        fieldnames = ['object', 'summary', 'description', 'cleandescription']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in metadata_list:
            writer.writerow(data)
