import csv
from collections import defaultdict, Counter

# Read supplier data
with open(r'B:\Project\Data Science\project\dynamic_supply_chain_logistics_dataset_with_country.csv') as f:
    reader = csv.DictReader(f)
    supplier_data = list(reader)

# Create supplier summary
supplier_summary = defaultdict(lambda: {
    'product_id': '', 'supplier_id': '', 'supplier_country': '',
    'lead_time_days': [], 'supplier_reliability_score': [], 
    'disruption_likelihood_score': [], 'delay_probability': [],
    'delivery_time_deviation': [], 'shipping_costs': [],
    'risk_classification': []
})

for row in supplier_data:
    key = (row['product_id'], row['supplier_id'])
    supplier_summary[key]['product_id'] = row['product_id']
    supplier_summary[key]['supplier_id'] = row['supplier_id']
    supplier_summary[key]['supplier_country'] = row['supplier_country']
    try:
        supplier_summary[key]['lead_time_days'].append(float(row['lead_time_days']))
        supplier_summary[key]['supplier_reliability_score'].append(float(row['supplier_reliability_score']))
        supplier_summary[key]['disruption_likelihood_score'].append(float(row['disruption_likelihood_score']))
        supplier_summary[key]['delay_probability'].append(float(row['delay_probability']))
        supplier_summary[key]['delivery_time_deviation'].append(float(row['delivery_time_deviation']))
        supplier_summary[key]['shipping_costs'].append(float(row['shipping_costs']))
        supplier_summary[key]['risk_classification'].append(row['risk_classification'])
    except Exception as e:
        pass

with open(r'B:\Project\Data Science\project\Supplier_Performance_Summary.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['product_id', 'supplier_id', 'supplier_country', 'avg_lead_time_days', 
                'avg_supplier_reliability', 'avg_disruption_likelihood', 'avg_delay_probability',
                'avg_delivery_time_deviation', 'avg_shipping_costs', 'risk_classification', 'record_count'])
    for k, v in supplier_summary.items():
        if v['lead_time_days']:
            risk = Counter(v['risk_classification']).most_common(1)[0][0]
            w.writerow([
                v['product_id'], v['supplier_id'], v['supplier_country'],
                sum(v['lead_time_days'])/len(v['lead_time_days']),
                sum(v['supplier_reliability_score'])/len(v['supplier_reliability_score']),
                sum(v['disruption_likelihood_score'])/len(v['disruption_likelihood_score']),
                sum(v['delay_probability'])/len(v['delay_probability']),
                sum(v['delivery_time_deviation'])/len(v['delivery_time_deviation']),
                sum(v['shipping_costs'])/len(v['shipping_costs']),
                risk,
                len(v['lead_time_days'])
            ])

print('Done')
