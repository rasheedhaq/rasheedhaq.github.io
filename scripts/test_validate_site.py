import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('validator', Path(__file__).parents[1] / 'research/validate_site.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SiteValidation(unittest.TestCase):
    def test_directory_and_fragment_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'lab').mkdir()
            (root / 'index.html').write_text('<a href="/lab/#study">Read</a>')
            (root / 'lab/index.html').write_text('<h1 id="study">Study</h1>')
            self.assertEqual(validator.validate(root), [])
            (root / 'lab/index.html').write_text('<h1>Study</h1>')
            self.assertIn('Missing fragment', str(validator.validate(root)))

    def test_missing_and_private_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'index.html').write_text('<a href="file:///C:/private.pdf">Private</a><img src="missing.png">')
            self.assertEqual(len(validator.validate(root)), 2)

    def test_archive_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / 'lab/archive'
            archive.mkdir(parents=True)
            (archive / 'draft.tex').write_text('draft')
            self.assertIn('three HTML/PDF', str(validator.validate(root)))


if __name__ == '__main__':
    unittest.main()
