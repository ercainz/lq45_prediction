# Prediksi Nilai Index LQ45
---
Memprediksi nilai Indeks LQ45 3 hari ke depan menggunakan _Model SARIMAX_.


## DESKRIPSI PROJECT
### Background Permasalahan:
Belom kelar...

### Arsitektur Project:
Belom kelar....

### Expected Output:
Belom kelar...


## DOKUMENTASI PROJECT
### Data yang Diperlukan:
Belom kelar...

### Output prediksi via API:
Belom kelar...

### Workflow dari Project:
* Blok Diagram Persiapan Data
* Blok Diagram Preprocessing
* Blok Diagram Features Engineering
* Blok Diagram Pemodelan dan Evaluasinya


## DATASET
### Format data:
* **header csv** - *date,lq45,jci,idx30,eido,spy,dom_b,dom_s,for_b,for_s*.
* `date` - tipe data **date** dengan format `yyyy-mm-dd`.
* `lq45` - tipe data **float** dengan format `.4f`
* `jci` - tipe data **float** dengan format `.4f`
* `idx30` - tipe data **float** dengan format `.4f`
* `eido` - tipe data **float** dengan format `.4f`
* `spy` - tipe data **float** dengan format `.4f`
* `dom_b` - tipe data **float** dengan format `.4f`
* `dom_s` - tipe data **float** dengan format `.4f`
* `for_b` - tipe data **float** dengan format `.4f`
* `for_s` - tipe data **float** dengan format `.4f`

### Penjelasan:
* `date` - Deret waktu dengan periode harian, sesuai dengan kalender hari kerja di Indonesia.
* `lq45` - Harga penutupan Index LQ45.
> * Merupakan representasi/cerminan harga saham dari 45 emiten yang ada di Bursa Efek Indonesia (BEI) yang dipilih berdasarkan pertimbangan likuiditas tertinggi dan kapitalisasi pasar terbesar dengan kriteria-kriteria lain yang sudah ditentukan.
* `jci` - Harga penutupan IHSG (Index Harga Saham Gabungan)
> * Merupakan cerminan harga dari seluruh saham yang ada di Bursa Efek Indonesia (BEI).
* `idx30` - Harga penutupan Index IDX-30
> * Merupakan indeks saham yang mengukur kinerja harga dari 30 saham yang memiliki likuiditas tinggi dan kapitalisasi pasar yang besar serta didukung oleh kekuatan fundamental perusahaannya yang baik.
* `eido` - Harga penutupan Index EIDO
> * Merupakan indeks Mutual Fund sejenis ETF (Exchange Traded Fund) atau reksadana dibursa "NYSE / New York Stock Exchange", yang didalamnya terdapat saham-saham Indonesia yang dipilih berdasarkan kriteria dari MSCI (Morgan Stanley Composite Index).
* `spy` - Harga penutupan Index Standard & Poor's 500 - S&P 500
> * Merupakan adalah representasi/cerminan harga saham dari 500 emiten Amerika Serikat yang dipilih berdasarkan kapitalisasi pasar, likuiditas, kelompok industri, beserta sejumlah kriteria lainnya. Emiten dalam indeks S&P 500 dipilih oleh Komite Indeks S&P.
* `dom_b` - Jumlah nominal transaksi pembelian domestik (dalam satuan triliun)
* `dom_s` - Jumlah nominal transaksi penjualan domestik (dalam satuan triliun)
* `for_b` - Jumlah nominal transaksi pembelian asing (dalam satuan triliun)
* `for_s` - Jumlah nominal transaksi penjualan asing (dalam satuan triliun)

## CARA PENGGUNAAN
### Format input untuk melakukan prediksi via API:
Menggunakan format standar *json* dengan *key* sebagai berikut:

* `date` - Tanggal dengan format `yyyymmdd`
> * tipe data **string** dan harus terdiri dari 8 karakter
* `jci` - Nilai penutupan indeks IHSG pada tanggal `date`
> * tipe data **float** dengan rentang nilai 1,000 hingga 20,000
* `idx30` - Nilai penutupan indeks IDX-30 pada tanggal `date`
> * tipe data **float** dengan rentang nilai 100 hingga 5,000
* `eido` - Nilai penutupan indeks EIDO pada tanggal `date`
> * tipe data **float** dengan rentang nilai 1 hingga 200
* `spy` - Nilai penutupan indeks S&P 500 pada tanggal `date`
> * tipe data **float** dengan rentang nilai 1 hingga 5,000
* `dom_b` - Jumlah nominal transaksi pembelian domestik (dalam satuan triliun) pada tanggal `date`
> * tipe data **float** dengan rentang nilai 0.01 hingga 100
* `dom_s` - Jumlah nominal transaksi penjualan domestik (dalam satuan triliun) pada tanggal `date`
> * tipe data **float** dengan rentang nilai 0.01 hingga 100
* `for_b` - Jumlah nominal transaksi pembelian asing (dalam satuan triliun) pada tanggal `date`
> * tipe data **float** dengan rentang nilai 0.01 hingga 100
* `for_s` - Jumlah nominal transaksi penjualan asing (dalam satuan triliun) pada tanggal `date`
> * tipe data **float** dengan rentang nilai 0.01 hingga 100

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

