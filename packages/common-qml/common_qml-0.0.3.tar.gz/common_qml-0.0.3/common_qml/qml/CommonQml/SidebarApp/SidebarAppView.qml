// Copyright (C) 2024 twyleg
import QtQuick 2.0

Item {
    id: sidebarAppView

    enum Alignment {
        Top,
        Bottom
    }

    property alias viewProperties: properties

    anchors.fill: parent
    visible: false

    SidebarAppViewProperties {
        id: properties
    }

}
