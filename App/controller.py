﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    loadArtist(catalog)
    loadAdworks(catalog)

def loadArtist(catalog):
    artists_file = cf.data_dir + "Artists-utf8-large.csv"
    input_file = csv.DictReader(open(artists_file, encoding="utf-8"))

    for artist in input_file:
        model.addArtist(catalog, artist)


def loadAdworks(catalog):
    artworks_file = cf.data_dir + "Artworks-utf8-large.csv"
    input_file2 = csv.DictReader(open(artworks_file, encoding="utf-8"))

    for artwork in input_file2:
        model.addArtwork(catalog,artwork)

#Funciones de Consulta

def ArtistbyBeginDate(catalog, min, max):
    return model.ArtistbyBeginDate(catalog, min, max)

def ArtworksbyMedium(catalog,Name,n):
    return model.ArtworksbyMedium(catalog,Name,n)

def ArtworksbyNationality(catalog,Nation):
    return model.ArtworksbyNationality(catalog,Nation)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
