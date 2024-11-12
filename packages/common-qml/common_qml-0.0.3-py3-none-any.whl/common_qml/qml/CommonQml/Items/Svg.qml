// Copyright (C) 2024 twyleg
import QtQuick 2.0

Image {
    id: svg

    fillMode: Image.PreserveAspectFit

    sourceSize.height: height
    sourceSize.width: width

    function reload() {
        var bak = svg.source
        svg.source = ""
        svg.source = bak
    }

}
