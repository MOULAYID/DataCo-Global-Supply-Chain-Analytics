# Spec-Driven Development (SDD): Data Analysis & Feature Engineering Plan

## 1. Exploratory Data Analysis & Transformation Blueprint
1. **Schema Auditing & Type Casting**:
   - `order date (DateOrders)` & `shipping date (DateOrders)` -> Datetime conversion.
   - Text standardizations (strip whitespace, upper case categorization).
   - Missing Value Handling:
     - `Product Description`: Drop or replace with placeholder (100% missing).
     - `Order Zipcode`: Impute via City/Country mapping where possible, or flag as missing.
     - `Customer Lname`, `Customer Zipcode`: Standard median/mode or string imputations.
2. **Engineered Feature Specifications**:
   - `shipping_delay_days`: `Days for shipping (real)` - `Days for shipment (scheduled)`
   - `is_late`: Binary flag (`Late_delivery_risk` == 1)
   - `order_processing_time_hours`: Hours between order timestamp and shipping timestamp.
   - `profit_margin_pct`: `Order Profit Per Order` / `Sales`
   - `total_item_value`: `Order Item Product Price` * `Order Item Quantity`
   - `discount_amount`: `Order Item Discount`
   - `customer_tenure_days`: Difference between customer's first order and last order date.
   - `customer_order_count`: Total order count per `Customer Id`.
   - `customer_total_spend`: Cumulative spend per `Customer Id`.
   - `avg_basket_value`: `Sales` / `Order Item Quantity`.
   - Time Extractors: `order_year`, `order_month`, `order_dayofweek`, `order_hour`, `order_quarter`, `is_weekend`, `season`.
   - Rolling Features: 7-day and 30-day moving average sales volume.

## 2. Statistical Analysis Methodology
1. **Normality Testing**: Shapiro-Wilk and D'Agostino-Pearson tests on order profit, sales, and shipping delay distributions.
2. **Hypothesis Testing**:
   - **T-Test**: Difference in profit between late orders vs on-time orders.
   - **ANOVA**: Profit variations across shipping modes (`Standard Class`, `First Class`, `Second Class`, `Same Day`).
   - **Chi-Square Test**: Independence between `Market` / `Customer Segment` and `Order Status` (e.g. `SUSPECTED_FRAUD`).
3. **Correlation Analysis**: Pearson & Spearman rank correlations across numerical operational variables.
4. **Regression Diagnostics**: OLS regression of order profit on discount, price, shipping delay, and quantity, evaluating $R^2$, collinearity (VIF), and residual distributions.

## 3. Advanced Analytical Techniques
1. **Pareto Analysis & ABC Classification**: Categorize products into Class A (Top 80% revenue), Class B (Next 15%), Class C (Bottom 5%).
2. **RFM Segmentation & Customer Clustering**: Calculate Recency, Frequency, Monetary metrics; standard scaling + K-Means clustering (elbow method & silhouette score).
3. **Time-Series Analysis & Forecasting**: Aggregate daily sales; seasonal decomposition (trend, seasonal, residual); Holt-Winters / ARIMA / Prophet forecasting for next 30 days.
