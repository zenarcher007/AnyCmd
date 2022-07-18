# AnyCmd

&nbsp;&nbsp;&nbsp;&nbsp;Do the provided cell magics not quite fit your needs? AnyCmd is a versatile Jupyter cell magic that allows you to run a cell with any utility. Simply specify the command you want to run as arguments after the magic. Access the contents of the cell as a file using the literal string "%FILE" or "%FILE.someExtension"  
&nbsp;&nbsp;&nbsp;&nbsp;By default, the command specified after the magic will be run from a temporary working directory. However, you may use -d/--dir <directory> to chdir into a custom directory before running the cell command. Use "-d ." to run it in the current working directory.  
&nbsp;&nbsp;&nbsp;&nbsp;Use -i/--inplace if you would like to write the cell contents temp files in the specified working directory, rather than the temporary directory (has no effect without --dir). This may help with compilers that reference libraries in the same directory, for instance.  
&nbsp;&nbsp;&nbsp;&nbsp;Use "-p/--print" to print command output instead of outputting to the cell. This can improve readability.  

  
  

#### Example (compiling and running c++):  
!git config --global url.\"https://github.com/\".insteadOf git://github.com/  
!pip install git+https://github.com/zenarcher007/AnyCmd.git  
%load_ext anycmd
___
##### %%any -p -- clang++ -O3 %FILE.cpp -o file && ./file

\#include \<iostream\>  
using namespace std;  
int main(int argc, const char** argv) {  
&nbsp;&nbsp;&nbsp;&nbsp;cout << "Hello World\n";  
}  
___
Result:  
Hello World  
