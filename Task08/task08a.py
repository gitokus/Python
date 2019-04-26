from delphiTools3.base import loadmat
from tqdm import tqdm
import numpy as np
import os


# funkcja filtrująca pliki typu ".mat"
def getFiles(path):
    FileList = []
    for file in os.listdir(path):
        if file.endswith(".mat"):
            FileList.append(os.path.join(path, file))
    return FileList

data_table = []
# mat_path = os.getcwd()
# lista plików *.mat w folderze
matList = getFiles(r".")

for item in tqdm(matList):
    print(f"***** Processing: {item} ****")

    # tu jest ładowany cały plik *.mat do zmiennej mat
    try:
        mat = loadmat(item)
    except Exception as e:
        # w razie wyjatku dodajemny nazwe pliku do data_table
        data_table.append([item, e, None])
        continue

    # tu z elementu mat wybieramy właściwe wartosci
    vdID = mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo']['activeLightSpots']['vdID']
    id = mat['mudp']['vis']['vision_obstacles_info']['visObjects']['visObs']['id']

    for coordinates, val_vdID in np.ndenumerate(vdID):
        if val_vdID != 0:  # jesli wartość w macierzy vdID jest różna od zera
            id_l = id[coordinates[0]]  # to znajdz w macierzy id odpowiadający wiersz
            # print(coordinates, val_vdID)
            if np.where(id_l == val_vdID):  # sprawdź czy niezerowa wartość w macierzy vdID w odpowiednim wierszu znajduje się także w macierzy id
                with open(r"lista.csv", 'a') as f:
                    f.write( f"{os.path.basename(item)};Wartość id odpowiada wartości vdID ! ;"+
                             f"Numer ramki: {coordinates[0]}; Niezerowa wartość vdID: {val_vdID}; Wartość id: {id_l}" + '\n')
            else:  # jeśli nie to poinformuj o niezgodności
                with open(r"lista.csv", 'a') as f:
                    f.write( f"{os.path.basename(item)};Wartość id NIE odpowiada wartości vdID ! ;"+
                             f"Numer ramki: {coordinates[0]}; Niezerowa wartość vdID: {val_vdID}; Wartość id: {id_l}" + '\n')
