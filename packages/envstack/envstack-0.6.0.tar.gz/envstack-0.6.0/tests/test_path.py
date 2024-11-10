import unittest
from envstack.path import Template, Path

class TestPath(unittest.TestCase):
    def test_template_apply_fields(self):
        t = Template('/projects/{show}/{sequence}/{shot}/{task}')
        p = t.apply_fields(show='bunny', sequence='abc', shot='010', task='comp')
        self.assertEqual(str(p), '/projects/bunny/abc/010/comp')

    def test_template_get_fields(self):
        t = Template('/projects/{show}/{sequence}/{shot}/{task}')
        fields = t.get_fields('/projects/bunny/abc/010/comp')
        self.assertEqual(fields, {'show': 'bunny', 'sequence': 'abc', 'shot': '010', 'task': 'comp'})

    def test_path_toPlatform(self):
        p = Path('/projects/bunny/abc/010/comp')
        converted_path = p.toPlatform('windows')
        self.assertEqual(converted_path, '//projects/bunny/abc/010/comp')

    def test_path_basename(self):
        p = Path('/projects/bunny/abc/010/comp')
        basename = p.basename()
        self.assertEqual(basename, 'comp')

    def test_path_dirname(self):
        p = Path('/projects/bunny/abc/010/comp')
        dirname = p.dirname()
        self.assertEqual(dirname, '/projects/bunny/abc/010')

    def test_path_levels(self):
        p = Path('/projects/bunny/abc/010/comp')
        levels = p.levels()
        self.assertEqual(levels, ['projects', 'bunny', 'abc', '010', 'comp'])

if __name__ == '__main__':
    unittest.main()