# BẢN TỪ ĐIỂN DỮ LIỆU TÀI CHÍNH (FINANCIAL DATA DICTIONARY)
<!-- maintained-by: antigravity-ide | domain: finance-analytics-engineering -->

Tài liệu này chuẩn hóa toàn bộ các lược đồ dữ liệu (Star Schema & Medallion Data Lakehouse) được kế thừa trực tiếp từ đề tài Khóa luận Tốt nghiệp (`F:\thuc-tap-2026\03_Khoa_Luan_Tot_Nghiep`) để làm cơ sở triển khai lên nền tảng **AWS Cloud (S3, AWS Glue, Amazon Athena, Amazon RDS, Amazon DynamoDB)** trong chương trình thực tập FCAJ của **Mr.Híu**.

---

## 1. PHÂN TẦNG LƯU TRỮ MEDALLION (S3 DATA LAKEHOUSE)

- **Bronze Zone (`s3://fcaj-financial-datalake/bronze/` hoặc `raw/`)**: Dữ liệu chuỗi thời gian giao dịch thô (JSON/CSV) thu thập từ các API thị trường tài chính (Vnstock API, Yahoo Finance, FRED, SBV).
- **Silver Zone (`s3://fcaj-financial-datalake/silver/` hoặc `processed/`)**: Dữ liệu đã được làm sạch, khử trùng lặp (deduplicated), chuẩn hóa kiểu dữ liệu, định dạng Columnar Parquet (Snappy compression), phân vùng (partitioned) theo `year` và `ticker`.
- **Gold Zone (`s3://fcaj-financial-datalake/gold/` hoặc `curated/`)**: Dữ liệu tính toán đặc trưng tài chính (Feature Store trễ $t-1$), bảng điểm rủi ro thị trường ($VaR$, $ES$) và các kết quả phân tích theo chuẩn Basel III phục vụ báo cáo BI trên QuickSight và truy vấn tốc độ cao.

---

## 2. LƯỢC ĐỒ STAR SCHEMA (DWH DATA MODEL)

### 2.1. Dimension Tables (Bảng Chiều)

#### Bảng `Dim_Asset` (Danh mục Tài sản & Cổ phiếu Ngân hàng)
- **Vị trí lưu trữ**: Amazon RDS PostgreSQL (Master) & S3 Silver/Gold Parquet.
- **Mô tả**: Quản lý danh mục 26 Ngân hàng TMCP tại Việt Nam cùng các chỉ số vĩ mô đối sánh.

| Tên trường (Column) | Kiểu dữ liệu (Data Type) | Ràng buộc (Constraint) | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- | :--- |
| `asset_id` | `VARCHAR(10)` | Primary Key | Mã định danh tài sản (VD: `VCB`, `BID`, `CTG`, `VNINDEX`, `USDVND`) |
| `asset_name` | `VARCHAR(100)` | NOT NULL | Tên đầy đủ của ngân hàng hoặc chỉ số tài chính |
| `exchange` | `VARCHAR(10)` | NOT NULL | Sàn giao dịch niêm yết (`HOSE`, `HNX`, `UPCOM`, `MACRO`) |
| `sector` | `VARCHAR(50)` | NOT NULL | Phân ngành hoạt động (`Commercial Banking`, `Macro Index`) |
| `is_vn30` | `BOOLEAN` | DEFAULT FALSE | Cờ đánh dấu thuộc rổ chỉ số vốn hóa lớn VN30 |
| `active_status` | `BOOLEAN` | DEFAULT TRUE | Trạng thái đang niêm yết và giao dịch |

#### Bảng `Dim_Date` (Master Trading Calendar)
- **Vị trí lưu trữ**: Amazon RDS PostgreSQL & S3 Silver/Gold Parquet.
- **Mô tả**: Lịch giao dịch chuẩn của thị trường chứng khoán Việt Nam (2017–2025), loại trừ thứ Bảy, Chủ nhật và các ngày nghỉ lễ theo quy định.

| Tên trường (Column) | Kiểu dữ liệu (Data Type) | Ràng buộc (Constraint) | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- | :--- |
| `date_key` | `INTEGER` | Primary Key | Khóa định dạng số nguyên `YYYYMMDD` (VD: `20240102`) |
| `full_date` | `DATE` | NOT NULL | Ngày tháng chuẩn ISO-8601 |
| `year` | `SMALLINT` | NOT NULL | Năm giao dịch |
| `quarter` | `SMALLINT` | NOT NULL | Quý giao dịch (1–4) |
| `month` | `SMALLINT` | NOT NULL | Tháng giao dịch (1–12) |
| `day_of_week` | `SMALLINT` | NOT NULL | Ngày trong tuần (2–6 cho các ngày giao dịch) |
| `is_trading_day`| `BOOLEAN` | NOT NULL | Cờ xác định ngày mở cửa khớp lệnh |

---

### 2.2. Fact Tables (Bảng Sự kiện)

#### Bảng `Fact_Market_Prices` (Chuỗi Giá & Khối lượng Giao dịch)
- **Vị trí lưu trữ**: S3 Silver Zone (`s3://fcaj-financial-datalake/silver/market_prices/`).
- **Phân vùng (Partitioning)**: `year=YYYY/ticker=XXXX`

