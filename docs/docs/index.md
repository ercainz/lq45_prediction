# Prediksi Nilai Index LQ45
> Memprediksi harga penutupan Indeks LQ45 pada 3 hari ke depan menggunakan _Model SARIMAX_.

---
## DESKRIPSI PROJECT
### Background Permasalahan
Pada dunia pasar modal, tentunya banyak orang yang ingin mendapatkan keuntungan yang maksimal. Untuk mencapai tujuan tersebut, sebenarnya ada banyak metode analisa yang dapat dilakukan. Namun untuk mempelajari dan menerapkannya diperlukan waktu dan ketekunan yang konsisten setiap harinya. Hal itu relatif sulit bagi sebagian orang, terlebih lagi bagi mereka yang mempunyai rutinitas yang padat.<br>

Pada project ini, dimaksudkan untuk mengatasi problematik tersebut. Project ini akan mencoba melakukan prediksi harga penutupan salah satu indeks saham yang cukup populer di kalangan dunia pasar modal, yaitu **Indeks LQ45**. 

Nilai indeks LQ45 yang akan diprediksi adalah harga penutupan pada 3 hari ke depan. Pemilihan angka *3 hari* didapatkan dari hasil analisa dari beberapa analis saham, yang mengatakan bahwa *kejadian di T0 idealnya akan terasa efeknya hingga 3-4 hari ke depan*.

Diharapkan dengan mengetahui harga penutupan pada 3 hari ke depan, *User* dapat melakukan tindakan yang tepat (beli atau jual) untuk memaksimalkan keuntungan mereka.

![lq45_closeprice](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/lq45_closeprice.jpg)

Dari gambar, dapat dilihat bahwa data yang akan diprediksi berupa deret waktu. Salah satu model *machine learning* yang umum digunakan untuk melakukan pemodelan regresi deret waktu adalah *ARIMA*. *ARIMA* merupakan jenis model regresi *univariate*, sehingga yang tidak memerlukan fitur tambahan apapun untuk menghasilkan prediksi. *ARIMA* memiliki 3 parameter dasar, yaitu AR - Autoregressive (`p`), I - Integrated (`d`), MA - Moving Average (`q`). Model *ARIMA* memiliki beberapa pengembangan seiring kemajuan jaman, yaitu *SARIMA*, *ARIMAX*, dan *SARIMAX*.

*(S)ARIMA* merupakan pengembangan model *ARIMA* dengan tambahan parameter *seasonal* yang dapat mendeteksi adanya efek musiman untuk periode waktu yang lebih besar. Misalnya, untuk data dengan rentang waktu bulanan, efek musiman dapat melihat pola musiman secara tahunan (per 12 bulan). *SARIMA* memiliki tambahan 3 parameter tambahan selain *seasonal* (`S`), yaitu Seasonal-Autoregressive (`P`), Seasonal-Integrated (`D`), Seasonal-Moving Average (`Q`).

*ARIMA(X)* merupakan pengembangan model *ARIMA* yang menggunakan tambahan fitur-fitur eksogen untuk menghasilkan prediksi. Hal ini dipercaya dapat meningkatkan performa dari model *ARIMA* biasa.

*(S)ARIMA(X)* merupakan gabungan dari model *SARIMA* dan *ARIMAX*. Model inilah yang akan digunakan pada project ini.


### Arsitektur Project
Berikut *arsitektur* project secara umum:
![arsitektur](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/arsitektur.jpg)

Penjelasan singkat:

1. Pada **Proses prediksi** (tanda panah warna biru dan merah) data input didapatkan dari *User* melalui API. Sedangkan untuk **Proses retrain model** (tanda panah warna hijau) data didapat dalam bentuk file csv.
2. Pada **Proses prediksi**, tahapan proses yang dilalui di dalam *Sistem Machine Learning* adalah: *Validasi Data*, *Preprocessing Data & Feature Engineering*, dan *Predictor*.
4. *Predictor* adalah output yang dihasilkan pada **Proses retrain model** setelah berhasil didapatkan *Model Best-Fit*.
5. Pada **Proses retrain model**, ada tambahan proses *Splitting Data*, *Fit & Train Model*. 
6. Output dari *Predictor* akan dikembalikan ke *User* melalui API.


