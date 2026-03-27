import zipfile
import json
import csv
import os
from collections import defaultdict

class PBIXAnalyzer:
    def __init__(self, pbix_file):
        self.pbix_file = pbix_file
        self.fields = defaultdict(set)

    def extract_zip(self):
        with zipfile.ZipFile(self.pbix_file, 'r') as z:
            z.extractall(os.path.dirname(self.pbix_file))

    def read_json_files(self):
        extracted_dir = os.path.splitext(self.pbix_file)[0]
        data_model_path = os.path.join(extracted_dir, 'DataModel.json')
        report_layout_path = os.path.join(extracted_dir, 'ReportLayout.json')

        with open(data_model_path, 'r') as f:
            data_model = json.load(f)
        with open(report_layout_path, 'r') as f:
            report_layout = json.load(f)

        self.extract_fields(data_model)
        self.extract_fields(report_layout)

    def extract_fields(self, json_data):
        def parse_table(table):
            for column in table.get('columns', []):
                self.fields[table['name']].add(column['name'])

        for table in json_data.get('tables', []):
            parse_table(table)

    def export_to_csv(self, output_file):
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Table', 'Field'])  # Header
            for table, columns in self.fields.items():
                for field in columns:
                    writer.writerow([table, field])

    def analyze(self):
        self.extract_zip()
        self.read_json_files()
        output_file = os.path.splitext(self.pbix_file)[0] + '_fields.csv'
        self.export_to_csv(output_file)
        return output_file

if __name__ == '__main__':
    pbix_file_path = 'path_to_your_pbix_file.pbix'  # Replace with actual path
    analyzer = PBIXAnalyzer(pbix_file_path)
    output_file = analyzer.analyze()
    print(f'Fields exported to {output_file}')