| Tên trường (Column) | Kiểu dữ liệu | Ý nghĩa & Công thức |
| :--- | :--- | :--- |
| `date_key` | `INTEGER` | Khóa liên kết đến `Dim_Date` |
| `asset_id` | `VARCHAR(10)` | Khóa liên kết đến `Dim_Asset` |
| `open_price` | `DECIMAL(18,2)` | Giá mở cửa đã điều chỉnh quyền (Adjusted Open) |
| `high_price` | `DECIMAL(18,2)` | Giá cao nhất trong phiên |
| `low_price` | `DECIMAL(18,2)` | Giá thấp nhất trong phiên |
| `close_price` | `DECIMAL(18,2)` | Giá đóng cửa phiên giao dịch |
| `volume` | `BIGINT` | Khối lượng cổ phiếu khớp lệnh |
| `log_return` | `DECIMAL(18,6)` | Tỷ suất sinh lời logarit: $r_t = \ln(P_t / P_{t-1})$ |

#### Bảng `Fact_Feature_Store` (18 Đặc trưng Tài chính trễ $t-1$)
- **Vị trí lưu trữ**: Amazon DynamoDB (Real-time Serving) & S3 Gold Zone (Batch Analytics).
- **Ràng buộc an toàn dữ liệu**: Đảm bảo **Zero Look-Ahead Bias** bằng cách áp dụng độ trễ trọn vẹn $t-1$ trước khi đưa vào mô hình dự báo.

| Nhóm đặc trưng | Tên trường (Feature) | Kiểu dữ liệu | Công thức & Diễn giải kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Biến động giá** | `vol_garch_11` | `FLOAT` | Biến động điều kiện trích xuất từ mô hình $GARCH(1,1)$ |
| | `vol_garman_klass` | `FLOAT` | Đo lường biến động nội phiên dựa trên Open, High, Low, Close |
| | `vol_parkinson` | `FLOAT` | Đo lường biến động biên độ giá cực đại (High - Low) |
| | `vol_rolling_20d` | `FLOAT` | Độ lệch chuẩn lịch sử tỷ suất sinh lời 20 phiên |
| **Động lượng & Kỹ thuật** | `rsi_14d` | `FLOAT` | Chỉ số sức mạnh tương đối 14 ngày |
| | `macd_diff` | `FLOAT` | Hiệu số giữa MACD line và Signal line |
| | `bb_width` | `FLOAT` | Độ rộng dải Bollinger Bands (20 ngày, 2 độ lệch chuẩn) |
| | `momentum_5d` | `FLOAT` | Động lượng giá ngắn hạn 5 phiên |
| **Vĩ mô & Thị trường** | `interbank_rate` | `FLOAT` | Lãi suất liên ngân hàng kỳ hạn qua đêm (SBV) |
| | `usdvnd_change` | `FLOAT` | Tốc độ biến động tỷ giá hối đoái $USD/VND$ |
| | `vnindex_return` | `FLOAT` | Tỷ suất sinh lời của chỉ số thị trường chung $VN\text{-}Index$ |

#### Bảng `Fact_Risk_Forecasts` (Kết quả Dự báo Rủi ro Đuôi Basel III)
- **Vị trí lưu trữ**: S3 Gold Zone (`s3://fcaj-financial-datalake/gold/risk_forecasts/`).
- **Mục đích**: Cung cấp nguồn cấp dữ liệu cho Amazon Athena và Amazon QuickSight xây dựng Dashboard điều hành rủi ro.

| Tên trường (Column) | Kiểu dữ liệu | Ý nghĩa định lượng rủi ro |
| :--- | :--- | :--- |
| `forecast_id` | `VARCHAR(36)` | Khóa chính duy nhất (UUID) |
| `date_key` | `INTEGER` | Ngày thực hiện dự báo |
| `asset_id` | `VARCHAR(10)` | Mã tài sản / danh mục |
| `model_code` | `VARCHAR(20)` | Định danh thuật toán (`LGBM_QR`, `GARCH_EVT`, `BASELINE`) |
| `var_99` | `DECIMAL(12,6)` | Giá trị chịu rủi ro ở mức độ tin cậy 99% ($VaR_{99\%}$) |
| `es_975` | `DECIMAL(12,6)` | Giá trị chịu rủi ro có điều kiện chuẩn Basel III ($ES_{97.5\%}$) |
| `actual_loss` | `DECIMAL(12,6)` | Lỗ thực tế phát sinh tại phiên $t$ |
| `violation_flag`| `BOOLEAN` | Đánh dấu vi phạm ngưỡng rủi ro ($actual\_loss > var\_99$) |
| `basel_zone` | `VARCHAR(10)` | Phân vùng kiểm định giám sát Basel (`GREEN`, `YELLOW`, `RED`) |

---

## 3. MÔ HÌNH PHỤC VỤ DỮ LIỆU TỐC ĐỘ CAO TRÊN DYNAMODB (WEEK 10)

Để phục vụ các ứng dụng tài chính yêu cầu độ trễ cực thấp (Sub-10ms API):
- **Table Name**: `FinancialFeatureStore`
- **Billing Mode**: On-Demand (PAY_PER_REQUEST - Tiết kiệm chi phí tối đa khi nhàn rỗi)
- **Partition Key (`PK`)**: `TICKER#<asset_id>` (VD: `TICKER#VCB`)
- **Sort Key (`SK`)**: `DATE#<date_key>` (VD: `DATE#20261028`)
- **Global Secondary Index (`GSI1`)**: 
  - `GSI1-PK`: `DATE#<date_key>`
  - `GSI1-SK`: `TICKER#<asset_id>`
  - **Mục đích GSI**: Cho phép quét toàn bộ các chỉ số của toàn thị trường trong cùng 1 ngày chỉ với 1 truy vấn `Query`.

