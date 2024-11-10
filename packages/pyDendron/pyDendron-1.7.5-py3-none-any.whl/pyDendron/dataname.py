"""
Data Name
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"





import pandas as pd
import numpy as np
import copy


#--------------------------
# Dateset

## Categories
MEAN = 'Mean'
MEASURE = 'Measure'
SET = 'Set'
CATEGORIES = [MEAN, MEASURE, SET]

## Root in dataset
ROOT = -10
WORKSHOP = -20
CLIPBOARD = -30
TRASH = -40

## Dateset output keys (json, excel)
SEQUENCES = 'sequences'
COMPONENTS = 'components'
PACKAGES = 'packages'
VERSION = 'version'
LOG = 'log'
CROSSDATING = 'crossdating'

## Crossdating fileds
CROSSDATING_DATE = 'Crossdating Date'

## dataset check method
OFFSET_NORM = 'OffsetNorm'
DATE_BEGIN_NORM = 'BateBeginNorm'

## Components
### Components fileds
ID_PARENT = 'IdParent'
ID_CHILD = 'IdChild'
OFFSET = 'Offset'

### Components index
components_index = [ID_PARENT, ID_CHILD]

### Components type dictonary
components_dtype_dict = {
    OFFSET: 'Int32'
}

### Components columns list
components_cols = list(components_dtype_dict.keys())

### Components type list
components_dtype = list(components_dtype_dict.values())

## Sequences 
### Sequence fileds
ID = 'Id'
LABORATORY_CODE = 'LaboratoryCode'
PERS_ID = 'PersId'
PROJECT = 'Project'
KEYCODE = 'Keycode'
KEYCODE_MASTER = 'KeycodeMaster'
KEYCODE_PARENT = 'KeycodeParent'
SPECIES = 'Species'
SITE_LATITUDE = 'Latitude'
SITE_LONGITUDE = 'Longitude'
SITE_ELEVATION = 'Elevation'
SITE_CODE = 'SiteCode'
BIBLIOGRAPHY_CODE = 'BibliographyCode'
DATE_BEGIN = 'DateBegin'
#DATE_BEGIN_MASTER = 'DateBeginMaster'
DATE_END = 'DateEnd'
#SYNC = 'Sync'
DATE_BEGIN_ESTIMATED = 'DateBegin'
DATE_END_ESTIMATED = 'DateEnd'
CREATION_DATE = 'CreationDate'
DATE_SAMPLING = 'DateOfSampling'
CATEGORY = 'Category'
SUBCATEGORY = 'Subcategory'
MEANAS_MEASURE = 'MeanAsMeasure'
SAPWOOD = 'Sapwood' # not in data
PITH = 'Pith'
CAMBIUM = 'Cambium'
CAMBIUM_SEASON = 'CambiumSeason'
BARK = 'Bark'
COMMENTS = 'Comments'
URI = 'URI'
DATA_LENGTH = 'DataLength'
DATA_TYPE = 'DataType' 
DATA_VALUES = 'DataValues'
DATA_WEIGHTS = 'DataWeights'
DATA_INFO = 'DataInfo'
DATA_SIGNATURES = 'DataSignatures'
INCONSISTENT = 'Inconsistent'
TAG = 'Tag'
COMPONENT_COUNT = 'ComponentCount'

### Sequence index
sequences_index = [ID]

### Sequence type dictonary
sequences_dtype_dict = {
    KEYCODE: 'string', PROJECT: 'string', 
    SPECIES: 'string', 
    CATEGORY: 'string', SUBCATEGORY: 'string', 
    MEANAS_MEASURE : 'boolean',
    DATE_BEGIN: 'Int32', DATE_END: 'Int32', 
    SITE_LATITUDE: 'Float32', SITE_LONGITUDE: 'Float32', SITE_ELEVATION: 'Float32',
    SITE_CODE: 'string',
    PITH: 'boolean', 
    SAPWOOD: 'Int32', 
    CAMBIUM: 'boolean', 
    CAMBIUM_SEASON: 'string', 
    BARK: 'boolean', 
    CREATION_DATE: 'datetime64[ns]',
    DATE_SAMPLING : 'datetime64[ns]',
    LABORATORY_CODE : 'string',
    PERS_ID : 'string',
    BIBLIOGRAPHY_CODE : 'string',
    COMMENTS: 'string',
    URI: 'string',
    DATA_LENGTH : 'Int32', DATA_TYPE : 'string', DATA_VALUES : 'object',
    DATA_WEIGHTS : 'object', DATA_INFO : 'object', DATA_SIGNATURES : 'object',
    INCONSISTENT : 'boolean',
    TAG: 'string',
    COMPONENT_COUNT: 'Int32',
    
}

### Sequence columns list
sequences_cols = list(sequences_dtype_dict.keys())
### Sequence type list
sequences_dtype = list(sequences_dtype_dict.values())

## dataset log
### dataset log fileds
COLUMN = 'ColumnName'
DATE = 'UpdateDate'
NEWVALUE = 'NewValue'
OLDVALUE = 'OldValue'
USERNAME = 'UserName'

### dataset log dtype
log_dtype = {
    DATE: 'datetime64[ns]',
    ID_CHILD: 'Int32',
    ID_PARENT: 'Int32',
    COLUMN : 'String',
    OLDVALUE : 'object',
    NEWVALUE : 'object',
    USERNAME : 'String',
    COMMENTS: 'string',
}

#--------------------------
# Detrend

## Detrend methods
HANNING = 'Hanning'
HAMMING = 'Hamming'
BARTLETT = 'Bartlett'
BLACKMAN = 'Blackman'
RECTANGULAR = 'Rectangular'
BESANCON = 'Besancon (classic)'
BESANCON1 = 'besancon (log at the end)'
BP73 = 'BP73'
SPLINE = 'Spline'
SLOPE = 'Slope'
RAW = 'Raw'
CORRIDOR = 'Corridor (polynome)'
CORRIDOR_SPLINE = 'Corridor (spline)'
DELTA = 'Delta (first derivative)'
DELTADELTA = 'DeltaDelta (second derivative)'
LOG = 'log'

## detrend list
detrend_types = [RAW, HANNING, HAMMING, BARTLETT, BLACKMAN, RECTANGULAR, BESANCON, BESANCON1, 
             BP73, SPLINE, SLOPE, CORRIDOR, DELTA, DELTADELTA, LOG]

## detrend parameter fileds
DETREND = 'Detrend'
DETREND_WSIZE = 'Detrend Window Size'
DETREND_LOG = 'Detrend Log'

#--------------------------
# Mean

## Mean parameter fileds
MEANDATE_AS_OFFSET = 'Mean Date as Offset'
BIWEIGHT_MEAN = 'Biweight Mean'

#--------------------------
# CrossDating

## CrossDating fileds

ID_MASTER = 'IdMaster'
CORR_OVERLAP = 'r overlap'
GLK_OVERLAP = 'glk overlap'
DIST_OVERLAP = 'd overlap'

CORRELATION = 'correlation'
SYNC = 'Sync'

CORR = 'r'
GLK = 'glk'
#DIST = 'distance' 

T_SCORE = 't-score' 
Z_SCORE = 'z-score'

T_RANK= 't-rank'
Z_RANK= 'z-rank'
D_RANK= 'd-rank'

ZP_VALUE = 'zp-value'
TP_VALUE = 'tp-value'

CORR_OVERLAP_NAN = 'r Nnan'
GLK_OVERLAP_NAN = 'glk Nnan'
DIST_OVERLAP_NAN = 'd Nnan'

#PV = 'PV'
DCG = 'DCG'
AGC = 'agc'
SSGC = 'ssgc'
SGC = 'sgc'

COSINE = 'cosine'
EUCLIDEAN = '-1 x euclidean'
CITYBLOCK = '-1 x cityblock'
DISTANCE = 'distance'

crossdating_method = [CORRELATION, GLK, DISTANCE]
crossdating_distance = [COSINE, CITYBLOCK, EUCLIDEAN]

#--------------------------
# Location
SITE_COUNTRY = 'SiteCountry'
SITE_STATE = 'SiteState'
SITE_DISTRICT = 'SiteDistrict'
SITE_TOWN = 'SiteTown'
SITE_ZIP = 'SiteZipcode'

#--------------------------
# Drawing
HEARTWOOD = 'Heartwood'
MISSING_RING_BEGIN = 'MissingRingBegin'
MISSING_RING_END = 'MissingRingEnd'
CAMBIUM_BOUNDARIES = 'CambiumBoundaries'

CAMBIUM_ESTIMATED = 'CambiumEstimated'
CAMBIUM_LOWER = 'CambiumLower'
CAMBIUM_UPPER = 'CambiumUpper'

#PITH_ABSENT = 'PithAbsent'
PITH_ESTIMATED = 'PithEstimated'
PITH_LOWER = 'PithLower'
PITH_UPPER = 'PithUpper'

#--------------------------
# Treeview Tabulator

# Treeview Tabulator specific columns
ICON = 'Icon'
DATE_END_CE = '[B]CEEnd'
DATE_BEGIN_CE = '[B]CEBegin'

# Treeview Tabulator column types
dtype_view = sequences_dtype_dict.copy()
dtype_view.update(components_dtype_dict)
dtype_view[ICON] = 'string'
dtype_view[ID_CHILD] = 'Int32'
dtype_view[ID_PARENT] = 'Int32'
dtype_view[KEYCODE_PARENT] = 'string'
dtype_view[DATE_BEGIN_CE] = 'string'
dtype_view[DATE_END_CE] = 'string'

# Treeview Tabulator tips
dtips_view = {
    KEYCODE: 'A string that identifies the sequence, should be unique.', 
    PROJECT: 'A string that identifies the project associated to the serie. Free text.', 
    SPECIES: 'The species code, use the ITRDB code.', 
    CATEGORY: 'The value is Measure, Mean or Set. Measure is a serie of ring width, Mean is a set of serie with a mean, Set is a set of serie.', 
    SUBCATEGORY: 'The subcategory is a free text. Could be Master Chronology, Regional Chronology, Local Chronology, Site Chronology, etc.', 
    MEANAS_MEASURE: 'The mean is considered as a measure. Detrend is apply on the mean',
    DATE_BEGIN: 'The date of the first ring, in year.', 
    DATE_END: 'The date of the last ring, in year.', 
#    SYNC: 'The date is certain if True else unknown or uncertain.', 
    SITE_LATITUDE: 'The latitude of the site location.', 
    SITE_LONGITUDE: 'The longitue of the site location.', 
    SITE_ELEVATION: 'The elevation of the site location.',
    SITE_CODE: 'The code or name of the site.',
    PITH: 'a boolean that indicates if the pith is present.', 
    #PITH_ABSENT: '?',
    SAPWOOD: 'The position of the sapwood in the serie.', 
    CAMBIUM: 'A boolean that indicates if the cambium is present.', 
    CAMBIUM_SEASON: 'The season (spring or summer) of the cambium.', 
    BARK: 'A boolean that indicates if the bark is present.', 
    CREATION_DATE: 'The date of the creation of the serie.',
    DATE_SAMPLING : 'The date of the sampling of the serie.',
    LABORATORY_CODE : 'The code of the laboratory that has produced the serie.',
    PERS_ID : 'The id of the person that has produced the serie.',
    BIBLIOGRAPHY_CODE : 'A reference to a bibliography.',
    COMMENTS: 'Free text comments.',
    URI: 'A link to a file or a web page that explains the serie.',
    DATA_LENGTH : 'The number of rings in the serie.', 
    DATA_TYPE : 'The type of the data. It must be "RAW" in the tree and a detrend type in other cases.', 
    DATA_VALUES : 'The width of the rings.',
    DATA_WEIGHTS : 'The weight of each ring. 1 for each Tree rings, the number of trees at each Mean rings.', 
    DATA_INFO : 'List of pairs (Id, Offset) for each component in the Mean.',
    DATA_SIGNATURES : 'List of signatures for each component in the Mean.',
    INCONSISTENT : 'A boolean indicating whether the series is inconsistent: data errors/offsets, Mean component changes.',
    TAG: 'Use to group series in a plot.',
    COMPONENT_COUNT: 'Number of components in the Mean.',
}



#--------------------------
# Excel Columns OUTPUT

excel_columns = [KEYCODE, PROJECT, SPECIES, CATEGORY, SUBCATEGORY, MEANAS_MEASURE, DATE_BEGIN, DATE_END,
                 SITE_LATITUDE, SITE_LONGITUDE, SITE_ELEVATION, SITE_CODE, 
                 PITH, SAPWOOD, CAMBIUM, CAMBIUM_SEASON, BARK, 
                 DATA_LENGTH, DATA_TYPE, DATA_SIGNATURES, COMPONENT_COUNT]


#--------------------------
# Statistics

## Statistics fileds
DATA_NAN = 'NbMissingRing'
STAT_MEAN = 'Mean'
STAT_MEDIAN= 'Median'
STAT_MODE= 'Mode'
STAT_STD= 'STD'
STAT_VAR= 'Variance'
STAT_MIN= 'Minimum'
STAT_MAX= 'Maximum'
STAT_PERC25= 'Percentil 25'
STAT_PERC50= 'Percentil 50'
STAT_PERC75= 'Percentil 75'
STAT_SUM= 'Sum'
STAT_KURTOSIS= 'Kurtosis'
STAT_SKEWNESS= 'Skewness'
STAT_ENTROPY= 'Entropy'
#STAT_NORM= 'Norm'

## Statistics type dictonary
stat_dtype_dict = {
    DATA_NAN: 'Int32',
    STAT_MEAN: 'Float32',
    STAT_MEDIAN: 'Float32',
    STAT_MODE: 'Float32',
    STAT_STD: 'Float32',
    STAT_VAR: 'Float32',
    STAT_MIN: 'Float32',
    STAT_MAX: 'Float32',
    STAT_PERC25: 'Float32',
    STAT_PERC50: 'Float32',
    STAT_PERC75: 'Float32',
    STAT_SUM: 'Float32',
    STAT_KURTOSIS: 'Float32',
    STAT_SKEWNESS: 'Float32',
    STAT_ENTROPY: 'Float32',
    #STAT_NORM: 'Float32',
}

detrend_dtype_dict = {
    #PITH_ESTIMATED: 'Int32',
    #PITH_LOWER: 'Int32',
    #PITH_UPPER: 'Int32',
    CAMBIUM_ESTIMATED: 'Int32',
    CAMBIUM_LOWER: 'Int32',
    CAMBIUM_UPPER: 'Int32',
    SLOPE : 'object',
}

#--------------------------
# Package Tabulator
ADD_STATISTICS = False
dtype_package = copy.deepcopy(dtype_view)

dtype_package.update(detrend_dtype_dict)
if ADD_STATISTICS:  
    dtype_package.update(stat_dtype_dict)

