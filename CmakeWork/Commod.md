# this is for the cmake learning
//2023.4.22 陈东贡献

## 检测CMake 与C++ 环境

打开cmd.exe 
输入：
gcc --version
cmake --version

#创建一个空的文件夹，并设为工作目录
mkdir testdir
cd testdir
code .   //在当前目录用vscode打开

## 使用ctrl + shift + p ,输入 CMake: quick start 
就可以得到一个默认输出hello World 的项目。


## CMakeLists.txt

cmake_minimum_required(VERSION 3.26) //最低版本要求

project (ExampleProject) //项目命名

add_executable(ExampleProject main.cpp) //添加源文件

## main.cpp

// main.cpp
#include <iostream>

using namespace std;

int main(void)
{
    cout<<"Hello World"<<endl;
}