### Format output Respons dari API:
Respons juga berupa format standar *json* dengan *key* sebagai berikut:

* `input_date` - Tanggal sesuai input `date` dengan format `yyyymmdd`
> * tipe data **string** yang terdiri dari 8 karakter
* `pred_value` - Hasil prediksi Nilai indeks LQ45 3 hari kerja setelah `input_date`
> * tipe data **float**
* `pred_desc` - Deskripsi hasil prediksi
> * tipe data **string**

Contoh:
```json
{
    "input_date": "20220328",
    "pred_value": 1053.672,
    "pred_desc": "3 Business Days after 28-Mar-2022, LQ45 value would be 1053.672"
}
```

### Menjalankan Layanan Machine Learning di Komputer Lokal:
* **Melakukan Retrain Model** :
> * Dari folder root, jalankan script python `remodelling.py` pada folder *src*
> * Pastikan dataset sudah berada di folder *[root]/data/raw* dengan nama file *dataset_Q122.csv* dengan format yang sesuai.
```
python src\remodelling.py
```
* **Menjalankan API** :
> * Dari folder root, jalankan script python `api.py` pada folder *src*
> * Setelah server API menyala (URL : *localhost:8080/pred/*), lakukan API POST dengan format json yang sesuai.

```
python src\api.py --reload
```
> ![api_00](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/api_00.jpg)

> ![api_01](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/api_01.jpg)

> ![api_02](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/api_02.jpg)

> ![api_03](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/api_03.jpg)

> ![api_04](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/api_04.jpg)

## KESIMPULAN
Model *SARIMAX* yang merupakan pengembangan dari model *ARIMA*/*ARIMAX*/*SARIMA* secara umum dapat digunakan untuk melakukan prediksi nilai indeks LQ45 3 hari ke depan. Namun hasil prediksi dirasa masih kurang akurat. Hal ini sebenarnya dapat diatasi dengan melakukan eksplorasi tiap-tiap *fitur* dengan lebih mendalam. Bisa juga dengan melakukan *hyperparameter tunning* yang lebih variatif pada model.

Untuk penelitian lebih lanjut, dapat coba digunakan model machine learning *LSTM (Long Short Term Memory network)* dan/atau *GRU (Gated Recurrent Unit)* yang menurut beberapa sumber, dapat menghasilkan performa yang lebih baik ketimbang model *SARIMAX*.

## REFERENSI
### Lingkup bisnis:
* [Mengenal LQ45, Indeks Saham Paling Populer dan Perbedaannya dengan Saham Bluechip (by: Siti Hadijah)](https://www.cermati.com/artikel/mengenal-lq45-indeks-saham-paling-populer-dan-perbedaannya-dengan-saham-bluechip)
* [ETF Saham Eido dan Kinerjanya pada Bursa Efek (by: Jonathan Siahaan)](https://admiralmarkets.sc/id/education/articles/shares/etf-saham-eido)
* [Informasi Umum Seputar S&P 500](https://help.pluang.com/knowledge/informasi-umum-seputar-snp-500)


### Seasonal decomposition:
* [statsmodels seasonal_decompose](https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.seasonal_decompose.html)
* [How to Decompose Time Series Data into Trend and Seasonality (by: Jason Brownlee)](https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/)

### Pemodelan SARIMAX:
* [statsmodels SARIMAX](https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html)
* [pmdarima](https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.auto_arima.html)
* [Time Series Forecasting with ARIMA , SARIMA and SARIMAX (by: Brendan Artley)](https://towardsdatascience.com/time-series-forecasting-with-arima-sarima-and-sarimax-ee61099e78f6)
* [Time Series Forecasting: ARIMA vs LSTM vs PROPHET (by: Mauro Di Pietro)](https://medium.com/analytics-vidhya/time-series-forecasting-arima-vs-lstm-vs-prophet-62241c203a3b)
* [ARIMA Model – Complete Guide to Time Series Forecasting in Python (by: Selva Prabhakaran)](https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/)


### Panduan Lengkap:
* [Inflation Forecasting (by: SwatiSethee)](https://medium.com/inflation-forecasting-using-sarimax-and-nkpc/plotting-monthly-inflation-over-the-selected-time-period-to-check-if-the-time-series-has-any-35e3b1fac761)
* [Complete Guide To SARIMAX in Python for Time Series Modeling (by: Yugesh Verma)](https://analyticsindiamag.com/complete-guide-to-sarimax-in-python-for-time-series-modeling/)

