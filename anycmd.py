import IPython.core.magic as ipym
import argparse
import tempfile
import os
import subprocess

def defArgparse():
  p = argparse.ArgumentParser(description = "AnyCmd arguments")
  p.add_argument("-d", "--dir", action = "store", type = str, help = "Working directory") # Working dir.
  # AnyCmd uses a temporary by default. Use "-d/--dir ." to prevent this.
  
  # To explicitly separate arguments from magic from those of your command, use "--"
  p.add_argument("rest", nargs = argparse.REMAINDER)
  return p

@ipym.magics_class
class AnyCmd(ipym.Magics):
  def __init__(self, shell):
    super(AnyCmd, self).__init__(shell)
    self.argparser = defArgparse()

  # Makes a temporary file with the cell's contents, and replaces anything starting
  # in "%FILE" with the temporary file's path. Includes text after the parameter as an extension
  # (ex: "%FILE.cpp" = /some/path/CELL_CONTENTS.cpp"). Returns these updated arguments.
  def parseFileMagics(self, tmpDir, args, cell):
    resArgs = args
    for i in range(len(args)):
      arg = args[i]
      if arg.startswith('%FILE'):
        ext = arg[5:] # Extension (ex: %FILE.cpp)
        fPath = tmpDir + "/" + "CELL_CONTENTS" + ext
        if not os.path.isfile(fPath):
          with open(tmpDir + "/" + "CELL_CONTENTS" + ext, "w") as f:
            f.write(cell)
        resArgs[i] = fPath # Replace %FILE argument with new file path
    return resArgs
        
    
  @ipym.cell_magic
  def any(self, line, cell):
    args = self.argparser.parse_args(line.split())
    output = None
    currentDir = os.getcwd() # Save current working directory
    with tempfile.TemporaryDirectory() as tmpDir:
      if args.dir:
        os.chdir(args.dir)
      else:
        os.chdir(tmpDir)
      cmdArgs = self.parseFileMagics(tmpDir, args.rest, cell)
      try:
        output = subprocess.check_output(' '.join(cmdArgs), shell = True, stderr=subprocess.STDOUT).decode('utf8')
      except subprocess.CalledProcessError as e:
        print(e.output.decode('utf8'))
        print(e)
    os.chdir(currentDir) # Restore current working directory
    return output
      
def load_ipython_extension(ip):
  any_magic = AnyCmd(ip)
  ip.register_magics(any_magic)
