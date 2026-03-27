# 🚀 Smart Dynamic Route Analyser

<p align="center">
  <a href="https://github.com/ineffablexd/dynamic_route_analyser"><img src="https://img.shields.io/badge/version-1.1.1-blue.svg" alt="Version"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL--2.0--or--later-green.svg" alt="License"/></a>
  <a href="https://qgis.org"><img src="https://img.shields.io/badge/QGIS-3.0+-orange.svg" alt="QGIS Compatibility"/></a>
  <img src="https://img.shields.io/badge/Suite-Ineffable_Tools-purple.svg" alt="Suite Branding"/>
</p>

---

## 📖 Description

**Smart Dynamic Route Analyser** is a QGIS plugin developed for high-precision real-time route validation and engineering workflows. It dynamically calculates vertex angles and segment distances in meters, providing immediate visual feedback as geometry is modified. Designed for professionals working with transmission lines, pipeline routing, and corridor analysis, the tool ensures geometric integrity via intelligent coordinate handling.

---

## 🖼️ Visual Workflow

<p align="center">
  <img src="assets/before_running.png" width="48%" alt="Before Running Tool"/>
  <img src="assets/after_running.png" width="48%" alt="After Running Tool"/>
</p>
<p align="center">
  <i>Fig 1: Real-time calculation of vertex angles (blue) and segment lengths (red) during active editing.</i>
</p>

---

## ✨ Key Features

- ⚡ **Real-time Live Processing:** Instantaneous updates of vertex angles and segment distances as you modify line geometries.
- 📐 **Geometric Validation:** Automatically calculates interior angles at each vertex to monitor route deviation.
- 📏 **Metric Measurements:** Precisely measures segment lengths in meters for engineering-grade accuracy.
- 🌍 **Intelligent CRS Management:** Automatic UTM zone detection and on-the-fly reprojection based on feature centroids for precise metric units.
- 🎨 **Dynamic Labeling System:** Features high-visibility blue labels for angles and red labels for distances, rendered on temporary analysis layers.
- 🛠️ **Seamless Integration:** Fully integrated into the **Ineffable Tools** suite with a dedicated menu and toolbar action.

---

## 🛠️ Installation

### Via QGIS Plugin Manager

1.  Open **QGIS**.
2.  Navigate to `Plugins` > `Manage and Install Plugins...`.
3.  Search for **Smart Dynamic Route Analyser**.
4.  Click **Install Plugin**. (Note: Ensure the Ineffable repository is added to your plugin providers).

### Manual Installation (GitHub)

1.  Clone the repository or download the ZIP from GitHub.
2.  Extract the plugin folder into your QGIS plugins directory:
    - **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
    - **Windows:** `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
    - **MacOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3.  Restart QGIS and enable the plugin from the Plugin Manager.

---

## 🚀 How to Use

1.  **Launch Plugin:** Locate the **Ineffable Tools** menu in the top menu bar or click the plugin icon on the sidebar.
2.  **Select Layer:** A dropdown will appear; choose the active line layer you wish to analyze.
3.  **Real-time Analysis:** Once activated, the plugin creates two dynamic memory layers: `Dynamic_Vertex_Angles` and `Dynamic_Segment_Length_m`.
4.  **Edit & Update:** Switch your line layer to **Edit Mode (✏️)**. As you move vertices or add new segments, the labels will update dynamically.
5.  **Stop Tool:** Click the plugin icon again to disable the analysis and remove the temporary memory layers.

---

## 👤 Author & License

- **Author:** Vicky Sharma
- **Email:** [vsharma@powergrid.in](mailto:vsharma@powergrid.in)
- **GitHub:** [@ineffablexd](https://github.com/ineffablexd)
- **License:** Distributed under the **GPL-2.0-or-later** license. See [LICENSE](LICENSE) for more details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/ineffablexd">Ineffable</a>
</p>
