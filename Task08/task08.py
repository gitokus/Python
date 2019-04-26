from delphiTools3.base import loadmat
from tqdm import tqdm
import os
import numpy as np


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
matList = getFiles(r"D:\dev\python\PycharmProjects\Zuzia\Python\Task08")
# matList = matList[:5]
# dla kazdego pliku
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
    # tu z elementu mat wybieramy właściwe wartosci
    vdID = mat['mudp']['vis']['vision_active_light_sensor_info']['activeLightSensorInfo']['activeLightSpots']['vdID']
    id = mat['mudp']['vis']['vision_obstacles_info']['visObjects']['visObs']['id']

    # vdID tablica 15 x 916, id tablica 15 x 916
    for coordinates, val_vdID in np.ndenumerate(vdID):
        if val_vdID != 0:
            x = coordinates[0]
            y = coordinates[1]
            print(coordinates, val_vdID)
            id_l = id[x]
            if np.where(id_l == val_vdID):
                print(id_l)

    # w-nadpisuje 1 linie, a-append dodaje na koniec !
    # with open(r"C:\Users\djy8yz\Desktop\task_21_02\lista.csv", 'a') as f:
    # f.write(
    # f"{os.path.basename(item)};{vdID};{id}" + '\n')

    # print(niezero_val)

print(f"***** Uff, zrobione ****")
