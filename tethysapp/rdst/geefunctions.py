import ee, logging
from ee.ee_exception import EEException 

logger = logging.getLogger(__name__)
try:
	ee.Initialize()

except EEException as e:
	print("Failed to Initialize google earth engine. Error is: "+ str(e))

def imageToMapId(imageName, visParams={}):
    """  """
    try:
        eeImage = ee.Image(imageName)
        mapId = eeImage.getMapId(visParams)
        return {
        	'url': mapId['tile_fetcher'].url_format
        }
    except EEException as e:
    	logger.error("******imageToMapId error************", sys.exc_info()[0])
    return {
    	'errMsg':str(sys.exc_info()[0])
    }

def getMap(collectionName, visParams={}, reducer='mosaic', time_start=None, time_end=None):
    try:
        values = None
        eeCollection = ee.ImageCollection(collectionName).select('NDVI')
        if (time_start and time_end):
            eeFilterDate = ee.Filter.date(time_start, time_end)
            eeCollection = eeCollection.filter(eeFilterDate)
        if(reducer == 'min'):
            values = eeCollection.min().getMapId(visParams)
        elif (reducer == 'max'):
            values = eeCollection.max().getMapId(visParams)
        elif (reducer == 'mosaic'):
            values = eeCollection.mosaic().getMapId(visParams)
        else:
            values = eeCollection.mean().getMapId(visParams)
        
    except EEException as e:
        print(str(e))
        print(str(sys.exc_info()[0]))
        raise Exception(sys.exc_info()[0])
    #tile_url_template = values[:-12]+"{z}/{x}/{y}"
    #return values
    return values['tile_fetcher'].url_format

def clippedMap(collectionName, visParams={}, reducer='mosaic', time_start=None, time_end=None, county=None):
    try:
        values = None
        fc = ee.FeatureCollection('users/kimlotte423/kenya_counties').select('ADM1_EN')
        cty = fc.filter(ee.Filter.eq('ADM1_EN', county))
        eeCollection = ee.ImageCollection(collectionName).select('NDVI')
        if (time_start and time_end):
            eeFilterDate = ee.Filter.date(time_start, time_end)
            eeCollection = eeCollection.filter(eeFilterDate)
        values = eeCollection.mosaic().clip(cty).getMapId(visParams)

    except EEException as e:
        print(str(sys.exc_info()[0]))
        raise Exception(sys.exc_info()[0])

    return values['tile_fetcher'].url_format