from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

resource_dir = Path("./", "resources")

# CSV dosyasının tamamını 'kaynaklar' dizinindeki ZIP dosyasından oku
data = pd.read_csv(
    Path(resource_dir, 'full_dataset.zip'),
    sep=',',
    header=None,
    compression='zip')

col_names = []

with open(Path(resource_dir, 'col_names.txt')) as cols_fp:
    for line_num, name in enumerate(cols_fp):
        col_names.append(name.rstrip())

# Sütun başlıklarını Wireshark çerçevesindeki adlara ayarla
data.columns = col_names


# '?' işaretini NumPy NaN değerine sahip DataFrame'deki değerle değiştir
data = data.replace('?', np.nan)

# Bir sütundaki değerlerin %60'ından fazlası boşsa onu kaldır
prev_num_cols = len(data.columns)
data.dropna(axis='columns', thresh=len(data.index) * 0.40, inplace=True)
print("Removed " + str(prev_num_cols - len(data.columns)) +
      " columns with all NaN values.")

# Değişiklik içermeyen sütunları kaldır (sıfır değer veya içinde yalnızca bir benzersiz değer)
cols_to_drop = []

for col in data:
    if not data[col].nunique() > 1:
        cols_to_drop.append(col)

data.drop(columns=cols_to_drop, inplace=True)
print("Removed " + str(len(cols_to_drop)) +
      " columns with no variation in its values.")
print("DataFrame's current shape: " + str(data.shape))

# Doğru günlük kaydı için bırakılacak sütunların listesini temizle
cols_to_drop.clear()

for col in data:
    if data[col].nunique() >= (len(data.index) * 0.50):
        cols_to_drop.append(col)

data.drop(columns=cols_to_drop, inplace=True)
print("Removed " + str(len(cols_to_drop)) +
      " columns with over 50% variation in its values")

# Küçültülmüş ve önceden işlenmiş veri kümesinin bir ZIP dosyasına çıktısına kaydet (dizin sütunu eklenmeden)
data.to_csv(
    Path(resource_dir, 'preproc_dataset.zip'),
    sep=',',
    index=False,
    compression='zip')