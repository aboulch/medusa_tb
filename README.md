![Medusa Logo](./doc/logo-medusa-368x118_0.jpg)

# MEDUSA Toolbox

This code provides a common interface in order to download [Sentinel 1 and 2](https://sentinel.esa.int/web/sentinel/home) data using [ESA Scihub](https://scihub.copernicus.eu/).
It is developed in the [MEDUSA project](http://w3.onera.fr/medusa/) at [ONERA](http://www.onera.fr).

## MEDUSA project
The *Multidate Earth observation Datamass for Urban Sprawl Aftercase* (MEDUSA) project is designed to bring together and promote processing of remote sensing images in the current context of big data, with a focus on developing a demonstrator

The project website is hosted at http://w3.onera.fr/medusa/.

## What for ?

This code is based on the python package [sentinelsat](http://sentinelsat.readthedocs.io) for downloading sentinel products.
It provide a simple interface to download sentinel 1 and 2 data and then crop the prodicts according to a geojson geometry.

## Getting geojson area
Many websites provide geojson, [geojson.io](geojson.io) is one of them.

## Documentation

Date and Scihub ids must be filled in the **data.json**.
Sentinel sensor (1 or 2) is an option.

#### sentinel download


```
python sentinel_download --sentinel 1 --data path_to_data_file --geojson path_area_geojson
```

#### sentinel crop

```
python sentinel_crop --sentinel 1 --archive path_to_archive_ZIP --geojson path_area_geojson
```

Note that SenitnelSat provides much more download functionalities.
[sentinelsat documentation](http://sentinelsat.readthedocs.io)
