# AWID


# Veri Seti İşleme ve Ön İşleme Python Kodu

Bu Python kodu, bir veri setini okuma, işleme ve ön işleme adımlarını içeren bir dizi işlemi gerçekleştirir. Aşağıda kodun ne yaptığını adım adım açıklıyoruz:


Adım 1: Pathlib ve Gerekli Kütüphaneleri İçe Aktarma

from pathlib import Path
import numpy as np
import pandas as pd
Bu kısımda, pathlib kütüphanesi kullanılarak dosya yollarını işlemek için gerekli olan sınıflar ve numpy ile pandas kütüphaneleri içe aktarılır.


Adım 2: Dosya Yollarını Tanımlama ve İlgili Sütunları Seçme

resource_dir = Path('./', 'resources')
desired_cols = [2, 5, 45, 62, 64, 65, 68, 71, 74, 75, 88, 91, 92, 105, 106, 110, 116, 120, 154]
resource_dir değişkeni, çalışma dizinindeki 'resources' klasörünün dosya yolu olarak belirlenir. desired_cols listesi, analizde kullanılacak olan sütunların indekslerini içerir.


Adım 3: Veriyi Okuma ve Belirli Sütunları Seçme

data = pd.read_csv(
    Path(resource_dir, 'full_dataset.zip'),
    sep=',',
    compression='zip',
    usecols=desired_cols)
pd.read_csv fonksiyonu kullanılarak, belirtilen sütunları içeren bir CSV dosyası okunur ve bu veri data adlı bir Pandas DataFrame'e atanır.



Adım 4: Sütun İsimlerini Belirleme

with open(Path(resource_dir, 'col_names.txt')) as cols:
    for line_num, col_name in enumerate(cols



