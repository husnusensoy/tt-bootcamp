setwd("/Users/2na/Documents/veri bilimi dersleri/2. dönem/İstatistik ve Olasılık/final ödevi")
data <- read.csv("bodyfat.csv")
nrow(data)

set.seed(2023900325)
indeks <-  sort(sample(1:nrow(data), size=150, replace = F))
data <- data[indeks,]

library(moments)
set.seed(2023900325)
indeks <-  sort(sample(1:ncol(data), size=3, replace = F))

apply(data[,indeks], 2, function(column) {
  c(
    Mean = mean(column),
    Median = median(column),
    Mode = as.numeric(names(sort(table(column), decreasing = TRUE)[1])), # Mod
    Variance = var(column),
    Std_Dev = sd(column),
    Range = diff(range(column)),
    IQR = IQR(column),
    Q1 = quantile(column, 0.25), 
    Q3 = quantile(column, 0.75),
    Min = min(column),
    Max = max(column),
    Skewness = skewness(column),
    Kurtosis = kurtosis(column)
  )
})


apply(data, 2, function(column) {
  c(
    Skewness = skewness(column),
    Kurtosis = kurtosis(column)
  )
})[, order(apply(data, 2, function(column) skewness(column)))]

set.seed(2023900325)
sonuncu_degisken<- sample(c("Thigh","Abdomen","Weight","Hip"), size=1)
sonuncu_degisken
data<-data[c("Forearm","Height",sonuncu_degisken)]


library(nortest)

sapply(data, function(column) {
  c(
    ShapiroWilk_P_Value = shapiro.test(column)$p.value,                      # Shapiro-Wilk
    CramerVonMises_P_Value = cvm.test(column)$p.value,                      # Cramér-von Mises
    AndersonDarling_P_Value = ad.test(column)$p.value,                      # Anderson-Darling
    KolmogorovSmirnov_P_Value = ks.test(column, "pnorm",                    # Kolmogorov-Smirnov
                                        mean(column), sd(column))$p.value
  )
})


# Gerekli kütüphaneler
library(ggplot2)
library(nortest)
library(tidyr)
library(dplyr)

# Merkezi Limit Teoremi ve Normallik Testleri Fonksiyonu
clt_demo_with_tests <- function(data, sample_sizes = c(5, 10, 30, 50), num_samples = 1000) {
  plots <- list()
  norm_tests <- list()
  
  # Her sütun için
  for (col_name in colnames(data)) {
    column_data <- data[[col_name]]
    results <- list()
    tests <- list()
    
    for (size in sample_sizes) {
      # Örneklem ortalamaları
      sample_means <- replicate(num_samples, mean(sample(column_data, size, replace = TRUE)))
      
      # Normallik testleri
      shapiro_p <- shapiro.test(sample_means)$p.value
      ad_p <- ad.test(sample_means)$p.value
      cvm_p <- cvm.test(sample_means)$p.value
      
      # Test sonuçlarını kaydet
      tests[[as.character(size)]] <- data.frame(
        SampleSize = size,
        Shapiro_Wilk = shapiro_p,
        Anderson_Darling = ad_p,
        Cramer_Von_Mises = cvm_p
      )
      
      # Örneklem büyüklüğüne göre görselleştirme için veri kaydı
      results[[as.character(size)]] <- data.frame(
        SampleSize = factor(size, levels = c(5, 10, 30, 50),
                            labels = c("Sample Size = 5", "Sample Size = 10", 
                                       "Sample Size = 30", "Sample Size = 50")),
        SampleMeans = sample_means
      )
    }
    
    # Tüm test sonuçlarını birleştirme
    norm_tests[[col_name]] <- do.call(rbind, tests)
    
    # Tüm örneklem büyüklüklerini görselleştirme için birleştirme
    results_df <- do.call(rbind, results)
    sturges_bins <- ceiling(log2(length(data[[1]])) + 1)
    
    # ggplot oluşturma
    p <- ggplot(results_df, aes(x = SampleMeans)) +
      geom_histogram(bins = sturges_bins, color = "black", fill = "skyblue") +
      facet_wrap(~ SampleSize, ncol = 2, scales = "free") + # Dinamik eksenler için scales = "free"
      labs(
        title = paste("Merkezi Limit Teoremi:", col_name),
        x = "Örneklem Ortalamaları",
        y = "Frekans"
      ) +
      theme_minimal()
    
    # Her bir plotu sakla
    plots[[col_name]] <- p
  }
  
  # Görseller ve normallik testlerini döndür
  return(list(Plots = plots, NormTests = norm_tests))
}

# Fonksiyonu çalıştır
clt_results <- clt_demo_with_tests(data)

# Her bir sütunun görselleştirilmesi
for (col_name in names(clt_results$Plots)) {
  print(clt_results$Plots[[col_name]]) # Sütunun grafiği
  print(clt_results$NormTests[[col_name]]) # Normallik test sonuçları
}

