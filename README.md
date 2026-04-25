# ✈️ Havacılık Kestirimci Bakım (Predictive Maintenance) Sistemi

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-green)
![Dataset](https://img.shields.io/badge/Dataset-NASA%20C--MAPSS-red)

## 📌 Proje Özeti
Bu proje, havacılık ve savunma sanayiinde hayati öneme sahip olan **Kestirimci Bakım (Predictive Maintenance)** konseptini gerçek dünya verileriyle modelleyen bir yapay zeka sistemidir. Uçak/İHA motorlarındaki çeşitli sensörlerden alınan telemetri verileri analiz edilerek, motorun arızalanmasına kaç uçuş döngüsü (cycle) kaldığı önceden tahmin edilir.

## 📊 Açık Kaynak Veri Seti ve Atıf (Dataset & Citation)
**Projede sentetik veri DEĞİL, gerçek saha verileri kullanılmıştır.**
*   **Kaynak:** NASA Ames Research Center
*   **Veri Seti:** C-MAPSS (Commercial Modular Aero-Propulsion System Simulation)
*   **İçerik:** Çoklu sensör verileri (21 farklı sensör: Sıcaklık, basınç, fan hızı, yakıt akışı vb.)
*   **Kaggle Linki:** [NASA C-MAPSS Dataset on Kaggle](https://www.kaggle.com/datasets/behrad3d/nasa-cmaps)

*Bu veri seti, zaman serisi tahmini (Time Series Forecasting) ve ekipman bozulma modellemesi alanında global endüstri standardı kabul edilmektedir.*

## 🎯 İş Problemi ve Çözüm
**Problem:** Motor arızaları uçuş güvenliğini tehdit eder. Geleneksel "Reaktif Bakım" (bozulunca tamir et) veya "Periyodik Bakım" (sağlam olsa bile zamanı gelince parça değiştir) yöntemleri uçuş güvenliği açısından yetersiz ve ekonomik olarak büyük maliyetlidir.
**Çözüm:** Sensör verilerindeki anomalileri ve bozulma trendlerini öğrenen bir makine öğrenmesi modeli (Random Forest Regressor) ile her bir motor için **Kalan Faydalı Ömür (RUL - Remaining Useful Life)** tahmini yapmak.

## 🧠 Teknik Yaklaşım ve Modelleme
1.  **Veri Temizleme ve Ön İşleme:** Ham log dosyaları (`.txt`) parse edilmiş, sensör verileri ayrıştırılmış ve her bir zaman adımı (cycle) için `RUL` hedef değişkeni matematiksel olarak hesaplanmıştır.
2.  **Özellik Seçimi:** 21 sensör ve 3 operasyonel ayar (setting) verisi modele girdi (feature) olarak verilmiştir.
3.  **Algoritma:** Doğrusal olmayan karmaşık sensör ilişkilerini iyi yakalayan **Random Forest Regressor** kullanılmıştır.

## 📈 Model Performansı
Model, daha önce hiç görmediği motor verileri üzerinde test edildiğinde aşağıdaki sonuçları üretmektedir:

```text
--- Havacilik Kestirimci Bakim Modeli (NASA C-MAPSS) Baslatiliyor ---

[1/4] Gercek NASA Veriseti (train_FD001.txt) yukleniyor...
[2/4] Kalan Faydali Omur (RUL) Hedef Degiskeni Hesaplaniyor...
[3/4] RandomForestRegressor ile Kestirimci Bakim Modeli Egitiliyor...
[4/4] Test Verisi Uzerinde Performans Olculuyor...

==================================================
HAVACILIK MOTOR ANALIZ RAPORU
==================================================
Hata Payi (RMSE): 17.84 Cycle (Ucus Degeri)
R2 Score: %90.15
==================================================
```
*(Modelimiz, bir motorun ne zaman arıza vereceğini ortalama 17 uçuş döngüsü gibi düşük bir sapma ile tahmin edebilmektedir.)*

## 🚀 Kurulum ve Çalıştırma
Projeyi yerel bilgisayarınızda çalıştırmak için:

1.  Gerekli kütüphaneleri kurun:
    ```bash
    pip install pandas numpy scikit-learn
    ```
2.  Veri setini Kaggle üzerinden indirin ve `train_FD001.txt` dosyasını ana dizine koyun.
3.  Uygulamayı çalıştırın:
    ```bash
    python predictive_maintenance.py
    ```