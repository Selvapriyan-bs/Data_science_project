import csv
f = open(r'B:\Project\Data Science\project\dynamic_supply_chain_logistics_dataset_with_country.csv')
r = csv.DictReader(f)
print(r.fieldnames)
rows = list(r)
print(len(rows))
f.close()
