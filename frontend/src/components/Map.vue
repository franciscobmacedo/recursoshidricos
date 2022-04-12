<template>
  <div id="container">
    <div id="mapContainer"></div>
  </div>
</template>
<script>
import { mapGetters, mapState } from "vuex";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import L from "leaflet";
import turf from "turf";
import "leaflet-draw";

export default {
  name: "Map",
  data() {
    return {
      map: null,
      center: [39.65, -7.85],
      iconSize: [0, 0],
      iconAnchor: [0, 0],

      markers: [],
      selectedMarkers: [],
    };
  },
  watch: {
    stations(newStations) {
      console.log("changing stations", newStations);
      this.markers.map((marker) => {
        this.map.removeLayer(marker);
      });
      this.markers = [];
      newStations.forEach((station) => {
        this.addMarker(station);
      });
    },
    selectedStationsIDs(items) {
      this.markers.forEach((m) => {
        if (items.includes(m.stationID)) {
          m.setIcon(this.selectedIcon);
        } else {
          m.setIcon(this.icon);
        }
      });
    },
  },
  computed: {
    ...mapState(["stations"]),
    ...mapGetters(["selectedStationsIDs"]),
    icon() {
      return L.divIcon({
        className: "custom-div-icon",
        html: "<div  class='marker-pin'></div>",
        iconSize: this.iconSize,
        iconAnchor: this.iconAnchor,
      });
    },
    selectedIcon() {
      return L.divIcon({
        className: "custom-div-icon",
        html: "<div  class='marker-pin selected'></div>",
        iconSize: this.iconSize,
        iconAnchor: this.iconAnchor,
      });
    },
  },
  methods: {
    setupLeafletMap: function () {
      this.map = L.map("mapContainer", {
        zoomSnap: 0.1,
      }).setView(this.center, 7.4);
      L.tileLayer(
        "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
        {
          maxZoom: 18,
          id: "mapbox/light-v9",
          accessToken:
            "pk.eyJ1IjoiZm1hY2VkbzEiLCJhIjoiY2sxODlsdjI1MGdjZjNlbXp1cHVzMmdsMSJ9.XS7XUAnQ6r5fAgzQx0OSmQ",
        }
      ).addTo(this.map);

      this.setLeafletDraw();
    },
    setLeafletDraw() {
      var drawnItems = new L.FeatureGroup();

      const options = {
        // position: "topright",
        draw: {
          polyline: {
            shapeOptions: {
              color: "#f357a1",
              weight: 10,
            },
          },
          polygon: {
            allowIntersection: false, // Restricts shapes to simple polygons
            drawError: {
              color: "#e1e100", // Color the shape will turn when intersects
              message: "<strong>Oh snap!<strong> you can't draw that!", // Message that will show when intersect
            },
            shapeOptions: {
              color: "#bada55",
            },
          },
          rectangle: {
            shapeOptions: {
              clickable: false,
            },
          },
        },
        edit: {
          featureGroup: drawnItems,
        },
      };

      this.map.addLayer(drawnItems);
      var drawControl = new L.Control.Draw(options);
      this.map.addControl(drawControl);
      L.Polygon.include({
        contains: function (latLng) {
          return turf.inside(
            new L.Marker(latLng).toGeoJSON(),
            this.toGeoJSON()
          );
        },
      });
      L.Circle.include({
        contains: function (latLng) {
          return this.getLatLng().distanceTo(latLng) < this.getRadius();
        },
      });

      this.map.on(L.Draw.Event.CREATED, (e) => {
        const selectedStationsIDs = [];
        this.markers.forEach((marker) => {
          if (e.layer.contains(marker.getLatLng())) {
            selectedStationsIDs.push(marker.stationID);
          }
        });

        this.$store.commit("setselectedStationsByID", selectedStationsIDs);
      });
    },

    addMarker(station) {
      const marker = L.marker([station.latitude, station.longitude], {
        icon: this.icon,
        uniqueID: station.uid,
      })
        .addTo(this.map)
        .on("click", this.clickMarker);
      marker.bindTooltip(station.nome);
      marker.stationID = station.uid;
      this.markers.push(marker);
    },
    clickMarker(e) {
      let selectedStationsIDs;
      if (e.originalEvent.metaKey) {
        if (this.selectedStationsIDs.includes(e.target.stationID)) {
          selectedStationsIDs = this.selectedStationsIDs.filter(
            (id) => id != e.target.stationID
          );
        } else {
          selectedStationsIDs = [
            ...this.selectedStationsIDs,
            e.target.stationID,
          ];
        }
      } else {
        if (this.selectedStationsIDs.includes(e.target.stationID)) {
          selectedStationsIDs = [];
        } else {
          selectedStationsIDs = [e.target.stationID];
        }
      }
      console.log(selectedStationsIDs);
      this.$store.commit("setselectedStationsByID", selectedStationsIDs);
    },
  },
  mounted() {
    this.setupLeafletMap();
  },
};
</script>

<style>
#mapContainer {
  width: 400px;
  height: 800px;
  z-index: 0;
}
.marker-pin {
  width: 10px;
  height: 10px;
  border-radius: 50% 50% 50% 0;
  background: rgba(88, 141, 211, 0.8);
  position: absolute;
  transform: rotate(-45deg);
  left: 50%;
  top: 50%;
  margin: -5px 0 0 -5px;
}

.selected {
  background: #f32c2c;
}
</style>