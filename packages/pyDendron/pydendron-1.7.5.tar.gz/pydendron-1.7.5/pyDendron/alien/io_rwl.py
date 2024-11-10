"""
    Import RWL file with text metadata
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"




"""
From TRICYCLE: A UNIVERSAL CONVERSION TOOL FOR DIGITAL MEASURE-RING DATA – SUMMARY OF DENDRO DATA FORMATS

Tucson RWL files begin with three lines of metadata. Strictly these lines should contain structured metadata, but with no software to assist in this, users either only partially stick to these rules, or reject them entirely instead using the three lines as free-text comment lines. The metadata should be set out as follows:
• Line1-Chars1-6SiteID
• Line 1 - Chars 10-61 Site Name
• Line 1 - Chars 62-65 Species Code followed by optional ID number
• Line2-Chars1-6SiteID
• Line 2 - Chars 10-22 State/Country
• Line 2 - Chars 23-30 Species
• Line 2 - Chars 41-45 Elevation
• Line 2 - Chars 48-57 Lat-Long in degrees and minutes, ddmm or dddmm 
• Line 2 - Chars 68-76 1st and last Year
• Line3-Chars1-6SiteID
• Line 3 - Chars 10-72 Lead Investigator
• Line 3 - Chars 73-80 comp. date
Then follows the data lines which are set out as follows:
• Chars 1-8 - Series ID - the series ID should be unique in the file so that it is clear where one series ends and another begins when multiple series are present in the same file.
• Next 4 chars - Year of first value in this row.
• Ten data values consisting of a space character and 5 integers. The file and last data line for a series may have
less than 10 data values so that the majority of lines begin at the start of a decade.
The final data value should be followed by a a stop marker which is either 999 or -9999. When a stop marker of 999 is used this indicates that the integer values in the file are measured in 0.01mm (1/100th mm) units, whereas if a -9999 stop marker is used the units are 0.001mm (microns). The stop marker is therefore used to indicate the end of the data series and the units the data are stored in.
There appears to be no official specification as to how missing rings should be encoded, but the standard notation seems to be to use -999 or 0.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import re
import copy

from pyDendron.dataname import *
from pyDendron.alien.io import IO
from pyDendron.tools.location import reverse_geocode, get_elevation
from pyDendron.app_logger import logger, perror

class IORWL(IO):
    file_extension = ['.rwl', '.crn']
    
    def next_line(self, lines):
        if len(lines) <= 0:
            return None
        line = lines[0]
        lines.pop(0)
        return line
    
    def _read_rwl(self, lines):
        def lat_long(word):
            def decode(str):
                try:
                    min = int(str[-2:]) / 60
                    deg = int(str[:-2])
                    return round(deg + min, 3)
                except Exception as inst:
                    return pd.NA
                
            word = word.upper()
            lat_offset = max(word.find('N'), word.find('S'))
            long_offset = max(word.find('E'), word.find('W'))
            return decode(word[:lat_offset]), decode(word[lat_offset+1:long_offset])
            
        def get_header(lines, meta):
            # Header, line 1
            line = self.next_line(lines)
            if line.startswith('#'):
                return
            meta[PROJECT] = line[0:6].strip()
            # Header, line 2
            line =  self.next_line(lines)
            meta[SITE_COUNTRY] = line[9:22].strip()
            meta[SPECIES] = line[22:30].strip()
            meta[SITE_ELEVATION] = line[40:45].strip()
            meta[SITE_LATITUDE], meta[SITE_LONGITUDE] = lat_long(line[47:59].strip())
            # Header, line 3
            line =  self.next_line(lines)
    
        meta = {}
        series = {}
        #print(lines[:3])
        get_header(lines, meta)
        serie_id = ''

        #print(meta)
            
        for line in lines:
            line = line.strip()
            #print(line)
            if len(line) < 12 or line.startswith('#'):
                continue
            if len(line) > 72:
                line = line[:72]
            tab = line[8:].split()
            if tab[0].startswith('#'):
                continue
            if line[0:8] != serie_id:
                serie_id = line[0:8]
                begin_date = float(tab[0])
                values = []
            values += [float(x) for x in tab[1:]]
            if (values[-1] == 999) or (values[-1] == -9999): # end serie
                d = 1
                if values[-1] == -9999: 
                    d = 10
                values = [np.nan if (x == 999) or (x <= 0) else x/d for x in values[:-1]]
                end_date = begin_date + len(values) - 1
                series[serie_id] = (begin_date, end_date, len(values), np.array(values, dtype='float'))

        return meta, series

    def _localisation(self, meta):
        if (SITE_LATITUDE in meta) and  (SITE_LONGITUDE in meta):
            if self.get_place:
                meta[SITE_COUNTRY], meta[SITE_STATE], meta[SITE_DISTRICT], meta[SITE_TOWN], meta[SITE_ZIP] = reverse_geocode(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.places)
            alt = meta[SITE_ELEVATION]
            if self.get_altitude: 
                meta[SITE_ELEVATION] = get_elevation(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.elevations)
    
    def read_sequences(self, id_parent, lines):
        gmeta, series = self._read_rwl(lines)
        self._localisation(gmeta)
        
        for keycode in series:
            meta = copy.deepcopy(gmeta)
            meta[ID] = self.next_id()
            meta[KEYCODE] = keycode
            meta[CATEGORY] = MEASURE
            meta[DATA_TYPE] = 'raw'
            (meta[DATE_BEGIN], meta[DATE_END], meta[DATA_LENGTH], meta[DATA_VALUES]) = series[keycode]
            self.sequences.append(meta)
            self.components.append({ID_PARENT: id_parent, ID_CHILD: meta[ID]})


                