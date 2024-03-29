# Vocabulary Quiz

## Features
+ 簡易的 CLI 拼字測驗
+ 簡易的 Google 發音
+ 簡易的結果統計

## Usage

### Setup
+ `$ python3 -m pip install -r requirements.txt`

### Take a Quiz
+ `$ python3 vocabulary.py`

### Add Vocabulary Set
+ 方法 A
  + 照著 `data` 資料夾裡的 `.json` 檔格式寫
+ 方法 B
  + 將資料寫成 `.tsv` 格式
    ```tsv
    apple	(n.) 蘋果
	banana	(n.) 香蕉
	...
	```
  + 執行 `$ convert.py [source_file] [title]`

## Results
+ 測驗結果會存在 `'./results/'` 資料夾下

## Reference
+ App [超級單字王](https://superwordking.wixsite.com/home)
+ App [懶人背單字 Vocabulazy](https://tinyurl.com/y62tatol)