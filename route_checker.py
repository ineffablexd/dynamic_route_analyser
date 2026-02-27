
import math
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QAction, QInputDialog, QMessageBox
from qgis.core import *
from qgis.PyQt.QtGui import QFont, QColor

class dynamicRouteChecker:

    def __init__(self, iface):
        self.iface = iface
        self.layer = None
        self.active = False
        self.point_layer = None
        self.segment_layer = None

    def initGui(self):
        self.action = QAction("Dynamic Route Checker", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.toggled.connect(self.toggle)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)

    def toggle(self, state):
        if state:
            self.start()
        else:
            self.stop()

    def start(self):

        layers = []
        for l in QgsProject.instance().mapLayers().values():
            if l.type() == QgsMapLayerType.VectorLayer and                l.geometryType() == QgsWkbTypes.LineGeometry:
                layers.append(l)

        if not layers:
            QMessageBox.critical(None, "Error", "No line layers found.")
            self.action.setChecked(False)
            return

        items = [l.name() for l in layers]
        name, ok = QInputDialog.getItem(None, "Select Line Layer",
                                        "Choose layer:", items, 0, False)
        if not ok:
            self.action.setChecked(False)
            return

        self.layer = next(l for l in layers if l.name() == name)
        self.active = True

        self.create_layers()
        self.connect_signals()
        self.update_layers()

    def stop(self):
        self.active = False
        self.disconnect_signals()

        if self.point_layer:
            QgsProject.instance().removeMapLayer(self.point_layer.id())
        if self.segment_layer:
            QgsProject.instance().removeMapLayer(self.segment_layer.id())

    def connect_signals(self):
        self.layer.geometryChanged.connect(self.update_layers)
        self.layer.featureAdded.connect(self.update_layers)
        self.layer.featureDeleted.connect(self.update_layers)

    def disconnect_signals(self):
        try:
            self.layer.geometryChanged.disconnect(self.update_layers)
            self.layer.featureAdded.disconnect(self.update_layers)
            self.layer.featureDeleted.disconnect(self.update_layers)
        except:
            pass

    def create_layers(self):

        self.point_layer = QgsVectorLayer(
            f"Point?crs={self.layer.crs().authid()}",
            "Dynamic_Vertex_Angles",
            "memory"
        )
        pr = self.point_layer.dataProvider()
        pr.addAttributes([QgsField("angle", QVariant.Double)])
        self.point_layer.updateFields()
        QgsProject.instance().addMapLayer(self.point_layer)

        self.segment_layer = QgsVectorLayer(
            f"LineString?crs={self.layer.crs().authid()}",
            "Dynamic_Segment_Length_m",
            "memory"
        )
        pr2 = self.segment_layer.dataProvider()
        pr2.addAttributes([QgsField("distance_m", QVariant.Double)])
        self.segment_layer.updateFields()
        QgsProject.instance().addMapLayer(self.segment_layer)

        self.setup_labels()

    def setup_labels(self):

        label = QgsPalLayerSettings()
        label.fieldName = "angle"
        label.placement = QgsPalLayerSettings.AroundPoint

        fmt = QgsTextFormat()
        fmt.setFont(QFont("Arial", 19))
        fmt.setSize(15)
        fmt.setColor(QColor("blue"))
        label.setFormat(fmt)

        self.point_layer.setLabeling(QgsVectorLayerSimpleLabeling(label))
        self.point_layer.setLabelsEnabled(True)

        seg_label = QgsPalLayerSettings()
        seg_label.fieldName = "distance_m"
        seg_label.placement = QgsPalLayerSettings.Line

        fmt2 = QgsTextFormat()
        fmt2.setFont(QFont("Arial", 19))
        fmt2.setSize(15)
        fmt2.setColor(QColor("red"))
        seg_label.setFormat(fmt2)

        self.segment_layer.setLabeling(QgsVectorLayerSimpleLabeling(seg_label))
        self.segment_layer.setLabelsEnabled(True)

    def update_layers(self, *args):

        if not self.active:
            return

        self.point_layer.dataProvider().deleteFeatures(
            [f.id() for f in self.point_layer.getFeatures()])
        self.segment_layer.dataProvider().deleteFeatures(
            [f.id() for f in self.segment_layer.getFeatures()])

        point_feats = []
        seg_feats = []

        for feat in self.layer.getFeatures():
            geom = feat.geometry()

            crs = self.layer.crs()

            if crs.mapUnits() == QgsUnitTypes.DistanceMeters:
                geom_projected = QgsGeometry(geom)

            else:
               
                center = geom.boundingBox().center()

                transform_to_wgs = QgsCoordinateTransform(
                    crs,
                    QgsCoordinateReferenceSystem("EPSG:4326"),
                    QgsProject.instance()
                )

                center_wgs = transform_to_wgs.transform(center)

                zone = int((center_wgs.x() + 180) / 6) + 1
                epsg = f"EPSG:326{zone:02d}" if center_wgs.y() >= 0 else f"EPSG:327{zone:02d}"

                utm_crs = QgsCoordinateReferenceSystem(epsg)

                transform_to_utm = QgsCoordinateTransform(
                    crs,
                    utm_crs,
                    QgsProject.instance()
                )

                geom_projected = QgsGeometry(geom)
                geom_projected.transform(transform_to_utm)

            vertices = geom_projected.asPolyline() if not geom_projected.isMultipart() else geom_projected.asMultiPolyline()[0]

            if len(vertices) < 2:
                continue

            for i in range(1, len(vertices)-1):
                angle = self.calculate_angle(vertices[i-1], vertices[i], vertices[i+1])
                f = QgsFeature(self.point_layer.fields())
                f.setGeometry(QgsGeometry.fromPointXY(transform_to_utm.transform(vertices[i], QgsCoordinateTransform.ReverseTransform)))
                f.setAttribute("angle", round(angle,2))
                point_feats.append(f)

            for i in range(len(vertices)-1):
                p1 = vertices[i]
                p2 = vertices[i+1]
                dist = math.hypot(p2.x() - p1.x(), p2.y() - p1.y())

                orig_p1 = transform_to_utm.transform(p1, QgsCoordinateTransform.ReverseTransform)
                orig_p2 = transform_to_utm.transform(p2, QgsCoordinateTransform.ReverseTransform)

                f2 = QgsFeature(self.segment_layer.fields())
                f2.setGeometry(QgsGeometry.fromPolylineXY([orig_p1, orig_p2]))
                f2.setAttribute("distance_m", round(dist,2))
                seg_feats.append(f2)

        self.point_layer.dataProvider().addFeatures(point_feats)
        self.segment_layer.dataProvider().addFeatures(seg_feats)

        self.point_layer.updateExtents()
        self.segment_layer.updateExtents()

        self.point_layer.triggerRepaint()
        self.segment_layer.triggerRepaint()

    def compute_azimuth(self, p1, p2):
        angle_rad = math.atan2(p2.y() - p1.y(), p2.x() - p1.x())
        angle_deg = math.degrees(angle_rad)
        return angle_deg if angle_deg >= 0 else angle_deg + 360

    def calculate_angle(self, p_prev, p_curr, p_next):
        incoming = self.compute_azimuth(p_prev, p_curr)
        outgoing = self.compute_azimuth(p_curr, p_next)
        diff = (outgoing - incoming + 180) % 360 - 180
        return abs(diff)