### Output yang diharapkan
* Prediksi harga penutupan Indeks LQ45 pada T+3.


## DETAIL PROJECT
### Data yang diperlukan
Berbeda dengan pemodelan menggunakan *ARIMA*/*SARIMA* yang hanya menggunakan satu variabel (univariate) deret waktu, pemodelan *SARIMAX* juga memerlukan input eksogen (X).<br>Untuk proses pelatihan, validasi, dan test model, diperlukan data berupa deret waktu dengan interval *harian* sejak 2012 hingga kuartal pertama 2022.<br>Berikut beberapa data yang akan digunakan dalam project ini:

1. Harga penutupan index LQ45 pada T+3 (hanya digunakan untuk pemodelan, namun tidak digunakan saat proses prediksi).
1. Harga penutupan Indeks IHSG pada T0.
1. Harga penutupan Indeks IDX-30 pada T0.
1. Harga penutupan Indeks EIDO pada T0.
1. Harga penutupan Indeks S&P 500 pada T0.
1. Jumlah nominal transaksi pembelian domestik pada T0.
1. Jumlah nominal transaksi penjualan domestik pada T0.
1. Jumlah nominal transaksi pembelian asing pada T0.
1. Jumlah nominal transaksi penjualan asing pada T0.

### Output prediksi via API
* Prediksi harga penutupan Indeks LQ45 pada T+3.

### Workflow Project (Proses Retrain Model)
Berikut *workflow* untuk **Proses Retrain Model**, setelah melalui beberapa kali proses *trial-error*:

1. Pengambilan data dari file csv dengan format yang sudah sesuai.
2. Validasi data untuk memastikan bahwa format sudah sesuai dengan ketentuan.
3. Resampling data dengan interval *hari kerja* (*senin, selasa, rabu, kamis, jumat*), sekaligus imputasi data point yang hilang dengan metode *ffill*.
4. Membentuk kolom `target` yang dibentuk dari kolom `lq45` yang di-*shift-forward* sejauh 3 data point.
5. Penambahan 4 fitur baru (`dom_tot`,`dom_net`,`for_tot`,`for_net`) yang bertujuan untuk memudahkan model dalam melakukan training.
> * `dom_tot` merupakan kolom `dom_b` dijumlahkan dengan kolom `dom_s`.
> * `dom_net` merupakan kolom `dom_b` dikurangkan dengan kolom `dom_s`.
> * `for_tot` merupakan kolom `for_b` dijumlahkan dengan kolom `for_s`.
> * `for_net` merupakan kolom `for_b` dikurangkan dengan kolom `for_s`.
6. Splitting data dengan komposisi:
> * **data train** adalah data sejak awal hingga *31-12-2020*.
> * **data validasi** adalah data sejak *01-01-2021* hingga *31-07-2021*.
> * **data test** adalah data sejak *01-08-2021* hingga data terakhir.
7. Penambahan fitur `seasonal` yang mempresentasikan *trend* dari kolom `target` dalam interval *bulanan*.
8. Mendeteksi data outlier pada semua kolom dengan metode *1.5 x IQR*, serta melakukan imputasi dengan nilai *percentile 10%* untuk outlier bawah, dan *percentile 90%* untuk outlier atas.
9. Proses scaling standardisasi untuk semua kolom, kecuali kolom `target`.
10. Proses pelatihan model dengan pustaka *pmdarima*, yang secara otomatis dapat menentukan parameter-parameter model *SARIMAX* yang terbaik.
11. Evaluasi model dilakukan pada **data validasi** dan **data test** dengan cara membandingkan hasil prediksi `pred` dengan kolom `target`.

Berikut ilustrasinya,

![flowchart_1](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/flowchart_1.jpg)

Catatan tambahan:
> * Setelah langkah ke 7 (Penambahan fitur `seasonal`), pernah dicoba dilakukan proses **Stationaring Data**, yaitu mentransformasi semua kolom menjadi bentuk yang stasioner dengan metode *first difference*. Menurut beberapa literatur, proses ini merupakan syarat pemodelan *ARIMA* dan turunannya. Namun saat proses ke 11 (Evaluasi model), menunjukkan bahwa proses **Stationaring Data** malah menghasilkan performa model yang buruk. Sehingga proses **Stationaring Data** ini tidak diterapkan.

### Workflow Project (Proses Prediksi)
Berikut *workflow* untuk **Proses Prediksi**:

1. Penerimaan data dari *User* melalui API dengan format yang sudah sesuai.
2. Validasi data untuk memastikan bahwa format sudah sesuai dengan ketentuan.
3. Proses konversi data kedalam bentuk *Pandas Dataframe*.
4. Penambahan 4 fitur baru (`dom_tot`,`dom_net`,`for_tot`,`for_net`) yang bertujuan untuk memudahkan model dalam melakukan training.
> * `dom_tot` merupakan kolom `dom_b` dijumlahkan dengan kolom `dom_s`.
> * `dom_net` merupakan kolom `dom_b` dikurangkan dengan kolom `dom_s`.
> * `for_tot` merupakan kolom `for_b` dijumlahkan dengan kolom `for_s`.
> * `for_net` merupakan kolom `for_b` dikurangkan dengan kolom `for_s`.
5. Penambahan fitur `seasonal` dari pickle dataframe yang sebelumnya dibuat saat proses pemodelan (file: **[root]\data\remodel\value_for_seasonal.pkl**).
6. Mendeteksi data outlier pada semua kolom, serta melakukan imputasi dengan nilai dari pickle dataframe yang sebelumnya dibuat saat proses pemodelan (file: **[root]\data\remodel\value_for_outlier.pkl**).
7. Proses scaling standardisasi untuk semua kolom menggunakan pickle scaler yang sebelumnya dibuat saat proses pemodelan (file: **[root]\data\remodel\scaler_x.pkl**).
8. Proses prediksi menggunakan model yang sebelumnya dibuat saat proses pemodelan (file: **[root]\models\sarimax.pkl**).
9. Pengiriman hasil prediksi kembali ke *User* melalui API.

Berikut ilustrasinya,

![flowchart_2](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/flowchart_2.jpg)


## DATASET
### Format dan deskripsi data
**header csv** - *date,lq45,jci,idx30,eido,spy,dom_b,dom_s,for_b,for_s*

| Header | Tipe Data | Definisi | Deskripsi |
| ------ | ---- | ---- | ---- |
| `date`  | **date**<br>dengan format<br>`yyyy-mm-dd` | Deret waktu dengan<br>periode harian,<br>sesuai dengan kalender<br>hari kerja di Indonesia. | |
| `lq45`  | **float**<br>dengan format `.4f` | Harga penutupan Index<br>LQ45 | Representasi/cerminan harga<br>saham dari 45 emiten  yang<br>ada di Bursa Efek Indonesia<br>(BEI) yang dipilih berdasarkan<br>pertimbangan likuiditas<br>tertinggi dan kapitalisasi<br>pasar terbesar dengan<br>kriteria-kriteria lain<br>yang sudah ditentukan. |
| `jci`   | **float**<br>dengan format `.4f` | Harga penutupan Index<br>IHSG (Index Harga Saham<br>Gabungan) | Cerminan harga dari<br>seluruh saham yang ada di<br>Bursa Efek Indonesia (BEI). |
| `idx30` | **float**<br>dengan format `.4f` | Harga penutupan Index<br>IDX-30| Indeks saham yang mengukur<br>kinerja harga dari 30 saham yang<br>memiliki likuiditas tinggi dan<br>kapitalisasi pasar yang besar serta<br>didukung oleh kekuatan<br>fundamental perusahaannya<br>yang baik. |
| `eido`  | **float**<br>dengan format `.4f` | Harga penutupan Index<br>EIDO | Indeks Mutual Fund sejenis ETF<br>(Exchange Traded Fund) atau<br>reksadana dibursa "NYSE /<br>New York Stock Exchange", yang<br>didalamnya terdapat saham-saham<br>Indonesia yang dipilih berdasarkan<br>kriteria dari MSCI (Morgan Stanley<br>Composite Index). |
| `spy`   | **float**<br>dengan format `.4f` | Harga penutupan Index<br>Standard & Poor's 500<br>(S&P 500) | Representasi/cerminan harga<br>saham dari 500 emiten Amerika<br>Serikat yang dipilih berdasarkan<br>kapitalisasi pasar, likuiditas,<br>kelompok industri, beserta sejumlah<br>kriteria lainnya. Emiten dalam<br>indeks S&P 500 dipilih oleh<br>Komite Indeks S&P. |
| `dom_b` | **float**<br>dengan format `.4f` | Jumlah nominal transaksi<br>pembelian domestik<br>(dalam satuan triliun) | |
| `dom_s` | **float**<br>dengan format `.4f` | Jumlah nominal transaksi<br>penjualan domestik<br>(dalam satuan triliun) | |
| `for_b` | **float**<br>dengan format `.4f` | Jumlah nominal transaksi<br>pembelian asing<br>(dalam satuan triliun) | |
| `for_s` | **float**<br>dengan format `.4f` | Jumlah nominal transaksi<br>penjualan asing<br>(dalam satuan triliun) | |


## CARA PENGGUNAAN
### Format input untuk melakukan prediksi via API
Menggunakan format standar *json* dengan *key* sebagai berikut:

* `date` - Tanggal dengan format `yyyymmdd`
> * tipe data **string** dan harus terdiri dari 8 karakter.
* `jci` - Nilai penutupan indeks IHSG pada tanggal `date`
> * tipe data **float** dengan rentang nilai 1,000 hingga 20,000.
* `idx30` - Nilai penutupan indeks IDX-30 pada tanggal `date`
> * tipe data **float** dengan rentang nilai 100 hingga 5,000.
* `eido` - Nilai penutupan indeks EIDO pada tanggal `date`
> * tipe data **float** dengan rentang nilai 1 hingga 200.
* `spy` - Nilai penutupan indeks S&P 500 pada tanggal `date`
> * tipe data **float** dengan rentang nilai 1 hingga 5,000.
* `dom_b` - Jumlah nominal transaksi pembelian domestik (dalam satuan triliun) pada tanggal `date`
> * tipe data **float** dengan rentang nilai 0.01 hingga 100.
* `dom_s` - Jumlah nominal transaksi penjualan domestik (dalam satuan triliun) pada tanggal `date`
> * tipe data **float** dengan rentang nilai 0.01 hingga 100.
* `for_b` - Jumlah nominal transaksi pembelian asing (dalam satuan triliun) pada tanggal `date`
> * tipe data **float** dengan rentang nilai 0.01 hingga 100.
* `for_s` - Jumlah nominal transaksi penjualan asing (dalam satuan triliun) pada tanggal `date`
> * tipe data **float** dengan rentang nilai 0.01 hingga 100.

Contoh:
```json
{
    "date": "20220328",
    "jci": 7049.6030,
    "idx30": 549.373,
    "eido": 24.92,
    "spy": 455.91,
    "dom_b": 9.9995,
    "dom_s": 10.8573,
    "for_b": 4.2166,
    "for_s": 3.3587
}
```

### Format output Respons dari API
Respons juga berupa format standar *json* dengan *key* sebagai berikut:

* `input_date` - Tanggal sesuai input `date` dengan format `yyyymmdd`
> * tipe data **string** yang terdiri dari 8 karakter.
* `pred_value` - Hasil prediksi Nilai indeks LQ45 3 hari kerja setelah `input_date`
> * tipe data **float**.
* `pred_desc` - Deskripsi dari hasil prediksi
> * tipe data **string**.


Contoh:
```json
{
    "input_date": "20220328",
    "pred_value": 1053.672,
    "pred_desc": "3 Business Days after 28-Mar-2022, LQ45 value would be 1053.672"
}
```

### Menjalankan Layanan Machine Learning di Komputer Lokal
* **Melakukan Retrain Model** :
> * Dari folder root, jalankan script python `remodelling.py` pada folder *src*.
> * Pastikan dataset sudah berada di folder **[root]/data/raw** dengan nama file **dataset_Q122.csv** dengan format yang sesuai.
```
python src\remodelling.py
```
* **Menjalankan API** :
> * Dari folder root, jalankan script python `api.py` pada folder *src*.
> * Setelah server API menyala (URL : *localhost:8080/pred/*), lakukan API POST dengan format json yang sesuai.

```
python src\api.py --reload
```
> ![api_server_up](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/api_server_up.jpg)

> ![api_client_test](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/api_client_test.jpg)


## KESIMPULAN
Model *SARIMAX* yang merupakan pengembangan dari model *ARIMA*/*ARIMAX*/*SARIMA* secara umum dapat digunakan untuk melakukan prediksi nilai indeks LQ45 3 hari ke depan.<br>Namun hasil prediksi dirasa masih kurang akurat.<br>Hal ini sebenarnya dapat diatasi dengan melakukan eksplorasi tiap-tiap *fitur* dengan lebih mendalam. Bisa juga dengan melakukan *hyperparameter tunning* yang lebih variatif pada model.

Untuk penelitian lebih lanjut, dapat coba digunakan model machine learning *LSTM (Long Short Term Memory network)* dan/atau *GRU (Gated Recurrent Unit)* yang menurut beberapa sumber, dapat menghasilkan performa yang lebih baik ketimbang model *SARIMAX*.

## REFERENSI
**Lingkup bisnis** :
> * [Mengenal LQ45, Indeks Saham Paling Populer dan Perbedaannya dengan Saham Bluechip (by: Siti Hadijah)](https://www.cermati.com/artikel/mengenal-lq45-indeks-saham-paling-populer-dan-perbedaannya-dengan-saham-bluechip)
> * [ETF Saham Eido dan Kinerjanya pada Bursa Efek (by: Jonathan Siahaan)](https://admiralmarkets.sc/id/education/articles/shares/etf-saham-eido)
> * [Informasi Umum Seputar S&P 500](https://help.pluang.com/knowledge/informasi-umum-seputar-snp-500)


**Dekomposisi seasonal dan ADF Test** :
> * [statsmodels seasonal_decompose](https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.seasonal_decompose.html)
> * [How to Decompose Time Series Data into Trend and Seasonality (by: Jason Brownlee)](https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/)
> * [Augmented Dickey Fuller Test (ADF Test) – Must Read Guide (by: Selva Prabhakaran)](https://www.machinelearningplus.com/time-series/augmented-dickey-fuller-test/)

**ARIMA, ARIMAX, SARIMA, SARIMAX** :
> * [statsmodels SARIMAX](https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html)
> * [pmdarima](https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.auto_arima.html)
> * [Time Series Forecasting with ARIMA , SARIMA and SARIMAX (by: Brendan Artley)](https://towardsdatascience.com/time-series-forecasting-with-arima-sarima-and-sarimax-ee61099e78f6)
> * [How to Create an ARIMA Model for Time Series Forecasting in Python (by: Jason Brownlee)](https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/)
> * [An Introduction to Time Series Analysis with ARIMA (by: Taha Binhuraib)](https://towardsdatascience.com/an-introduction-to-time-series-analysis-with-arima-a8b9c9a961fb)
> * [Time Series Forecasting: ARIMA vs LSTM vs PROPHET (by: Mauro Di Pietro)](https://medium.com/analytics-vidhya/time-series-forecasting-arima-vs-lstm-vs-prophet-62241c203a3b)
> * [ARIMA Model – Complete Guide to Time Series Forecasting in Python (by: Selva Prabhakaran)](https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/)


**Panduan lengkap**:
> * [Inflation Forecasting (by: SwatiSethee)](https://medium.com/inflation-forecasting-using-sarimax-and-nkpc/plotting-monthly-inflation-over-the-selected-time-period-to-check-if-the-time-series-has-any-35e3b1fac761)
> * [Complete Guide To SARIMAX in Python for Time Series Modeling (by: Yugesh Verma)](https://analyticsindiamag.com/complete-guide-to-sarimax-in-python-for-time-series-modeling/)

