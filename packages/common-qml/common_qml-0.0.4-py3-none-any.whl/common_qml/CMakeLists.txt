# Copyright (C) 2024 twyleg
cmake_minimum_required(VERSION 3.16.3)

if (NOT DEFINED QML_IMPORT_PATH)
    set(QML_IMPORT_PATH "${CMAKE_CURRENT_SOURCE_DIR}/qml/" CACHE PATH "QML Import Path")
endif()

list(APPEND QML_IMPORT_PATH "${CMAKE_CURRENT_SOURCE_DIR}/qml/")