# Normallik testlerinin sonuçları
for (col_name in names(clt_results$NormTests)) {
  cat("\nNormallik Test Sonuçları -", col_name, "\n")
  print(clt_results$NormTests[[col_name]])
}


set.seed(2023900325)
indeks1 <- sort(sample(1:nrow(data),size = 30,replace = F))
set.seed(2023900325)
indeks2 <- sample(1:ncol(data),size=1)
kitle<- data[,indeks2]
orneklem<- data[indeks1,indeks2]
orneklem

# standart sapma biliniyorsa

orneklem_ortalama <- mean(orneklem)
kitle_ortalama <- mean(kitle)
# Güven aralığını bir değişkene ata
guven_araligi <- 0.99

# Üst sınır için (1 + güven aralığı) / 2 işlemini yap
p_degeri <- (1 + guven_araligi) / 2
p_degeri  # 0.975

# Z-değerini hesapla
z_degeri <- qnorm(p_degeri)
z_degeri   # 1.959964

kitle_standart_sapması <- sqrt(sum((kitle-kitle_ortalama)^2)/length(kitle))

standart_hata <- kitle_standart_sapması/sqrt(length(orneklem))
maksimum_deger <- orneklem_ortalama+(z_degeri*standart_hata)
minimum_deger <- orneklem_ortalama-(z_degeri*standart_hata)
paste0("%99 Güvenle Kitle ortalaması (", 
       "\u03bc", # Unicode ile mu
       ") değerleri: ", 
       minimum_deger, 
       " ≤ ", 
       "\u03bc", 
       " ≤ ", 
       maksimum_deger)
?expression

# Kitle standart sapması biliniyorsa

guven_araligi <- 0.90

# Üst sınır için (1 + güven aralığı) / 2 işlemini yap
p_degeri <- (1 + guven_araligi) / 2
p_degeri  # 0.95

# Z-değerini hesapla
z_degeri <- qnorm(p_degeri)
z_degeri   # 1.644854


maksimum_deger <- orneklem_ortalama+(z_degeri*standart_hata)
minimum_deger <- orneklem_ortalama-(z_degeri*standart_hata)

paste0("%90 Güvenle Kitle ortalaması (", 
       "\u03bc", # Unicode ile mu
       ") değerleri: ", 
       minimum_deger, 
       " ≤ ", 
       "\u03bc", 
       " ≤ ", 
       maksimum_deger)




# R kodu: I. Tip ve II. Tip Hata Simülasyonu

# Rastgelelik için seed sabitlenmesi
set.seed(2023900325)

gercek_iyilestirme_orani <- 0.90  # Gerçek iyileştirme oranı
hipotez_orani <- 0.80  # H0'da kullanılan oran
n <- 100  # Örneklem büyüklüğü
simulasyon_sayisi <- 10000  # Simülasyon sayısı

tip1_hata_sayisi <- 0  # I. Tip hata sayısı
tip2_hata_sayisi <- 0  # II. Tip hata sayısı
alpha <- 0.05  # İstatistiksel anlamlılık düzeyi

# Simülasyon
for (i in 1:simulasyon_sayisi) {
  # Rastgele örnekleme (H0 hipotezi doğru varsayımı altında)
  ornek_h0 <- rbinom(1, n, hipotez_orani)
  ornek_orani_h0 <- ornek_h0 / n
  
  # Rastgele örnekleme (gerçek iyileştirme oranı ile)
  ornek_h1 <- rbinom(1, n, gercek_iyilestirme_orani)
  ornek_orani_h1 <- ornek_h1 / n
  
  # H0 hipotezi altındaki standart hata
  std_error_h0 <- sqrt((hipotez_orani * (1 - hipotez_orani)) / n)
  
  # Kritik değer (Z-testi için)
  kritik_deger <- qnorm(1 - alpha)
  
  # Test istatistiği (H0 hipotezi için)
  z_degeri_h0 <- (ornek_orani_h0 - hipotez_orani) / std_error_h0
  
  # Test istatistiği (H1 hipotezi için)
  z_degeri_h1 <- (ornek_orani_h1 - hipotez_orani) / std_error_h0
  
  # I. Tip Hata: H0 doğru ama reddedildi
  if (z_degeri_h0 > kritik_deger) {
    tip1_hata_sayisi <- tip1_hata_sayisi + 1
  }
  
  # II. Tip Hata: H0 yanlış ama reddedilmedi
  if (z_degeri_h1 <= kritik_deger) {
    tip2_hata_sayisi <- tip2_hata_sayisi + 1
  }
}

# Sonuçların Hesaplanması
tip1_hata_orani <- tip1_hata_sayisi / simulasyon_sayisi
tip2_hata_orani <- tip2_hata_sayisi / simulasyon_sayisi
test_gucu <- 1 - tip2_hata_orani

# Sonuçların Yazdırılması
cat("I. Tip Hata Oranı (α):", round(tip1_hata_orani, 4), "\n")
cat("II. Tip Hata Oranı (β):", round(tip2_hata_orani, 4), "\n")
cat("Testin Gücü (1 - β):", round(test_gucu, 4), "\n")

