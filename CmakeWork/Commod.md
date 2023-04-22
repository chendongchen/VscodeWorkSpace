# this is for the cmake learning
//2023.4.22 陈东贡献

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
