# Supply Chain Disruption Monitoring and Lead Time Estimation - Power BI Dashboard

## Overview
This interactive Power BI dashboard provides comprehensive monitoring of supply chain disruptions and lead time estimation using your logistics dataset.

## Data Sources
- `dynamic_supply_chain_logistics_dataset_with_country.csv` - Primary supplier/product data with risk metrics
- `dynamic_supply_chain_logistics_dataset.csv` - Operational data with GPS, weather, traffic
- `Supplier_Performance_Summary.csv` - Aggregated supplier performance metrics (created)

## Dashboard Pages

### 1. Executive Overview
**Purpose:** High-level KPIs and risk summary
- **KPI Cards:** Total Suppliers, Avg Lead Time, High Risk %, Avg Disruption Likelihood
- **Risk Classification Donut Chart:** Distribution of Low/Moderate/High Risk
- **Disruption Likelihood Trend:** By product/supplier
- **Top 10 High-Risk Suppliers:** Bar chart sorted by risk

### 2. Disruption Monitoring
**Purpose:** Real-time disruption tracking
- **Disruption Likelihood Gauge:** Overall risk score
- **Route Risk Analysis:** Route risk levels
- **Weather Impact:** Weather severity vs disruptions
- **Customs & Port Analysis:** Clearance times and congestion
- **Cargo Condition:** Status monitoring

### 3. Lead Time Estimation
**Purpose:** Lead time analysis and prediction insights
- **Avg Lead Time by Country:** Geographic analysis
- **Lead Time vs Supplier Reliability:** Scatter plot with trendline
- **Historical Demand Impact:** Correlation analysis
- **Delivery Time Deviation:** Actual vs expected
- **Shipping Costs Analysis:** Cost vs lead time

### 4. Supplier Performance
**Purpose:** Detailed supplier scorecarding
- **Supplier Scorecard Table:** All key metrics with conditional formatting
- **Country Performance Map:** Filled map by supplier country
- **Product-wise Analysis:** Lead times by product
- **Reliability vs Disruption:** Matrix visualization
- **Performance Ranking:** Top/bottom performers

## Key Measures (DAX)

```dax
Avg Lead Time = AVERAGE('Supplier_Performance_Summary'[avg_lead_time_days])

High Risk Count = CALCULATE(COUNTROWS('Supplier_Performance_Summary'), 'Supplier_Performance_Summary'[risk_classification]="High Risk")

High Risk % = DIVIDE([High Risk Count], COUNTROWS('Supplier_Performance_Summary'), 0)

Avg Disruption Score = AVERAGE('Supplier_Performance_Summary'[avg_disruption_likelihood])

Avg Reliability = AVERAGE('Supplier_Performance_Summary'[avg_supplier_reliability])

On-Time Risk = AVERAGE('Supplier_Performance_Summary'[avg_delivery_time_deviation])
```

## How to Create in Power BI Desktop

1. **Open Power BI Desktop**
2. **Get Data > Text/CSV**
   - Import `dynamic_supply_chain_logistics_dataset_with_country.csv`
   - Import `Supplier_Performance_Summary.csv`
3. **Data Modeling**
   - Create relationships between tables if needed (by product_id, supplier_id)
4. **Create Measures** - Add the DAX measures above
5. **Build Visuals** - Follow the page layouts described
6. **Add Interactivity**
   - Add slicers for: supplier_country, product_id, risk_classification
   - Enable cross-filtering between visuals
   - Add drillthrough pages if desired
7. **Format & Style** - Use red/yellow/green for risk indicators

## Quick Insights from Your Data
- 113,097 records across suppliers/products/countries
- 3,524 unique supplier-product combinations
- Multiple risk classifications (High Risk, Moderate Risk)
- Global supplier base across many countries

## Files in This Folder
- `dynamic_supply_chain_logistics_dataset_with_country.csv` - Main dataset
- `dynamic_supply_chain_logistics_dataset.csv` - Operational dataset  
- `Supplier_Performance_Summary.csv` - Aggregated supplier metrics
- `Dashboard_Config.json` - Dashboard configuration
- `README_DASHBOARD.md` - This documentation
- `process_data.py` - Data processing script
- `check.py` - Data inspection script

## Tips
- Use conditional formatting on risk columns (Red for High Risk)
- Add tooltips for detailed supplier information
- Consider using bookmarks for different views
- The filled map works great for country-level analysis
