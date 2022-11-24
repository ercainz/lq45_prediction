# Prediksi Nilai Index LQ45
---
Memprediksi nilai Indeks LQ45 3 hari ke depan menggunakan _Model SARIMAX_.


## DESKRIPSI PROJECT
### Background Permasalahan:
Belom kelar...

### Arsitektur Project:
Belom kelar....

### Output yang diharapkan:
* Prediksi harga penutupan Indeks LQ45 pada T+3.


## DOKUMENTASI PROJECT
### Data yang diperlukan:
Berbeda dengan pemodelan menggunakan *ARIMA*/*SARIMA* yang hanya menggunakan satu variabel (univariate) deret waktu, pemodelan *SARIMAX* juga memerlukan input eksogen (X).<br>Untuk proses pelatihan, validasi, dan test model, diperlukan data berupa deret waktu dengan interval *harian* sejak 2012 hingga kuartal pertama 2022.<br>Berikut beberapa data yang akan digunakan dalam project ini:

* Harga penutupan index LQ45 pada T+3 (hanya digunakan untuk pemodelan, namun tidak digunakan saat proses prediksi).

* Harga penutupan Indeks IHSG pada T0.

* Harga penutupan Indeks IDX-30 pada T0.

* Harga penutupan Indeks EIDO pada T0.

* Harga penutupan Indeks S&P 500 pada T0.

* Jumlah nominal transaksi pembelian domestik pada T0.

* Jumlah nominal transaksi penjualan domestik pada T0.

* Jumlah nominal transaksi pembelian asing pada T0.

* Jumlah nominal transaksi penjualan asing pada T0.

### Output prediksi via API:
* Prediksi harga penutupan Indeks LQ45 pada T+3.

### Workflow dari Project:
* Blok Diagram Persiapan Data
* Blok Diagram Preprocessing
* Blok Diagram Features Engineering
* Blok Diagram Pemodelan dan Evaluasinya


## DATASET
### Format dan deskripsi data:
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
> ![api_server_up](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/api_server_up.jpg)

> ![api_client_test](https://raw.githubusercontent.com/ercainz/lq45_prediction/main/docs/images/api_client_test.jpg)


## KESIMPULAN
Model *SARIMAX* yang merupakan pengembangan dari model *ARIMA*/*ARIMAX*/*SARIMA* secara umum dapat digunakan untuk melakukan prediksi nilai indeks LQ45 3 hari ke depan.<br>Namun hasil prediksi dirasa masih kurang akurat.<br>Hal ini sebenarnya dapat diatasi dengan melakukan eksplorasi tiap-tiap *fitur* dengan lebih mendalam. Bisa juga dengan melakukan *hyperparameter tunning* yang lebih variatif pada model.

Untuk penelitian lebih lanjut, dapat coba digunakan model machine learning *LSTM (Long Short Term Memory network)* dan/atau *GRU (Gated Recurrent Unit)* yang menurut beberapa sumber, dapat menghasilkan performa yang lebih baik ketimbang model *SARIMAX*.

## REFERENSI
**Lingkup bisnis**:
> * [Mengenal LQ45, Indeks Saham Paling Populer dan Perbedaannya dengan Saham Bluechip (by: Siti Hadijah)](https://www.cermati.com/artikel/mengenal-lq45-indeks-saham-paling-populer-dan-perbedaannya-dengan-saham-bluechip)
> * [ETF Saham Eido dan Kinerjanya pada Bursa Efek (by: Jonathan Siahaan)](https://admiralmarkets.sc/id/education/articles/shares/etf-saham-eido)
> * [Informasi Umum Seputar S&P 500](https://help.pluang.com/knowledge/informasi-umum-seputar-snp-500)


**Dekomposisi Seasonal**:
> * [statsmodels seasonal_decompose](https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.seasonal_decompose.html)
> * [How to Decompose Time Series Data into Trend and Seasonality (by: Jason Brownlee)](https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/)

**Pemodelan SARIMAX**:
> * [statsmodels SARIMAX](https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html)
> * [pmdarima](https://alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.auto_arima.html)
> * [Time Series Forecasting with ARIMA , SARIMA and SARIMAX (by: Brendan Artley)](https://towardsdatascience.com/time-series-forecasting-with-arima-sarima-and-sarimax-ee61099e78f6)
> * [Time Series Forecasting: ARIMA vs LSTM vs PROPHET (by: Mauro Di Pietro)](https://medium.com/analytics-vidhya/time-series-forecasting-arima-vs-lstm-vs-prophet-62241c203a3b)
> * [ARIMA Model – Complete Guide to Time Series Forecasting in Python (by: Selva Prabhakaran)](https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/)


**Panduan Lengkap**:
> * [Inflation Forecasting (by: SwatiSethee)](https://medium.com/inflation-forecasting-using-sarimax-and-nkpc/plotting-monthly-inflation-over-the-selected-time-period-to-check-if-the-time-series-has-any-35e3b1fac761)
> * [Complete Guide To SARIMAX in Python for Time Series Modeling (by: Yugesh Verma)](https://analyticsindiamag.com/complete-guide-to-sarimax-in-python-for-time-series-modeling/)

