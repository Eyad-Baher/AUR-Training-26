pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Shapes

Item {
    id: root
    width: 400
    height: 400

    property var clockData
    property real hours: clockData ? clockData.hours : 0
    property real minutes: clockData ? clockData.mins : 0
    property real seconds: clockData ? clockData.secs : 0

    Item {
        id: clockFace
        property real size: Math.min(root.width, root.height)
        width: size
        height: size
        anchors.centerIn: parent

        Rectangle {
            anchors.fill: parent
            anchors.margins: 10
            radius: width / 2
            color: "#FFFFFF"
            border.color: "#555555"
            border.width: 12
        }

        Repeater {
            model: 60
            Item {
                required property int index
                x: clockFace.width / 2
                y: clockFace.height / 2
                rotation: index * 6

                Rectangle {
                    x: -width / 2
                    y: -(clockFace.height / 2 - 22)
                    width: parent.index % 5 === 0 ? 4 : 2
                    height: parent.index % 5 === 0 ? 14 : 7
                    color: "#000000"
                }
            }
        }

        Repeater {
            model: 12
            Item {
                required property int index
                property int num: index + 1
                property real angle: num * (360 / 12) * (Math.PI / 180)

                Text {
                    text: parent.num.toString()
                    font.pixelSize: 18
                    font.bold: true
                    color: "#000000"
                    
                    x: (clockFace.width / 2) + (clockFace.width / 2 - 50) * Math.sin(parent.angle) - width / 2
                    y: (clockFace.height / 2) - (clockFace.height / 2 - 50) * Math.cos(parent.angle) - height / 2
                }
            }
        }

        Rectangle {
            x: clockFace.width / 2 - width / 2
            y: clockFace.height / 2 - height
            width: 8
            height: clockFace.height * 0.25
            color: "#111111"
            radius: 4
            transformOrigin: Item.Bottom
            rotation: (root.hours + root.minutes / 60) * (360 / 12)
        }

        Rectangle {
            x: clockFace.width / 2 - width / 2
            y: clockFace.height / 2 - height
            width: 5
            height: clockFace.height * 0.35
            color: "#111111"
            radius: 2
            transformOrigin: Item.Bottom
            rotation: (root.minutes + root.seconds / 60) * (360 / 60)
        }

        Rectangle {
            x: clockFace.width / 2 - width / 2
            y: clockFace.height / 2 - height + 20
            width: 2
            height: clockFace.height * 0.40
            color: "#E53935"
            transformOrigin: Item.Bottom
            rotation: root.seconds * (360 / 60)
        }

        Rectangle {
            anchors.centerIn: parent
            width: 12
            height: 12
            radius: 6
            color: "#E53935"
        }
    }
}