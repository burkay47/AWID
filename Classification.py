import pandas as pd
from sklearn.utils import resample
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

# Min-Max normalizasyonu uygulamak için bir fonksiyon
def normalize(x):
    return (x - min(x)) / (max(x) - min(x))

# CSV dosyasını yükle
wifi_log = pd.read_csv("C:/CIS660/project/dataset-headers-reduced-removed-null.csv", sep=",")

# Kullanılan 4 sütun dışındaki tüm sütunları kaldır
selected_columns = ["wlan.fc.type", "frame.time_delta_displayed", "wlan.duration", "class"]
wifi_log_2 = wifi_log[selected_columns]

# Kullanılan sütunları Min-Max normalize et
wifi_log_2["wlan.fc.type"] = normalize(wifi_log_2["wlan.fc.type"].astype(float))
wifi_log_2["frame.time_delta_displayed"] = normalize(wifi_log_2["frame.time_delta_displayed"].astype(float))
wifi_log_2["wlan.duration"] = normalize(wifi_log_2["wlan.duration"].astype(float))

# Tahminde bulunduğumuz saldırı türü
ATTACK_TYPE = "arp"

# Hedef sınıfı ve normal paketleri tut
wifi_log_2 = wifi_log_2[(wifi_log_2["class"] == "normal") | (wifi_log_2["class"] == ATTACK_TYPE)]

# Hedef saldırı türünü ve sınıf türünü 0/1 olarak değiştir
wifi_log_2["class"] = wifi_log_2["class"].map({"normal": 0, ATTACK_TYPE: 1})

# Veri setini bölmek için kullanılacak oran: %66 eğitim, %33 test
smp_size = int(0.66 * len(wifi_log_2))

# Bölme işlemi
train_ind = resample(wifi_log_2.index, n_samples=smp_size, random_state=32)

# Eğitim setini oluştur
train = wifi_log_2.loc[train_ind]

# Test setini oluştur
test = wifi_log_2.drop(train_ind)

# SMOTE'u çalıştır
train_oversampled = resample(train, replace=True, n_samples=int(len(train) * 1.5), random_state=1)

# Tahmin edici değişkenlerin formülünü oluştur
features = ["wlan.fc.type", "frame.time_delta_displayed", "wlan.duration"]
X_train = train_oversampled[features]
y_train = train_oversampled["class"]
X_test = test[features]
y_test = test["class"]

# kNN modelini oluştur
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

# Tahmin işlemini gerçekleştir
predictions = knn.predict(X_test)

# Karmaşıklık matrisini oluştur
conf_matrix = confusion_matrix(y_test, predictions)

# Diğer metrikleri hesapla
TP = conf_matrix[1, 1]
TN = conf_matrix[0, 0]
FP = conf_matrix[0, 1]
FN = conf_matrix[1, 0]

accuracy = (TP + TN) / (FP + TP + TN + FN)
error_rate = (FP + FN) / (FP + TP + TN + FN)
sensitivity = TP / (TP + FN)
specificity = TN / (TN + FP)
precision = TP / (FP + TP)
recall = TP / (TP + FN)

print("FP:", FP, " TP:", TP, "TN: ", TN, "FN: ", FN)
print("Karmaşıklık Matrisi:\n", conf_matrix)
print("Doğruluk: ", accuracy)
print("Hata Oranı: ", error_rate)
print("Hassasiyet: ", sensitivity)
print("Özgünlük: ", specificity)
print("Precision: ", precision)
print("Recall: ", recall)
