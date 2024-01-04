# Min-Max normalizasyonu uygulamak için bir fonksiyon
normalize <- function(x) { return ((x - min(x)) / (max(x) - min(x)))  }

# CSV dosyasını yükle
wifiLog <- read.delim("C:/CIS660/project/dataset-headers-reduced-removed-null.csv", sep=",")
View(wifiLog)

# Kullanılan 4 sütun dışındaki tüm sütunları kaldır
wifiLog2 <- wifiLog[,c(which(colnames(wifiLog)=="wlan.fc.type"), which(colnames(wifiLog)=="frame.time_delta_displayed"), which(colnames(wifiLog)=="wlan.duration"), which(colnames(wifiLog)=="class"))]
View(wifiLog2)

# Kullanılan sütunları Min-Max normalize et
wifiLog2$wlan.fc.type = normalize(as.numeric(wifiLog2$wlan.fc.type))
wifiLog2$frame.time_delta_displayed = normalize(as.numeric(wifiLog2$frame.time_delta_displayed))
wifiLog2$wlan.duration = normalize(as.numeric(wifiLog2$wlan.duration))
View(wifiLog2)

# Tahminde bulunduğumuz saldırı türü
ATTACKTYPE <- "arp"

# Hedef sınıfı ve normal paketleri tut
wifiLog2 <- wifiLog2[wifiLog2$class=="normal" | wifiLog2$class==ATTACKTYPE, ]

# Hedef saldırı türünü ve sınıf türünü 0/1 olarak değiştir
wifiLog2$class <- as.character(wifiLog2$class)
wifiLog2$class[wifiLog2$class=="normal"] <- as.character("0")
wifiLog2$class[wifiLog2$class==ATTACKTYPE] <- as.character("1")
wifiLog2$class <- as.factor(wifiLog2$class)

# Kullanılmayan faktör seviyelerini kaldır
wifiLog2$class <- droplevels(wifiLog2$class)
unique(wifiLog2$class)

# Veri setini bölmek için kullanılacak oran: %66 eğitim, %33 test
smp_size <- floor(0.66 * nrow(wifiLog2))

## Bölümü çoğaltılabilir kılmak için seed ayarı
set.seed(32)
# Bölme işlemi
train_ind <- sample(seq_len(nrow(wifiLog2)), size = smp_size)

# Eğitim setini oluştur
train <- wifiLog2[train_ind, ]

# Test setini oluştur
test <- wifiLog2[-train_ind, ]

View(train)
View(test)

library(DMwR)
# Tahmin edici değişkenlerin formülünü oluştur
f <- formula("class ~ wlan.fc.type + frame.time_delta_displayed + wlan.duration")
# SMOTE'u çalıştır
train_smote <- SMOTE(f, train, perc.over = 150, perc.under = 400, k = 1)
View(train_smote)
library(mlr)

# Görevi oluştur
# task <- makeClassifTask(data = test, target = "class")
# test_oversamp_task <- oversample(task, rate = 25)
# test_oversamp <- test_oversamp_task$env$data
test_oversamp <- test

# Tahmin işlemini gerçekleştir
m <- kNN(f, train_smote, test_oversamp, norm = FALSE, k = 1)

# Bir örnek bir false positive mı diye belirle
FindFP <- function(predicted, predictor)
{
  c <- 0
  #cat("IN FindFP: predictor:", predictor, " predicted: ", predicted)
  for (x in 1:length(predicted))
  {
    if(predictor[x]==0 && predicted[x]==1)
      c <- c + 1
  }
  return (c)
}

# Bir örnek bir false negative mı diye belirle
FindFN <- function(predicted, predictor)
{
  c <- 0
  #cat("IN FindFP: predictor:", predictor, " predicted: ", predicted)
  for (x in 1:length(predicted))
  {
    if(predictor[x]==1 && predicted[x]==0)
      c <- c + 1
  }
  return (c)
}

# Bir örnek bir true positive mı diye belirle
FindTP <- function(predicted, predictor)
{
  c <- 0
  #cat("IN FindFP: predictor:", predictor, " predicted: ", predicted)
  for (x in 1:length(predicted))
  {
    if(predictor[x]==1 && predicted[x]==1)
      c <- c + 1
  }
  return (c)
}

# Bir örnek bir true negative mı diye belirle
FindTN <- function(predicted, predictor)
{
  c <- 0
  #cat("IN FindFP: predictor:", predictor, " predicted: ", predicted)
  for (x in 1:length(predicted))
  {
    if(predictor[x]==0 && predicted[x]==0)
      c <- c + 1
  }
  return (c)
}

#cat("ATTACK TYPE İÇİN TEST VERİSİ DAĞILIMI TABLOSU ",ATTACKTYPE,":")
#w <- table(test_oversamp$class)
#t <- as.data.frame(w)
#names(t)[1] <- "Class"
#show(t)

FP <- FindFP(m, test_oversamp$class)
TP <- FindTP(m, test_oversamp$class)
TN <- FindTN(m, test_oversamp$class)
FN <- FindFN(m, test_oversamp$class)
accuracy <- (TP + TN) / (FP + TP + TN + FN)
errorRate <- (FP + FN) / (FP + TP + TN + FN)
sensitivity <- TP / (TP + FP)
specificity <- TN / (TN + FN)
precision <- TP / (FP + TP)
recall <- TP / (TP + FN)

cat("FP:", FP, " TP:", TP, "TN: ", TN, "FN: ", FN, "\n")

cat("Karmaşıklık Matrisi:\n")
n <- sprintf("n=%d", TP + TN + FP + FN)

l <- sprintf("%20s%20s%20s\n", n, "Tahmin Edilen: HAYIR", "Tahmin Edilen: EVET")
cat(l)
l <- sprintf("%20s%20d%20d%20d\n", "Gerçek: HAYIR", TN, FP, TN + FP)
cat(l)
l <- sprintf("%20s%20d%20d%20d\n", "Gerçek: EVET", FN, TP, FN + TP)
cat(l)
l <- sprintf("%20s%20d%20d\n", "", TN + FN, FP + TP)
cat(l)
cat("Doğruluk: ", accuracy, "\n")
cat("Hata Oranı: ", errorRate, "\n")
cat("Hassasiyet: ", sensitivity, "\n")
cat("Özgünlük: ", specificity, "\n")
cat("Precision: ", precision, "\n")
cat("Recall: ", recall, "\n")
