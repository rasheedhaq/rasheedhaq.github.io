import importlib.util
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('sync_cv', Path(__file__).with_name('sync_cv.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class Retention(unittest.TestCase):
    def test_published_source_hash_uses_lf(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            module.ROOT = root
            source = root/'Rasheed_Abdul_Haq_Resume_12OCT2026.tex'
            original = b'First\r\nSecond\nThird\r\n'
            source.write_bytes(original)
            pdf = source.with_suffix('.pdf')
            pdf.write_bytes(b'%PDF-1.4\nexample')
            module.sync(source, pdf, update_pages=False)
            metadata = json.loads((root/'cv/versions.json').read_text())['latest']
            published = (root/'cv/latest/resume.tex').read_bytes()
            self.assertEqual(published, b'First\nSecond\nThird\n')
            self.assertEqual(metadata['source_sha256'], hashlib.sha256(published).hexdigest())
            self.assertEqual(metadata['import_source_sha256'], hashlib.sha256(original).hexdigest())
            self.assertEqual(source.read_bytes(), original)

    def test_rotation_and_same_date_update(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            module.ROOT = root
            (root/'cv').mkdir()
            def sync(date, text):
                source = root/f'Rasheed_Abdul_Haq_Resume_{date}.tex'
                source.write_text(text)
                source.with_suffix('.pdf').write_bytes(b'%PDF-1.4\n' + text.encode())
                module.sync(source, source.with_suffix('.pdf'), update_pages=False)
            sync('04AUG2026', 'August')
            sync('12OCT2026', 'October')
            self.assertEqual((root/'cv/previous/resume.tex').read_text(), 'August')
            sync('12OCT2026', 'October revised')
            self.assertEqual((root/'cv/previous/resume.tex').read_text(), 'August')
            sync('12NOV2026', 'November')
            self.assertEqual((root/'cv/previous/resume.tex').read_text(), 'October revised')
            self.assertEqual((root/'cv/latest/resume.tex').read_text(), 'November')
            self.assertEqual(len(list((root/'cv').glob('*/resume.tex'))), 2)
            with self.assertRaises(ValueError):
                sync('04AUG2026', 'Old')
            metadata = json.loads((root/'cv/versions.json').read_text())
            self.assertEqual(metadata['latest']['date'], '2026-11-12')
            self.assertEqual(metadata['previous']['date'], '2026-10-12')

if __name__ == '__main__':
    unittest.main()
