# 神策數據API查詢工具

## 項目目錄說明
```
1. bin： python程式
2. conf： API查詢工具設定組態檔
3. log : 程式日誌輸入位置
4. export: 輸出csv或是json檔案位置
5. requirement.txt : python3 所需要的lib
6. start.sh 程式啟動入口
7. main.py 程式主執行
```

## 功能說明

```
1. 基本API查詢
2. 可選帳號密碼或是使用使用Token登入
3. 將查詢結果輸出成csv或是json
4. 加入自定義ETL清洗邏輯
5. 藉由微信機器人推播清洗完的數據
```

## conf 設定組態檔說明

```
1. 請依組態檔內註解說名配置
2. 必填項目不可缺漏
3. 如果輸入內容過多，換行需要前面加上空格
```

## 程式執行方式
```
1. 請使用python3以上版本
2. 執行前先使用 pip install -r requirements.txt --no-index ，安裝所需lib
3. 至終端機輸入 sh start.sh
```