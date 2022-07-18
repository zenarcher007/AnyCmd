import IPython.core.magic as ipym
import argparse
import tempfile
import os
import subprocess
import uuid
import contextlib

def defArgparse():
  p = argparse.ArgumentParser(description = "Allows any command to be run as a cell magic.", prog = "AnyCmd", formatter_class = argparse.RawDescriptionHelpFormatter,
      epilog = "Any argument starting with the literal string \"%FILE\" or \"%FILE.someExtension\" will be replaced with a path to a file with the cell contents.")
  # AnyCmd uses a temporary working directory by default. Use "-d/--dir <directory>" to override this.
  p.add_argument("-d", "--dir", action = "store", type = str, help = "Change into <directory> before running the cell command. Does not change temp file location (unless --inplace is specified).") # Working dir.
  p.add_argument("-p", "--print", action = "store_true", default = False, help = "Print command output instead of outputting it to a jupyter cell. This may improve readability of the output.")
  p.add_argument("-i", "--inplace", action = "store_true", default = False, help = "Write temporary cell contents files in the current working directory (see --dir), instead of a temporary directory. Has no effect unless --dir is specified.)
  
  # To explicitly separate arguments for the magic from those of your command, use "--"
  p.add_argument("rest", nargs = argparse.REMAINDER)
  return p

@ipym.magics_class
class AnyCmd(ipym.Magics):
  def __init__(self, shell):
    super(AnyCmd, self).__init__(shell)
    self.argparser = defArgparse()

  def run(self, cmdArgs):
    output = None
    try:
      output = subprocess.check_output(' '.join(cmdArgs), shell = True, stderr=subprocess.STDOUT).decode('utf8')
    except subprocess.CalledProcessError as e:
      print(e.output.decode('utf8'))
      print(e)
    return output

  # Makes a temporary file with the cell's contents, and replaces anything starting
  # in "%FILE" with the temporary file's path. Includes text after the parameter as an extension
  # (ex: "%FILE.cpp" = /some/path/CELL_CONTENTS.cpp"). Returns these updated arguments, along with
  # a list of the paths of all temporary files used (for later cleanup).
  def parseFileMagics(self, tmpDir, args, cell):
    resArgs = args
    tempFiles = [] # To return a list of the temporary files generated
    randId = uuid.uuid4() # Names of the temp files from this function call
    for i in range(len(args)):
      arg = args[i]
      if arg.startswith('%FILE'):
        ext = arg[5:] # Extension (ex: %FILE.cpp)
        fPath = tmpDir + "/" + str(randId) + ext # Temp files with the same extension will not be recreated.
        tempFiles.append(fPath) # Save this path to return a list of temp files
        if not os.path.isfile(fPath):
          with open(fPath, "w") as f:
            f.write(cell)
        resArgs[i] = fPath # Replace %FILE argument with new file path
    return (resArgs, tempFiles)
  
  @contextlib.contextmanager
  def saveDir(self): # Help from https://stackoverflow.com/a/169112/16386050
    dir = os.getcwd()
    try: yield
    finally: os.chdir(dir)
  
  @contextlib.contextmanager
  def str_as_context(self, s): # Allows a string to be used in a context manager.
    yield s
  
  @ipym.cell_magic
  def any(self, line, cell):
    args = self.argparser.parse_args(line.split())
    remain = args.rest
    if len(remain) > 0 and remain[0] == "--":
      remain.pop(0) # Remove "--" argument
    
    output = None
    #currentDir = os.getcwd()
    
    tmpLocation = None
    if args.inplace and args.dir: # Use the working directory, --dir, for temp files as well?
      tmpLocation = self.str_as_context(args.dir) # Use --dir for tmpDir instead.
    else:
      tmpLocation = tempfile.TemporaryDirectory()
    
    with tmpLocation as tmpDir:
      with self.saveDir(): # Save current working directory
        if args.dir: # --dir    Change into specified directory, or else a temporary working directory
          os.chdir(args.dir)
        else:
          os.chdir(tmpDir)
      
        cmdArgs, tempFiles = self.parseFileMagics(tmpDir, remain, cell)
        output = self.run(cmdArgs) # Run command, handling errors.
      
        if args.inplace: # Clean up temp files if created in custom work directory
          for file in tempFiles:
            os.remove(file)
    
      if(args.print): # --print: Print output instead of outputting to a cell?
        print(output)
        output = None
    return output
      
def load_ipython_extension(ip):
  any_magic = AnyCmd(ip)
  ip.register_magics(any_magic)

