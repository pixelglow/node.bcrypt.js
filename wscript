# -*- mode: python -*-

import Options, Utils, sys
from os import unlink, symlink, popen
from os.path import exists, islink

srcdir = "."
blddir = "build"
VERSION = "0.0.1"

def set_options(opt):
  opt.tool_options("compiler_cxx")
  opt.tool_options("compiler_cc")

def configure(conf):
  conf.check_tool("compiler_cxx")
  conf.check_tool("compiler_cc")
  conf.check_tool("node_addon")
  o = Options.options

  libpath = ['/lib', '/usr/lib', '/usr/local/lib', '/opt/local/lib', '/usr/sfw/lib']
  includes = ['/usr/include', '/usr/includes', '/usr/local/includes', '/opt/local/includes', '/usr/sfw/lib'];

  libssl = conf.check(lib="ssl",
          header_name='openssl/rand.h',
          function_name='RAND_bytes',
          includes=includes,
          libpath=libpath,
          uselib_store='OPENSSL')

  if sys.platform == "cygwin":
    libcrypto = conf.check(lib="crypto",
            includes=includes,
            libpath=libpath,
            uselib_store='CRYPTO')
    libz = conf.check(lib="z",
            includes=includes,
            libpath=libpath,
            uselib_store='Z')
  
def build(bld):
  bcryptnode = bld.new_task_gen("cxx", "shlib", "node_addon")
  bcryptnode.target = "bcrypt_lib"
  bcryptnode.source = """
    src/blowfish.cc
    src/bcrypt.cc
    src/bcrypt_node.cc
  """
  uselib = "OPENSSL"
  if sys.platform == "cygwin":
    uselib += " CRYPTO Z"
  bcryptnode.uselib = uselib

def test(t):
  Utils.exec_command('nodeunit test')

def shutdown():
  t = 'bcrypt_lib.node'
  if Options.commands['clean']:
    if exists(t): unlink(t)
  if Options.commands['build']:
    if exists('build/default/' + t) and not exists(t):
      symlink('build/default/' + t, t)
