// Copyright (C) 2024 twyleg
import QtQuick 2.0
import QtQuick.Layouts 1.15

Rectangle {
    id: navigationSidebar

    width: 100
    color: "#FF404142"

    property alias topColumn: topColumn
    property alias bottomColumn: bottomColumn
    property var activeButton

    property var buttonsByView: ({})

    signal activateViewRequested(view: SidebarAppView)
    signal closeViewRequested(view: SidebarAppView)


    ColumnLayout {
        id: column

        anchors.fill: parent
        spacing: 0

        ColumnLayout {
            id: topColumn

            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop

        }

        ColumnLayout {
            id: bottomColumn

            Layout.fillWidth: true
            Layout.fillHeight: false
            Layout.alignment: Qt.AlignBottom
        }
    }

    function addButton(view) {

        console.debug(`Add button for view: view=${view.viewProperties.name}`)

        var column = view.viewProperties.alignment === SidebarAppView.Alignment.Top ? topColumn : bottomColumn

        var buttonComponent = Qt.createComponent("NavigationSidebarButton.qml");
        var button = buttonComponent.createObject(column, {"view": view})

        buttonsByView[view] = button

        button.onClicked.connect(function (){
            activateViewRequested(view)
        });

        button.onCloseRequest.connect(function () {
            closeViewRequested(view)
        })
    }

    function removeButton(view) {
        buttonsByView[view].destroy()
        delete buttonsByView[view]
    }

    function activateButton(view) {
        if (activeButton) {
            activeButton.active = false
        }
        var button = buttonsByView[view]
        button.active = true
        activeButton = button
    }


}
