import QtQuick 2.0
import CommonQml.Icons 0.1

Svg {

    source: IconLoader.getIconPath("twyleg/rotation_loading_large")

    property alias running: animation.running

    visible: false


    NumberAnimation on rotation {
        id: animation

        running: false
        from: 0
        to: 360
        duration: 1000
        loops: Animation.Infinite
    }

    function start() {
        visible = true
        animation.start()
    }

    function stop() {
        visible = false
        animation.stop()
    }
}
