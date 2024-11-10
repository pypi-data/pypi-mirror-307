#!/usr/bin/env python

__doc__ = """
Viro unit tests.
"""

import os
import sys
import tempfile
import unittest

cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, cwd)
import envstack

from envstack.logger import setup_stream_handler
setup_stream_handler()


# sample env data
env_data_1 = """
all: &default
  FOO: bar
  BAR: $FOO
  BAZ: $BAR
  QUX: $BAR$BAR
  QUUX: $BAZ-1
  LIST: ['a', 'b', 'c']
  MAP: {'a': 1, 'b': 2}
  NUM: 12
  PI: 3.14
linux:
  <<: *default
  CMD: env
windows:
  <<: *default
  CMD: SET
"""

# contains reference to external var
env_data_2 = """
all: &default
  GRAULT: $FOO
"""

# contains circular reference to external source
env_data_3 = """
all: &default
  FOO: $BAR
"""

# appends to PATH
env_data_4 = """
all: &default
  PATH: $PATH:/path/to/tool
windows:
  <<: *default
  PATH: $PATH;/path/to/tool
"""

# nested data with platform specific overrides
env_data_5 = """
all: &default
  FRUIT: &fruit
    apple:
      color: red
    banana:
      color: yellow
    melon:
      color: green
linux:
  <<: *default
  FRUIT:
    <<: *fruit
    dragon:
      color: pink
windows:
  <<: *default
  FRUIT:
    <<: *fruit
    dragon:
      color: purple
"""

# bad source env file
env_data_6 = """
all: &default
FOO:bar,
"""

# template env
env_data_7 = """
all: &default
  ROOT: /fake/path
  PATH1: $ROOT/{show}
  PATH2: $PATH1/{seq}
  PATH3: $PATH2/{shot}
linux:
  <<: *default
windows:
  <<: *default
"""

# template env with ambiguous templates
env_data_8 = """
all: &default
  ROOT: /fake/path
  PATH1: $ROOT/{show}/{seq}/{shot}
  PATH2: $ROOT/{galaxy}/{system}/{planet}
linux:
  <<: *default
windows:
  <<: *default
"""


def create_viro_file(data, namespace=None, scope=None):
    """Writes viro env data to a valid viro .env file.

    :data: data to write to viro file
    :namespace: the env namespace
    :returns filepath, namespace, scope as tuple
    """

    if scope is None:
        scope = tempfile.gettempdir()

    viro_dir = os.path.join(scope, "test")

    if not os.path.isdir(viro_dir):
        os.makedirs(viro_dir)

    if namespace:
        filename = os.path.join(viro_dir, '{}.env'.format(namespace))
        f = open(filename, 'w+')
    else:
        f = tempfile.NamedTemporaryFile(mode='w+', delete=False, dir=viro_dir, 
                suffix='.env')

    f.write(data)
    f.close()

    namespace = os.path.splitext(os.path.basename(f.name))[0]
    return f.name, namespace, scope


