import pandas as pd

# Assuming the data is provided in a format like this
fields_data = [
    {'table': 'Table1', 'field': 'FieldA', 'type': 'Attribute'},
    {'table': 'Table1', 'field': 'FieldB', 'type': 'Measure'},
    {'table': 'Table2', 'field': 'FieldC', 'type': 'Attribute'},
    {'table': 'Table1', 'field': 'FieldA', 'type': 'Attribute'},  # Duplicate
]

# Create a DataFrame
fields_df = pd.DataFrame(fields_data)

# Remove duplicates
fields_df = fields_df.drop_duplicates()

# Group by table and sort fields alphabetically
used_fields = fields_df.groupby('table').apply(lambda x: x.sort_values('field')).reset_index(drop=True)

# Display the results
for table, group in used_fields.groupby('table'):
    print(f'Table: {table}')
    for _, row in group.iterrows():
        print(f'  Field: {row.field}, Type: {row.type}')