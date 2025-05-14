# AnyCmd

&nbsp;&nbsp;&nbsp;&nbsp;Do the provided cell magics not quite fit your needs? AnyCmd is a versatile Jupyter cell magic that allows you to run a cell with any command line utility. Simply specify the command you want to run as arguments after the magic. Access the contents of the cell as a file using the literal string "%FILE" or "%FILE.someExtension"  
&nbsp;&nbsp;&nbsp;&nbsp;By default, the command specified after the magic will be run from a temporary working directory. However, you may use -d/--dir <directory> to chdir into a custom directory before running the cell command. Use "-d ." to run it in the current working directory.  
&nbsp;&nbsp;&nbsp;&nbsp;Use -i/--inplace if you would like to write the cell contents temp files in the specified working directory, rather than the temporary directory (has no effect without --dir). This may help with compilers that reference libraries in the same directory, for instance.  
&nbsp;&nbsp;&nbsp;&nbsp;Use "-p/--print" to print command output live, instead of outputting to the cell. This may improve readability, and make it easier to debug long-running commands.  
&nbsp;&nbsp;&nbsp;&nbsp; --nonewline **prevents** adding a newline character before the cell contents in the temporary file to offset the first line taken up by the cell magic in order to fix line numbers from error messages. _[Changed in 0.1.4: this is now the default behavior and --lines was removed]._

  
#### You may install this package via PyPi:
```
!pip install anycmd-jupyter-magic
%load_ext anycmd
```

#### Example (compiling and running c++):  
___
```
%%any -p -l -- clang++ -O3 %FILE.cpp -o file && ./file

#include <iostream>  
using namespace std;  
int main(int argc, const char** argv) {  
  cout << "Hello World\n";  
}  
```
___
Result:  
Hello World  
