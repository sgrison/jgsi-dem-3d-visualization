JGSI XML DEM are downloaded from https://fgd.gsi.go.jp/download/menu.php.

JGSI XML DEM are converted to GeoTIFF using [gpxz's jpgis-dem library](https://github.com/gpxz/jpgis-dem). Raster is rescaled using Raster Calculator : (raster+15)*50.

QGis is used to merge GeoTIFF and [export a STL 3D model](https://youtu.be/0DRiqX20-68?si=bcVnkgaK5_jscTxQ).
