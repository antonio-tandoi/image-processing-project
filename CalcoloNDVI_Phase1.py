import ee, ee.mapclient

#-----DEFINIZIONE FUNZIONI
def NDVI_calc(image):
    return image.addBands(image.normalizedDifference(['B8', 'B4']))

#-----DEFINIZIONE AREA DI INTERESSE E PUNTI DI STUDIO
###ROI

area = ee.Geometry.Polygon([[15.374081, 41.686399], [16.146577, 41.686399],
                            [15.374081, 41.371181], [16.146577, 41.371181]])
ndviPalette = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'black']}

###CAMPI IRRIGATI E NON IRRIGATI
punti_irrigati = [
    ee.Feature(ee.Geometry.Point(15.616944, 41.508055).buffer(300), {'name': 'Irrigato 1'}),
    ee.Feature(ee.Geometry.Point(15.745277, 41.561388).buffer(300), {'name': 'Irrigato 2'}),
    ee.Feature(ee.Geometry.Point(15.475277, 41.615555).buffer(300), {'name': 'Irrigato 3'}),
    ee.Feature(ee.Geometry.Point(15.652222, 41.429722).buffer(300), {'name': 'Irrigato 4'}),
    ]

punti_nirrigati = [
    ee.Feature(ee.Geometry.Point(15.566944, 41.496111).buffer(300), {'name': 'Non Irrigato 1'}),
    ee.Feature(ee.Geometry.Point(15.571666, 41.528055).buffer(300), {'name': 'Non Irrigato 2'}),
    ee.Feature(ee.Geometry.Point(15.860833, 41.441111).buffer(300), {'name': 'Non Irrigato 3'}),
    ee.Feature(ee.Geometry.Point(15.854166, 41.491944).buffer(300), {'name': 'Non Irrigato 4'}),
  ]

lista_irr = ee.FeatureCollection(punti_irrigati)
lista_nir = ee.FeatureCollection(punti_nirrigati)


#INTERROGAZIONE SATELLITE
###Collezione Novembre2017
collection_nov = (ee.ImageCollection('COPERNICUS/S2')
               .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 60)) 
               .filterDate('2017-11-01', '2017-11-30')
               .filterBounds(area))
 
###Collezione Maggio2018
collection_mag = (ee.ImageCollection('COPERNICUS/S2')
               .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 40)) 
               .filterDate('2018-05-01', '2018-05-31')
               .filterBounds(area))
               
###Collezione Luglio2018
collection_lul = (ee.ImageCollection('COPERNICUS/S2')
               .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 40)) 
               .filterDate('2018-07-01', '2018-07-31')
               .filterBounds(area))
 
###Collezione Agosto2019
collection_ago = (ee.ImageCollection('COPERNICUS/S2')
              .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 40)) 
              .filterDate('2019-08-01', '2019-08-31')
              .filterBounds(area))
 
 
#SEZIONE 5 - CALCOLO NDVI
###Applicazione della banda NDVI a ogni immagine della collezione 
img_nov = collection_nov.map(NDVI_calc)
img_mag = collection_mag.map(NDVI_calc)
img_lul = collection_lul.map(NDVI_calc)
img_ago = collection_ago.map(NDVI_calc)
 
###Creazione di collezioni di immagini fatte solo di NDVI
NDVI_nov = img_nov.select(['nd'])
NDVI_mag = img_mag.select(['nd'])
NDVI_lul = img_lul.select(['nd'])
NDVI_ago = img_ago.select(['nd'])
 
###Calcolo mediana di ogni collezione
NDVImed_nov = NDVI_nov.median();
NDVImed_mag = NDVI_mag.median();
NDVImed_lul = NDVI_lul.median();
NDVImed_ago = NDVI_ago.median();
 
###Calcolo media delle mediane
NDVImedtot = (NDVImed_nov.add(NDVImed_mag.add(NDVImed_lul.add(NDVImed_ago)))).divide(4)
NDVImedtot = NDVImedtot.gt(0.35)
 
print(" Novembre: ",collection_nov.size().getInfo(), "immagini")
print(" Maggio: ",collection_mag.size().getInfo(), "immagini")
print(" Luglio: ",collection_lul.size().getInfo(), "immagini")
print(" Agosto: ",collection_ago.size().getInfo(), "immagini")

ee.mapclient.centerMap(15.7151226, 41.5049459, 11)
ee.mapclient.addToMap(NDVImedtot.gt(0.35), ndviPalette)
ee.mapclient.addToMap(lista_irr, {'color': 'blue'}, 'colored')
ee.mapclient.addToMap(lista_nir, {'color': 'red'}, 'colored')
    