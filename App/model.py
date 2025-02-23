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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from math import atan2
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mg
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todos los libros

    Se crean indices (Maps) por los siguientes criterios:
    Autores
    ID libros
    Tags
    Año de publicacion

    Retorna el catalogo inicializado.
    """
    catalog = {'Artists': None,
               'Artworks': None,
               'Constituen ID': None,
               'tags': None,
               'tagIds': None,
               'years': None}

    
    catalog['Artists'] = lt.newList('ARRAY_LIST', compareArtistIds)
    catalog['Artworks'] = lt.newList('ARRAY_LIST', compareArtworksIds)

    

    catalog['ArtistID'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtworksIds)

    
    
    catalog['BeginDate'] = mp.newMap(500,
                                   maptype='CHAINING',
                                   loadfactor=5,
                                   comparefunction=compareBeginDate)
    
    catalog['Medium'] = mp.newMap(34500,
                                maptype='CHAINING',
                                loadfactor=2,
                                comparefunction=compareArtworksbymedium)


    
    catalog['Work_Nationality'] = mp.newMap(34500,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareNationality)
    
    catalog['Artists_ConstituentID'] = mp.newMap(16000,
                                 maptype='PROBING',
                                 loadfactor=0.5,)
    '''
    catalog['Work_ConstituentID'] = mp.newMap(16000,
                                 maptype='PROBING',
                                 loadfactor=0.5,)
                                 
    '''

    return catalog
  

# Funciones para agregar informacion al catalogo
def addtomap(map,key,object):

    if mp.contains(map,key):

        if type(mp.get(map,key)['value']) == type(object):    
            l=lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(l,mp.get(map,key)['value'])
            lt.addLast(l,object)
            mp.put(map,key,l)
            
        else:     
            entry=mp.get(map,key)
            list=entry['value']
            #print(list)
            lt.addLast(list,object)
            #print(mp.get(catalog['BeginDate'],artist['BeginDate']))
            
    else: 
        mp.put(map,key,object)

 

def addArtist(catalog, artist):
    lt.addLast(catalog["Artists"], artist)

    addtomap(catalog['BeginDate'],artist['BeginDate'],artist)
    mp.put(catalog['Artists_ConstituentID'],artist['ConstituentID'],artist)



    
def addArtwork(catalog, artwork):
    lt.addLast(catalog["Artworks"], artwork)

    addtomap(catalog['Medium'],artwork['Medium'],artwork)
    #mp.put(catalog['Work_ConstituentID'],artwork['ConstituentID'],artwork)
    ArtworksbyNationalityMap(catalog,artwork)



def ArtworksbyNationalityMap(catalog,artwork):

    list=artwork['ConstituentID'].replace('[','').replace(']','').split(',')
    Nations=[]
    for i in list:

        Artist=mp.get(catalog['Artists_ConstituentID'],i)
        if Artist != None:
            Nation=mp.get(catalog['Artists_ConstituentID'],i)['value']['Nationality']
            if Nation not in Nations:
                Nations.append(Nation)
                addtomap(catalog['Work_Nationality'],Nation,artwork)
    

   





# Funciones para creacion de datos



# Funciones de consulta
#REQ 1

def ArtistbyBeginDate(catalog, min, max):

    rta=[]

    Dates=mp.keySet(catalog['BeginDate'])
    b=lt.newList(datastructure='ARRAY_LIST')

    for i in range(1,lt.size(Dates)+1):

        date=int(lt.getElement(Dates,i))

        if int(min) <= date and date <= int(max):
            lt.addLast(b,date)

    mg.sort(b,cmpArtistBegindate)

    size=lt.size(b)
    rta.append(size)

    

    if type(mp.get(catalog['BeginDate'],str(lt.getElement(b,1)))['value']) == type(lt.getElement(catalog['Artists'],1)):
        a1=mp.get(catalog['BeginDate'],str(lt.getElement(b,1)))['value']
        rta.append(a1)
    if type(mp.get(catalog['BeginDate'],str(lt.getElement(b,2)))['value']) == type(lt.getElement(catalog['Artists'],1)):
        a2=mp.get(catalog['BeginDate'],str(lt.getElement(b,2)))['value']
        rta.append(a2)

    if type(mp.get(catalog['BeginDate'],str(lt.getElement(b,3)))['value']) == type(lt.getElement(catalog['Artists'],1)):
        a3=mp.get(catalog['BeginDate'],str(lt.getElement(b,3)))['value']
        rta.append(a3)

    else: 
        mg.sort(mp.get(catalog['BeginDate'],str(lt.getElement(b,1)))['value'],cmpArtistNationality)
        if lt.size(mp.get(catalog['BeginDate'],str(lt.getElement(b,1)))['value']) >= 3:
            for i in range(1,4):
                a=lt.getElement(mp.get(catalog['BeginDate'],str(lt.getElement(b,1)))['value'],i)
                rta.append(a)
        else:
            for i in range(1,3):
                a=lt.getElement(mp.get(catalog['BeginDate'],str(lt.getElement(b,1)))['value'],i)
                rta.append(a)
            af=mp.get(catalog['BeginDate'],str(lt.getElement(b,1)))['value']
            rta.append(af)

    

    print(rta)    

    return rta

#lab5

def ArtworksbyMedium(catalog,Name,n):

    Artworks = mp.get(catalog['Medium'],Name)
    
    list=Artworks['value']
    
    mg.sort(list,cmpArtworkDate)
    
    rta=lt.newList(datastructure='ARRAY_LIST')
    for i in range(1,int(n)+1):
        
        lt.addLast(rta,lt.getElement(list,i))
        
    return rta

#Lab6

def ArtworksbyNationality(catalog,Nation):

    size=0
    if type(mp.get(catalog['Work_Nationality'],Nation)['value']) == dict:

        size=lt.size(mp.get(catalog['Work_Nationality'],Nation)['value'])
    elif type(mp.get(catalog['Work_Nationality'],Nation)['value']) == type(lt.getElement(catalog['Artists'],1)):
        size=1
    return size

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compareArtistIds(id1, id2):
   
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1



def compareArtworksIds(id, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1

def compareBeginDate(date, entry):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    datentry = me.getKey(entry)
    if (int(date) == int(datentry)):
        return 0
    elif (int(date) > int(datentry)):
        return 1
    else:
        return -1

def compareArtworksbymedium(Medium, artwork):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    artentry = me.getKey(artwork)
    if (Medium == artentry):
        return 0
    elif (Medium > artentry):
        return 1
    else:
        return -1

def compareAuthorsByName(keyname, author):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(author)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareNationality(Nationality,entry):
    NationalityE = me.getKey(entry)
    if Nationality == NationalityE:
        return 0
    elif Nationality > NationalityE:
        return 1
    else:
        return -1


##################################################
##################################################


def cmpArtistBegindate(Date1, Date2):

    if Date1 < Date2:
        return True
    else:
        return False

def cmpArtworkDate(artwork1, artwork2):

    if artwork1["Date"] == '':
        artwork1["Date"]='No se sabe'
    if artwork2["Date"] == '':
        artwork2["Date"]='No se sabe'

    if (artwork1["Date"]) < (artwork2["Date"]):
        return True
    else:
        return False

def cmpArtistNationality(artist1, artist2):

    if artist1['ArtistBio'] < artist2['ArtistBio']:
        return True
    else:
        return False