class TestBasic(unittest.TestCase):

    def test_env_expansion(self):
        # test progressive levels of expansion
        env = envstack.Env()

        # set an initial key/value
        env.update(foo='bar')
        self.assertEqual(env['foo'], 'bar')

        # create a new var that references the original
        env.update(bar='$foo')
        self.assertEqual(env['bar'], 'bar')

        # nested reference to original variable
        env.update(baz='${bar}')
        self.assertEqual(env['baz'], 'bar')

        # now change the original to something else, and 
        # the others should also update
        env.update(foo='foo')
        self.assertEqual(env['foo'], 'foo')
        self.assertEqual(env['bar'], 'foo')
        self.assertEqual(env['baz'], 'foo')

        # check the raw values
        self.assertEqual(env.get_raw('foo'), 'foo')
        self.assertEqual(env.get_raw('bar'), '$foo')
        self.assertEqual(env.get_raw('baz'), '${bar}')

        # set some sed vars
        env = envstack.Env({
            'BAR': '$FOO',
            'BAZ': '$BAR'
        })

        # $FOO is not yet defined
        self.assertEqual(env['BAR'], '$FOO')
        self.assertEqual(env.get('BAR'), '$FOO')
        self.assertEqual(env.get('BAR', resolved=False), '$FOO')

        # set $FOO, check one of the other vars set to $FOO and make sure it
        # gets resolved
        env.update({'FOO': 'bar'})
        self.assertEqual(env['BAR'], 'bar')
        self.assertEqual(env['BAZ'], 'bar')
        self.assertEqual(env.get('BAZ'), 'bar')
        self.assertEqual(env.get('BAZ', resolved=False), '$BAR')

    def test_load_file(self):
        """Tests the load_file function."""
        f1, _, _ = create_viro_file(env_data_1)
        d = envstack.load_file(f1)

        for p in ['all', 'linux', 'windows']:
            self.assertEqual(d[p]['FOO'], 'bar')
            self.assertEqual(d[p]['BAR'], '$FOO')
            self.assertEqual(d[p]['BAZ'], '$BAR')
            self.assertEqual(d[p]['QUX'], '$BAR$BAR')
            self.assertEqual(d[p]['NUM'], 12)

        def load_invalid():
            f2, _, _ = create_viro_file(env_data_6)
            d = envstack.load_file(f2)

        self.assertRaises(envstack.exceptions.InvalidSource, load_invalid)

    def test_load_source(self):
        """Tests Source class loading."""
        f1, _, _ = create_viro_file(env_data_1)
        f3, _, _ = create_viro_file(env_data_2)

        s1 = envstack.env.Source(f1)
        s2 = envstack.env.Source(f1)
        s3 = envstack.env.Source(f3)

        self.assertTrue(s1.exists())
        self.assertTrue(s2.exists())
        self.assertTrue(s3.exists())

        d1 = s1.load()
        d2 = s2.load()
        d3 = s3.load()

        self.assertEqual(d1['FOO'], 'bar')
        self.assertEqual(d1['BAR'], '$FOO')
        self.assertEqual(d1['BAZ'], '$BAR')
        self.assertEqual(d1['QUX'], '$BAR$BAR')
        self.assertEqual(d1['NUM'], 12)
        self.assertEqual(s1.includes(), [])
        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertEqual(d1, d2)
        self.assertNotEqual(d1, d3)

    def test_env(self):
        """Tests the Env class."""
        f1, _, _ = create_viro_file(env_data_1)
        env1 = envstack.env.load_environ(sources=[envstack.env.Source(f1)])

        # make sure all vars get resolved
        self.assertEqual(env1['FOO'], 'bar')
        self.assertEqual(env1['BAR'], 'bar')
        self.assertEqual(env1['BAZ'], 'bar')
        self.assertEqual(env1['QUX'], 'barbar')
        self.assertEqual(env1['QUUX'], 'bar-1')
        self.assertEqual(env1['LIST'], ['a', 'b', 'c'])
        self.assertEqual(env1['MAP'], {'a': 1, 'b': 2})
        self.assertEqual(env1['NUM'], 12)
        self.assertEqual(env1['PI'], 3.14)
        self.assertRaises(KeyError, lambda: env1['CORGE'])

        f2, _, _ = create_viro_file(env_data_2)
        env2 = envstack.env.load_environ(sources=[envstack.env.Source(f2)])

        # test inheritance var resolution (vars with vals defined in other files)
        env1.merge(env2)
        self.assertEqual(env1['GRAULT'], 'bar')

        # bake down the env files into a single env file
        from envstack.env import _bake_environ
        f3 = tempfile.NamedTemporaryFile(delete=False, suffix='.env')
        _bake_environ(env1, f3.name)
        f3.close()

        # load environ from baked file
        env3 = envstack.env.load_environ(sources=[envstack.env.Source(f3.name)])

        # load the baked env file and retest all values
        self.assertEqual(env3['FOO'], 'bar')
        self.assertEqual(env3['BAR'], 'bar')
        self.assertEqual(env3['BAZ'], 'bar')
        self.assertEqual(env3['QUX'], 'barbar')
        self.assertEqual(env3['QUUX'], 'bar-1')
        self.assertEqual(env3['GRAULT'], 'bar')
        self.assertRaises(KeyError, lambda: env3['CORGE'])

    def test_bake_environ(self):
        """Tests baking an environment."""
        from envstack.env import bake_environ, load_environ, Source
        f1, n1, s1 = create_viro_file(env_data_1)
        e1 = load_environ(n1, scope=s1)
        outfile = os.path.join(s1, 'baked.env')

        # bake the environment to an out file
        baked = bake_environ(n1, outfile, scope=s1)
        self.assertTrue(os.path.exists(outfile))

        # load baked environment
        env = envstack.Env()
        src = Source(outfile)

        env.update(src.load())
        self.assertEqual(env['FOO'], 'bar')
        self.assertEqual(env['BAZ'], 'bar')
        self.assertEqual(env['QUX'], 'barbar')

    def test_trace_var(self):
        """Tests tracing a variable."""
        from envstack.env import trace_var
        os.environ['FOOBAR'] = 'barbarbar'
        path = trace_var('default', 'FOOBAR')
        self.assertTrue('local' in path)
        path = trace_var('default', 'BARFOO')
        self.assertEqual(path, None)

    def test_self_reference(self):
        # self references should remain intact in case they get
        # defined later in subprocesses, other env files or in the shell 
        env = envstack.Env({
            'FOO': '$FOO'
        })
        self.assertEqual(env.get('FOO'), '$FOO')

        env = envstack.Env({
            'FOO': '$FOO:bar'
        })
        self.assertEqual(env.get('FOO'), '$FOO:bar')

    def test_circular_references(self):
        from envstack.env import Source, load_environ
        env = envstack.Env({
            'BAR': '$FOO',
            'FOO': '$BAR'
        })
        self.assertEqual(env.get('FOO'), '$FOO')
        self.assertEqual(env.get('BAR'), '$BAR')

        # circular reference two levels deep
        env = envstack.Env({
            'BAR': '$BAZ',
            'FOO': '$BAR',
            'BAZ': '$FOO'
        })
        self.assertEqual(env.get('FOO'), '$BAZ')
        self.assertEqual(env.get('BAR'), '$FOO')
        self.assertEqual(env.get('BAZ'), '$BAR')

        f1, _, _ = create_viro_file(env_data_1)
        f3, _, _ = create_viro_file(env_data_3)

        env = load_environ(sources=[Source(f1)])
        env3 = load_environ(sources=[Source(f3)])
        env.merge(env3)

        self.assertEqual(env['FOO'], '$FOO')
        self.assertEqual(env['BAR'], '$BAR')

    def test_nested_data(self):
        from envstack.env import load_file, load_environ

        # create nested data viro file
        filepath, namespace, scope = create_viro_file(env_data_5)

        # test load_file
        s1 = viro.Source(filepath)
        env = viro.load_environ(sources=[s1])

        self.assertEqual(env['FRUIT']['apple']['color'], 'red')
        self.assertEqual(env['FRUIT']['banana']['color'], 'yellow')
        self.assertEqual(env['FRUIT']['melon']['color'], 'green')
        self.assertEqual(env['FRUIT']['dragon']['color'], {
            'linux': 'pink', 'windows': 'purple'
        }.get(viro.PLATFORM))

        # test load_environ
        env = load_environ(namespace, scope=scope)
        self.assertEqual(env['FRUIT']['apple']['color'], 'red')
        self.assertEqual(env['FRUIT']['banana']['color'], 'yellow')
        self.assertEqual(env['FRUIT']['melon']['color'], 'green')
        self.assertEqual(env['FRUIT']['dragon']['color'], {
            'linux': 'pink', 'windows': 'purple'
        }.get(viro.PLATFORM))

    def test_local_override(self):
        from viro import load_environ

        # make sure local var is present in env
        os.environ['FOO'] = 'foo'
        env = viro.load_environ(environ=os.environ)
        self.assertEqual(env.get('FOO'), 'foo')

        _, namespace, scope = create_viro_file(env_data_1)

        local_env = load_environ(environ=os.environ)
        test_env = load_environ(namespace, scope=scope)
        merged_env = load_environ(namespace, environ=os.environ, scope=scope)

        self.assertEqual(local_env.get('FOO'), 'foo')
        self.assertEqual(test_env.get('FOO'), 'bar')

        # merged environ should get value from local env
        self.assertEqual(merged_env.get('FOO'), 'foo')

    def test_path(self):
        from viro.wrapper import encode

        # test appending to $PATH
        filepath, namespace, scope = create_viro_file(env_data_4)

        # path we want to add
        tool_path = '/path/to/tool'

        # exclusion test for os.environ
        os_env = os.environ.copy()
        os_env_path_value = os_env.get('PATH')
        self.assertTrue(tool_path not in os_env_path_value)

        # test load_file
        s1 = viro.Source(filepath)
        env = viro.load_environ(sources=[s1])
        self.assertTrue(env['PATH'].endswith(tool_path))
        self.assertTrue(encode(env)['PATH'].endswith(tool_path))
        self.assertEqual(env.get_raw('PATH'), {
            'linux': '$PATH:{}'.format(tool_path),
            'windows': '$PATH;{}'.format(tool_path)
        }.get(viro.PLATFORM))

        # test load_environ, resolve=False
        env = viro.load_environ(namespace, scope=scope)
        self.assertTrue(env['PATH'].endswith(tool_path))
        self.assertTrue(encode(env)['PATH'].endswith(tool_path))
        self.assertEqual(env.get_raw('PATH'), {
            'linux': '$PATH:{}'.format(tool_path),
            'windows': '$PATH;{}'.format(tool_path)
        }.get(viro.PLATFORM))

        # test load_environ, resolve=True
        env = viro.load_environ(namespace, scope=scope)
        self.assertTrue(env['PATH'].endswith(tool_path))
        self.assertTrue(encode(env)['PATH'].endswith(tool_path))
        self.assertEqual(env.get_raw('PATH'), {
            'linux': '$PATH:{}'.format(tool_path),
            'windows': '$PATH;{}'.format(tool_path)
        }.get(viro.PLATFORM))

    def test_env_copy(self):
        e1 = viro.Env({
            'FOO': '$BAR',
            'BAR': 'baz'
         })
        e2 = e1.copy()

        self.assertEqual(e1, e2)
        self.assertEqual(e1['FOO'], e2['FOO'])
        self.assertEqual(e1['BAR'], e2['BAR'])
        self.assertEqual(e1.get('FOO', resolved=False),
            e2.get('FOO', resolved=False))

        e2['BAR'] = 'qux'
        self.assertNotEqual(e1, e2)
        self.assertEqual(e1['FOO'], 'baz')
        self.assertEqual(e2['FOO'], 'qux')

    def test_env_export(self):
        _, namespace, scope = create_viro_file(env_data_1)
        env = viro.load_environ(namespace, scope=scope)

        bashexp = viro.export(namespace, scope=scope)
        for k, v in env.items():
            self.assertTrue('export {0}="{1}"'.format(k, v) in bashexp)

        tcshexp = viro.export(namespace, scope=scope, shell='tcsh')
        for k, v in env.items():
            self.assertTrue('setenv {0}:"{1}"'.format(k, v) in tcshexp)

        cmdexp = viro.export(namespace, scope=scope, shell='cmd')
        for k, v in env.items():
            self.assertTrue('set {0}="{1}"'.format(k, v) in cmdexp)

        pwshexp = viro.export(namespace, scope=scope, shell='pwsh')
        for k, v in env.items():
            self.assertTrue('$env:{0}="{1}"'.format(k, v) in pwshexp)

    def test_wrapper(self):
        """tests to make sure env vars get passed through to subprocess
        in wrappers"""

        env = viro.Env({
            'EXE': 'python',
            'FOO': 'bar',
            'BAR': '$FOO',
            'BAZ': '$BAR',
            'QUX': '$BAR$BAR',
            'QUUX': '$BAZ-1',
            'PATH1': '/path/with/${BAR}',
            'PATH2': '/path/with/{variable}',
            'PATH3': '$PATH2/folder',
            'NUM': 12,
            'PI': 3.14
        })
        ns = 'test_wrapper'

        # our test wrapper
        class TestWrapper(viro.Wrapper):
            def __init__(self, *args, **kwargs):
                super(TestWrapper, self).__init__(*args, **kwargs)
                self.env = env
            def executable(self):
                return "$EXE -c \
'import os,sys; assert os.environ[sys.argv[1]]==sys.argv[2],\
(sys.argv[1],os.environ[sys.argv[1]])'"

        # text for exitcode 1 with KeyError: 'MISSING'
        test = TestWrapper(ns, ['MISSING', ''])
        exitcode = test.launch()
        self.assertEqual(exitcode, 1)

        # text for exitcode 1 with AssertionError: FOO
        test = TestWrapper(ns, ['FOO', 'BADVALUE'])
        exitcode = test.launch()
        self.assertEqual(exitcode, 1)

        # test for exitcode 0
        for k, v in env.items():
            test = TestWrapper(ns, [k, viro.expandvars(v, env)])
            exitcode = test.launch()
            self.assertEqual(exitcode, 0, k)
            if k == 'PATH1':
                self.assertEqual(v, '/path/with/foo')
            if k == 'PATH2':
                self.assertEqual(v, '/path/with/{variable}')
            if k == 'PATH3':
                self.assertEqual(v, '/path/with/{variable}/folder')

    def test_envvar(self):
        """Tests the EnvVar class."""
        v1 = viro.EnvVar('$FOO:${BAR}')
        self.assertEqual(v1.template, '$FOO:${BAR}')
        self.assertEqual(len(v1.parts()), 2)
        self.assertEqual(v1.parts(), ['$FOO', '${BAR}'])
        self.assertEqual(v1.substitute(FOO='foo', BAR='bar'), 'foo:bar')

        v2 = viro.EnvVar('["a", "b"]')
        self.assertEqual(type(v2.value()), list)
        self.assertEqual(type(v2.template), str)
        self.assertEqual(v2[0], "a")
        self.assertEqual(v2[1], "b")
        v2.extend(["c", "d"])
        self.assertEqual(v2.value(), ["a", "b", "c", "d"])
        v2.append("e")
        self.assertEqual(v2.value(), ["a", "b", "c", "d", "e"])

        v3 = viro.EnvVar('{"a":1, "b":2}')
        self.assertEqual(type(v3.value()), dict)
        self.assertEqual(type(v3.template), str)
        self.assertEqual(v3["a"], 1)
        self.assertEqual(v3["b"], 2)

        v4 = viro.EnvVar({"a":1, "b":2})
        self.assertEqual(type(v4.value()), dict)
        self.assertEqual(type(v4.template), dict)
        self.assertEqual([x for x in v4.keys()], ["a", "b"])
        self.assertEqual(v4["a"], 1)
        self.assertEqual(v4["b"], 2)

        v5 = viro.EnvVar(["a", "b"])
        self.assertEqual(type(v5.value()), list)
        self.assertEqual(type(v5.template), list)
        self.assertEqual(v5[0], "a")
        self.assertEqual(v5[1], "b")
        self.assertEqual(v5.parts(), ["a", "b"])

    def test_scope(self):
        from viro import load_environ

        cwd = os.getcwd()

        _, namespace, scope = create_viro_file(env_data_1)

        default_env = load_environ()
        test_env = load_environ(namespace, scope=scope)
        cwd_env = load_environ(namespace)

        # check namespace values for each env
        self.assertEqual(default_env.namespace, 'default')
        self.assertEqual(test_env.namespace, namespace)
        self.assertEqual(cwd_env.namespace, namespace)

        # check scope values for each env
        self.assertEqual(default_env.scope, cwd)
        self.assertEqual(test_env.scope, scope)
        self.assertEqual(cwd_env.scope, cwd)

        # check resolved vars, cwd should be same as default
        self.assertEqual(cwd_env.keys(), default_env.keys())
        self.assertNotEqual(cwd_env.keys(), test_env.keys())

    def test_includes(self):
        """Tests namespace includes."""
        hello_env = viro.load_environ('hello')
        blender_env = viro.load_environ('blender')

        # the hello.env test file includes blender, but
        # overrides BLENDER_VERSION 
        self.assertEqual(blender_env['BLENDER_VERSION'], '2.79b')
        self.assertEqual(hello_env['BLENDER_VERSION'], '4.1a')

        # test BLENDER_ROOT from blender namespace
        dirname, filename = os.path.split(blender_env['BLENDER_ROOT'])
        self.assertEqual(filename, 'blender-2.79b-linux-glibc219-x86_64')

        # test BLENDER_ROOT from hello namespace, which is only
        # defined in the blender.env file
        dirname, filename = os.path.split(hello_env['BLENDER_ROOT'])
        self.assertEqual(filename, 'blender-4.1a-linux-glibc219-x86_64')

        # create two new env files, one includes the other
        f3, n3, s3 = create_viro_file("all: &default\n  FOO: bar\n")
        d4 = "include: ['{}']\nall: &default\n  BAR: $FOO\n".format(n3)
        f4, n4, s4 = create_viro_file(d4, scope=s3)
        self.assertEqual(s3, s4)

        # load env and test to make sure included values resolve
        env = viro.load_environ(n4, scope=s4)
        self.assertEqual(env['FOO'], 'bar')
        self.assertEqual(env['BAR'], 'bar')

if __name__ == '__main__':
    unittest.main()
