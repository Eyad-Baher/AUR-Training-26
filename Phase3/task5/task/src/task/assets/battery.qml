import QtQuick
import QtQuick.Shapes
import QtQuick.Effects

Rectangle {
    id: root
    width: 300
    height: 200
    color: palette.window

    required property var batteryData

    Rectangle {
        id: batteryBody
        anchors.rightMargin: parent.width * 0.05
        anchors.fill: parent
        radius: 16
        border.width: 4
        border.color: palette.window.hsvValue > 0.5 ? '#1f1f1f' : '#cccccc'
        color: 'transparent'

        Rectangle {
            id: mask
            anchors.fill: parent
            anchors.margins: parent.border.width
            radius: parent.radius - parent.border.width + 1
            layer.enabled: true
            visible: false
        }

        Item {
            id: fillContainer
            anchors.fill: mask
            visible: false

            Rectangle {
                id: fillBar
                width: parent.width * batteryData.batteryLevel
                height: parent.height
                color: 'green'
                
                Behavior on width {
                    NumberAnimation { duration: 300 }
                }
            }
        }

        MultiEffect {
            anchors.fill: mask
            source: fillContainer
            maskEnabled: true
            maskSource: mask
        }

        Text {
            property real percentage: batteryData.batteryLevel * 100

            text: percentage.toFixed(0) + '%'
            color: palette.window.hsvValue > 0.5 ? '#1f1f1f' : '#cccccc'
            font.pixelSize: parent.height < parent.width ? parent.height / 3 : parent.width / 3
            font.bold: true
            anchors.centerIn: parent
        }
    }

    Shape {
        id: batteryKnob
        width: parent.width * 0.05 + 2
        height: parent.height * 0.5
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter

        property int myRadius: 6

        ShapePath {
            fillColor: root.palette.window.hsvValue > 0.5 ? '1f1f1f' : '#cccccc'
            strokeColor: root.palette.window.hsvValue > 0.5 ? '#1f1f1f' : '#cccccc'

            startX: 0
            startY: 0

            PathLine {
                x: batteryKnob.width - batteryKnob.myRadius
                y: 0
            }
            PathArc {
                x: batteryKnob.width
                y: batteryKnob.myRadius
                radiusX: batteryKnob.myRadius
                radiusY: batteryKnob.myRadius
                direction: PathArc.Clockwise
            }
            PathLine {
                x: batteryKnob.width
                y: batteryKnob.height - batteryKnob.myRadius
            }
            PathArc {
                x: batteryKnob.width - batteryKnob.myRadius
                y: batteryKnob.height
                radiusX: batteryKnob.myRadius
                radiusY: batteryKnob.myRadius
                direction: PathArc.Clockwise
            }
            PathLine {
                x: 0
                y: batteryKnob.height
            }
            PathLine {
                x: 0
                y: 0
            }
        }
    }
}