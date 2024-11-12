// Copyright (C) 2024 twyleg
import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

import CommonQml.Items 0.1

Rectangle {
    id: navigationSidebarButton

    width: parent.width
    height: width

    property SidebarAppView view

    property color hoveredColor: "#FF5E5F60"
    property color activeColor: "#FF212222"
    property color inactiveColor: "#FF404142"
    property bool active: false

    signal clicked()
    signal closeRequest()

    color: inactiveColor

    Rectangle {
        id: activeIndicatorRectangle

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom

        width: 3

        visible: navigationSidebarButton.active

        color: "#FFC2C4C5"
    }

    ColumnLayout {
        id: imageTextColumn

        anchors.left: activeIndicatorRectangle.right
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom

        anchors.bottomMargin: 20



        Svg {

            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.margins: 10

            Layout.alignment: Qt.AlignHCenter

            source: view.viewProperties.iconUrl

        }

        Text {
            text: view.viewProperties.name

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter

            font.bold: true

            color: "#ffb2b2b2"

            clip: true
        }
    }

    ColorAnimation on color {
        id: colorAnimation
        running: false
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MiddleButton

        onEntered: {
            if (!active) {
                colorAnimation.stop()
                colorAnimation.to = hoveredColor
                colorAnimation.duration = 50
                colorAnimation.start()
            }
        }

        onExited: {
            if (!active) {
                colorAnimation.stop()
                colorAnimation.to = inactiveColor
                colorAnimation.duration = 300
                colorAnimation.start()
            }
        }

        onClicked: (mouse) => {
            if (mouse.button === Qt.LeftButton) {
                navigationSidebarButton.clicked()
            } else if (mouse.button === Qt.RightButton) {
                contextMenu.popup()
            } else if(mouse.button === Qt.MiddleButton) {
                if(view.viewProperties.closeable) {
                    navigationSidebarButton.closeRequest()
                }
           }
        }
    }

    Menu {
        id: contextMenu
        MenuItem {
            text: "Close"
            enabled: view.viewProperties.closeable
            onClicked: {
                console.debug("Close requested by context menu: view=", view.viewProperties.name)
                navigationSidebarButton.closeRequest()
            }
        }
    }

    onActiveChanged: {
        colorAnimation.stop()
        color = active ? activeColor : inactiveColor
    }
}
