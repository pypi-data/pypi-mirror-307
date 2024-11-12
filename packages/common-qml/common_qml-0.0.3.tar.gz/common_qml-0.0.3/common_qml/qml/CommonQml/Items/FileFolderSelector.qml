// Copyright (C) 2024 twyleg
import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs // No version specified: QtQuick.Dialogs does not require a version in this context

RowLayout {
    id: fileFolderSelector

    enum Type {
        File,
        Folder
    }

    property alias text: headlineText.text
    property alias nameFilters: fileDialog.nameFilters
    property alias value: valueTextEdit.text
    property int type:  FileFolderSelector.Type.File

    property int fontPointSize: 12

    Text {
        id: headlineText

        color: "white"
        font.pointSize: parent.fontPointSize

    }

    Rectangle {

        Layout.fillWidth: true
        Layout.fillHeight: true

        border.color: "white"
        border.width: 1

        color: "transparent"

        TextEdit {
            id: valueTextEdit

            anchors.fill: parent
            anchors.leftMargin: 5

            color: "white"
            text: fileFolderSelector.type === FileFolderSelector.Type.Folder ? folderDialog.selectedFolder : fileDialog.selectedFile

            verticalAlignment: TextEdit.AlignVCenter

            font.pointSize: fileFolderSelector.fontPointSize
        }
    }

    Button {
        id: fileButton

        Layout.fillHeight: true

        text: fileFolderSelector.type === FileFolderSelector.Type.Folder ? "Folder" : "File"
        onClicked: {
            if (fileFolderSelector.type === FileFolderSelector.Type.Folder) {
                folderDialog.visible = true
            } else {
                fileDialog.visible = true
            }
        }
    }

    FileDialog {
        id: fileDialog
        visible: false

        onSelectedFileChanged: {
            console.debug("FileDialog: " + selectedFile)
            valueTextEdit.text = urlToPath(selectedFile.toString())
        }
    }

    FolderDialog {
        id: folderDialog
        visible: false

        onSelectedFolderChanged: {
            console.debug("FolderDialog: " + selectedFolder)
            fileFolderSelector.value = urlToPath(selectedFolder.toString())
        }
    }

    function urlToPath(urlString) {
        var s
        if (urlString.startsWith("file:///")) {
            var k = urlString.charAt(9) === ':' ? 8 : 7
            s = urlString.substring(k)
        } else {
            s = urlString
        }
        return decodeURIComponent(s);
    }

}
