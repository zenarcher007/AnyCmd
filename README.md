# AnyCmd

AnyCmd is a versatile Jupyter cell magic that allows you to run a cell with any utility. Simply specify the command you want to run as arguments after the magic. Access the contents of the cell as a file using the literal string "%FILE" or "%FILE.someExtension"  
By default, the command specified after the magic will be run in a temporary working directory. However, you can specify a custom location using "-d/--dir"; use "-d ." if you would like your cell to be run in the current working directory. 

#### Example (compiling and running c++):  
!git config --global url.\"https://github.com/\".insteadOf git://github.com/
!pip install git+https://github.com/zenarcher007/AnyCmd.git
%load_ext anycmd
___
##### %%any clang++ -O3 %FILE.cpp -o file && ./file

\#include \<iostream\>  
using namespace std;  
int main(int argc, const char** argv) {  
&nbsp;&nbsp;&nbsp;&nbsp;cout << "Hello World\n";  
}  
___
Result:  
Hello World  
