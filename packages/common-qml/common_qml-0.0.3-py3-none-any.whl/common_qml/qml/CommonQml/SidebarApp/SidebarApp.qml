// Copyright (C) 2024 twyleg
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Item {

    id: appView

    default property alias data: content.data
    property alias content: content
    property SidebarAppView activeView

    signal closeViewRequested(view: SidebarAppView)

    NavigationSidebar {
        id: navigationSidebar

        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: parent.left

        onActivateViewRequested: (view) => activateView(view)
        onCloseViewRequested: (view) => closeView(view)
    }

    Item {
        id: content

        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: navigationSidebar.right
        anchors.right: parent.right


    }

    Component.onCompleted: {

        for (var i=0; i<content.data.length; i++) {
            var child = content.data[i]
            if (child instanceof SidebarAppView) {
                var view = child
                addView(view)
            }
        }
    }

    function addView(view) {
        navigationSidebar.addButton(view)

        if (activeView === null) {
            activateView(view)
        }
    }

    function activateView(view) {
        if (activeView) {
            activeView.visible = false
        }
        view.visible = true
        activeView = view
        navigationSidebar.activateButton(view)

    }

    function closeView(view) {
        navigationSidebar.removeButton(view)
        view.destroy()
    }

}
