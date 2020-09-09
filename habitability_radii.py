# functions for determining the habitability zone of a given star
# using calculations described here: https://www.planetarybiology.com/calculating_habitable_zone.html
# for use with the Gaia 2 dataset as is, no alterations

import pandas as pd
import math as m

df = pd.read_csv("DATA FRAME GOES HERE")

# get value of various stats for a given star
# both designation and column_name must be inputted as strings
def value(designation, column_name):
    return df.loc[df['designation'] == designation, column_name].values[0]

# spectral class function
# determine which spectral class host star is using temperature
def star_class(temp):
    if K >= 30000:
        return 'O'
    elif (K >= 10000) & (K < 30000):
        return 'B'
    elif (K >= 7500) & (K < 10000):
        return 'A'
    elif (K >= 6000) & (K < 7500):
        return 'F'
    elif (K >= 5200) & (K < 6000):
        return 'G'
    elif (K >= 3700) & (K < 5200):
        return 'K'
    elif (K >= 2400) & (K < 3700):
        return 'M'
    else:
        return None

# determine bolometric correction constant based on spectral class
def bolometric_constant(star_class):
    if star_class == 'B':
        return -2.0
    elif star_class == 'A':
        return -0.3
    elif star_class == 'F':
        return -0.15
    elif star_class == 'G':
        return -0.4
    elif star_class == 'K':
        return -0.8
    elif star_class == 'M':
        return -2.0
    else:
        return None

# calculate inner and outer radii of habitability zone
# function returns a list with the inner radius as the first value and the outer radius as the second
def habitability_radii(designation):
    try:
        # classify star, using teff_val (effective temperature) as classification stat
        # O type stars have effectively no habitability zone
        # too hot and short lived to allow life to evolve, despite it allowing water to be liquid at some distances
        star_type = temp_class(value(designation, 'teff_val'))
        if star_type == 'O':
            return None

        # determine absolute magnitude
        apparent_mag = -2.5 * m.log10(value(designation, 'phot_g_mean_mag'))
        distance = 1 / (value(designation, 'parallax') * 1000)
        absolute_mag = apparent_mag - 5 * m.log10(distance)

        # calculate bolometric magnitude
        bc = class_constant(star_type)
        bolometric_mag = absolute_mag + bc

        # calculate absolute luminosity of star
        sun_bolometric_mag = 4.75
        absolute_lum = m.pow(10, ((bolometric_mag - sun_bolometric_mag) / -2.5))

        # approximate radii
        # near radii (in AU)
        inner_radius = m.sqrt((absolute_lum / 1.1))
        outer_radius = m.sqrt((absolute_lum / 0.53))

        return [inner_radius, outer_radius]
    except:
        return None
