import React, { useEffect, useMemo, useState } from "react";
import { useSelector } from "react-redux";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Tooltip,
  useMapEvents,
  useMap,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

const DEFAULT_CENTER = [22.9734, 78.6569];

const ZoomHandler = ({ setZoom }) => {
  useMapEvents({
    zoomend: (e) => {
      setZoom(e.target.getZoom());
    },
  });
  return null;
};

const aggregateBeds = (hospitals, key) => {
  const map = {};
  hospitals.forEach((hosp) => {
    let id, lat, lng, name;
    if (key === "state") {
      id = hosp.state?.state_id;
      lat = hosp.state?.latitude;
      lng = hosp.state?.longitude;
      name = hosp.state?.state_name;
    } else if (key === "district") {
      id = hosp.district?.district_id;
      lat = hosp.district?.latitude;
      lng = hosp.district?.longitude;
      name = hosp.district?.district_name;
    } else {
      id = hosp.hospital_id;
      lat = hosp.latitude;
      lng = hosp.longitude;
      name = hosp.hospital_name;
    }
    if (!id) return;
    if (!map[id])
      map[id] = { latitude: lat, longitude: lng, total_beds: 0, name };
    map[id].total_beds += hosp.total_beds || 0;
  });
  return Object.values(map);
};

const MapZoomController = ({ selected }) => {
  const map = useMap();

  useEffect(() => {
    let lat, lng, targetZoom;

    if (selected.hospital) {
      lat = selected.hospital.latitude;
      lng = selected.hospital.longitude;
      targetZoom = 15;
    } else if (selected.district) {
      lat = selected.district.latitude;
      lng = selected.district.longitude;
      targetZoom = 9;
    } else if (selected.state) {
      lat = selected.state.latitude;
      lng = selected.state.longitude;
      targetZoom = 6;
    } else {
      lat = DEFAULT_CENTER[0];
      lng = DEFAULT_CENTER[1];
      targetZoom = 5;
    }

    if (lat && lng) {
      map.setView([lat, lng], targetZoom);
    }
  }, [selected, map]);

  return null;
};

const Map = ({ selected }) => {
  const { hospitals } = useSelector((state) => state.hospitals);

  const [zoom, setZoom] = useState(5);

  const displayData = useMemo(() => {
    if (zoom <= 5) return aggregateBeds(hospitals, "state");
    if (zoom <= 8) return aggregateBeds(hospitals, "district");
    return aggregateBeds(hospitals, "hospital");
  }, [hospitals, zoom]);

  const getRadius = () => {
    if (zoom <= 5) return 15;
    if (zoom <= 8) return 10;
    return 6;
  };

  return (
    <MapContainer className="map" center={DEFAULT_CENTER} zoom={5}>
      <TileLayer
        attribution='&copy; <a href="https://osm.org">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MapZoomController selected={selected} />
      <ZoomHandler setZoom={setZoom} />
      {displayData.map((item, index) => (
        <CircleMarker
          key={index}
          center={[item.latitude, item.longitude]}
          radius={getRadius()}
          fillColor="rgba(0,123,255,0.6)"
          color="rgba(0,0,0,0.3)"
          weight={1}
          fillOpacity={0.7}
        >
          <Tooltip direction="top" offset={[0, -5]} opacity={1}>
            <div style={{ textAlign: "center" }}>
              <strong>{item.name}</strong>
              <br />
              Beds: {item.total_beds}
            </div>
          </Tooltip>
        </CircleMarker>
      ))}
    </MapContainer>
  );
};

export default Map;
