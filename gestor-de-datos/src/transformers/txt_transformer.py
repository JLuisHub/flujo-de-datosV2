from src.extractors.txt_extractor import TXTExtractor
from os.path import join
import luigi, os, json

class TXTTransformer(luigi.Task):

    def requires(self):
        return TXTExtractor()

    def run(self):
        result = []
        for file in self.input():
            with file.open() as txt_file:
                headers_str = txt_file.readline()
                content_str = txt_file.readline()

                records = content_str.split(';')
                records.pop()

                for record in records:
                    datos = record.split(',')
                    numero, codigo, desc, montante, fecha,precio, id, pais = datos
                    result.append({
                        "description": desc,
                        "quantity": montante,
                        "price": precio,
                        "total": float(precio) * float(montante),
                        "invoice": numero,
                        "provider": id,
                        "country": pais
                    })
        with self.output().open('w') as out:
            out.write(json.dumps(result, indent=4))

    def output(self):
        project_dir = os.path.dirname(os.path.abspath("loader.py"))
        result_dir = join(project_dir, "result")
        return luigi.LocalTarget(join(result_dir, "txt.json"))
  