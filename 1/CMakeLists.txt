cmake_minimum_required(VERSION 3.10)
project(WaveEnergyProject)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找 Python 和 PyBind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

# 添加 C++ 源文件并创建可执行文件
add_executable(wave_energy_solver src/main.cpp src/bindings.cpp src/utilities.cpp)

# 添加 Python 模块
pybind11_add_module(ODESolver src/main.cpp src/bindings.cpp src/utilities.cpp)
target_include_directories(ODESolver PRIVATE ${CMAKE_SOURCE_DIR}/include)

# 包含头文件目录
target_include_directories(wave_energy_solver PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${Python_INCLUDE_DIRS}
    ${pybind11_INCLUDE_DIRS}
)

# 链接库
target_link_libraries(wave_energy_solver PRIVATE
    ${Python_LIBRARIES}
    pybind11::pybind11
    ${PYTHON_MODULE_NAME} PRIVATE 
    pybind11::module
)

# 添加 Python 脚本的自定义命令
add_custom_command(
    OUTPUT python_scripts
    COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/python/main.py
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Running Python scripts"
)

# 添加安装规则
install(FILES ${CMAKE_SOURCE_DIR}/python/main.py ${CMAKE_SOURCE_DIR}/python/helpers.py DESTINATION python)