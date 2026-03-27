import zipfile
import os
import xml.etree.ElementTree as ET

class PbixFieldAnalyzer:
    def __init__(self, pbix_file):
        self.pbix_file = pbix_file
        self.fields = []
        self.measures = []
        self.dimensions = []

    def extract_fields(self):
        with zipfile.ZipFile(self.pbix_file, 'r') as zip_ref:
            zip_ref.extractall('temp_pbix')
            for root, dirs, files in os.walk('temp_pbix'):
                for file in files:
                    if file.endswith('.xml'):
                        self._parse_xml(os.path.join(root, file))

    def _parse_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Extract fields, measures, dimensions from the XML
        for elem in root.iter('Field'):
            self.fields.append(elem.text)
        for elem in root.iter('Measure'):
            self.measures.append(elem.text)
        for elem in root.iter('Dimension'):
            self.dimensions.append(elem.text)

    def analyze(self):
        self.extract_fields()
        return {
            'fields': self.fields,
            'measures': self.measures,
            'dimensions': self.dimensions
        }

# Example usage:
# analyzer = PbixFieldAnalyzer('path/to/your/file.pbix')
# analysis_result = analyzer.analyze()  # Returns a dictionary with fields, measures, and dimensions
