import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("--- Havacilik Kestirimci Bakim Modeli (NASA C-MAPSS) Baslatiliyor ---\n")

DATA_PATH = "train_FD001.txt"

def load_data(filepath):
    """
    NASA C-MAPSS verisetini (Kaggle/UCI) okur ve DataFrame'e cevirir.
    Eger dosya yoksa profesyonel bir uyari verir.
    """
    if not os.path.exists(filepath):
        print(f"HATA: '{filepath}' bulunamadi!")
        print("Lutfen veriseti dosyasini asagidaki Kaggle linkinden indirip bu Python dosyasinin yanina koyun:")
        print("🔗 https://www.kaggle.com/datasets/behrad3d/nasa-cmaps")
        print("Not: Bu proje endustri standardi gercek verilerle calismaktadir, sentetik veri uretilmez.")
        exit(1)
        
    print(f"[1/4] Gercek NASA Veriseti ({filepath}) yukleniyor...")
    
    # NASA veriseti sutun isimleri (veriseti kaynaginda dokumante edilmistir)
    columns = ['unit_number', 'time_in_cycles', 'setting_1', 'setting_2', 'setting_3'] + \
              [f'sensor_{i}' for i in range(1, 22)]
              
    df = pd.read_csv(filepath, sep='\s+', header=None, names=columns)
    return df

def add_rul(df):
    """Her motor (unit_number) icin Kalan Faydali Omru (RUL) hesaplar"""
    print("[2/4] Kalan Faydali Omur (RUL) Hedef Degiskeni Hesaplaniyor...")
    # Her motorun maksimum cycle'i, o motorun bozuldugu andir
    rul = pd.DataFrame(df.groupby('unit_number')['time_in_cycles'].max()).reset_index()
    rul.columns = ['unit_number', 'max']
    df = df.merge(rul, on=['unit_number'], how='left')
    df['RUL'] = df['max'] - df['time_in_cycles']
    df.drop('max', axis=1, inplace=True)
    return df

if __name__ == "__main__":
    # 1. Veriyi Yukle ve Hazirla
    df = load_data(DATA_PATH)
    df = add_rul(df)

    # 2. Ozellikleri Sec (Sensorler ve Ayarlar)
    features = df.columns.drop(['unit_number', 'time_in_cycles', 'RUL'])
    X = df[features]
    y = df['RUL']

    # 3. Gercek dunya senaryosu: Son %20'lik veriyi test icin ayir (Zamana bagli kesim)
    train_size = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
    y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

    # 4. Model Egitimi
    print("[3/4] RandomForestRegressor ile Kestirimci Bakim Modeli Egitiliyor...")
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # 5. Degerlendirme
    print("[4/4] Test Verisi Uzerinde Performans Olculuyor...\n")
    y_pred = model.predict(X_test)

    print("="*50)
    print("HAVACILIK MOTOR ANALIZ RAPORU")
    print("="*50)
    print(f"Hata Payi (RMSE): {np.sqrt(mean_squared_error(y_test, y_pred)):.2f} Cycle (Ucus Degeri)")
    print(f"R2 Score: %{r2_score(y_test, y_pred)*100:.2f}")
    print("="*50)