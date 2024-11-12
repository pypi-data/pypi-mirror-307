import QtQuick 2.0

import CommonQml.Icons 0.1

Item {
    id: sidebarAppViewProperties

    property string name
    property url iconUrl: IconLoader.getIconPath("material/radio_button_checked")
    property int alignment: SidebarAppView.Alignment.Top
    property bool closeable: true

}
