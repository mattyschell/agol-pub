# agol-pub

Simple wrappers to publish data to ArcGIS Online.  Friends these are our wrappers, our rules, the trick is never to be afraid.

We will lovingly wrap [these wrappers](https://developers.arcgis.com/python/latest/api-reference/arcgis.html) of REST calls.


## Requirements

1. ArcGIS Pro installed (ie python _import_ _arcgis_)
2. A user and credentials for the nycmaps arcgis online organization
3. QA requires _import_ _arcpy_

## Replace a File Geodatabase

Copy geodatabase-scripts\sample-replace-cscl-gdb.bat out to a scripts directory, rename it, and update the environmentals.

```shell
C:\gis\geodatabase-scripts>replace-cscl-gdb.bat
``` 

## Test The Code In This Repository

See individual src\py\test-* test cases for sample uses. To run all tests update the environmentals in testall.bat and call it.  The tests expect a dummmy item to exist in the NYCMaps ArcGIS Online organization.

```shell
C:\gis\agol-pub>testall.bat
```