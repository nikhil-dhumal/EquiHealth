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
const DEFAULT_ZOOM = 5;

const ZoomHandler = ({ setZoom }) => {
  useMapEvents({
    zoomend: (e) => setZoom(e.target.getZoom()),
  });
  return null;
};

const aggregateBeds = (hospitals, key, districts, states) => {
  const map = {};

  hospitals.forEach((hosp) => {
    let id,
      lat,
      lng,
      name,
      population = 0;

    if (key === "state") {
      id = hosp.state_id;
      const s = states.byId[id];
      lat = s?.latitude;
      lng = s?.longitude;
      name = s?.state_name;

      population = districts.allIds
        .map((dId) => districts.byId[dId])
        .filter((d) => d.state_id === id)
        .reduce((acc, d) => acc + (d.total_persons || 0), 0);
    } else if (key === "district") {
      id = hosp.district_id;
      const d = districts.byId[id];
      lat = d?.latitude;
      lng = d?.longitude;
      name = d?.district_name;
      population = d?.total_persons || 0;
    } else {
      id = hosp.hospital_id;
      lat = hosp.latitude;
      lng = hosp.longitude;
      name = hosp.hospital_name;
    }

    if (!id) return;

    if (!map[id])
      map[id] = {
        latitude: lat,
        longitude: lng,
        total_beds: 0,
        name,
        population,
      };

    map[id].total_beds += hosp.total_beds || 0;
  });

  if (key !== "hospital") {
    Object.values(map).forEach((item) => {
      item.beds_per_1000 = item.population
        ? (item.total_beds / item.population) * 1000
        : 0;
    });
  }

  return Object.values(map);
};

const MapZoomController = ({ selected }) => {
  const map = useMap();
  const { states, districts, hospitals } = useSelector(
    (state) => state.healthInfra
  );

  useEffect(() => {
    let lat, lng, zoom;

    if (selected?.hospital) {
      const h = hospitals.byId[selected.hospital.value];
      lat = h?.latitude;
      lng = h?.longitude;
      zoom = 15;
    } else if (selected?.district) {
      const d = districts.byId[selected.district.value];
      lat = d?.latitude;
      lng = d?.longitude;
      zoom = 9;
    } else if (selected?.state) {
      const s = states.byId[selected.state.value];
      lat = s?.latitude;
      lng = s?.longitude;
      zoom = 6;
    } else {
      lat = DEFAULT_CENTER[0];
      lng = DEFAULT_CENTER[1];
      zoom = DEFAULT_ZOOM;
    }

    map.setView([lat, lng], zoom);
  }, [selected, map, states, districts, hospitals]);

  return null;
};

const Map = ({ selected }) => {
  const { states, districts, hospitals } = useSelector(
    (state) => state.healthInfra
  );
  const [zoom, setZoom] = useState(DEFAULT_ZOOM);

  const hospitalList = hospitals.allIds.map((id) => hospitals.byId[id]);

  const filteredHospitals = useMemo(() => {
    if (selected?.hospital) return [hospitals.byId[selected.hospital.value]];
    if (selected?.district)
      return hospitalList.filter(
        (h) => h.district_id === selected.district.value
      );
    if (selected?.state)
      return hospitalList.filter((h) => h.state_id === selected.state.value);
    return hospitalList;
  }, [hospitalList, selected]);

  const displayData = useMemo(() => {
    if (selected.hospital)
      return aggregateBeds(filteredHospitals, "hospital", districts, states);
    if (zoom <= 5)
      return aggregateBeds(filteredHospitals, "state", districts, states);
    if (zoom <= 8)
      return aggregateBeds(filteredHospitals, "district", districts, states);
    return aggregateBeds(filteredHospitals, "hospital", districts, states);
  }, [filteredHospitals, zoom, selected, districts, states]);

  const getRadius = (item) => {
    if (item.beds_per_1000 !== undefined) {
      if (zoom <= 5) return Math.max(10, item.beds_per_1000 * 4);
      if (zoom <= 8) return Math.max(8, item.beds_per_1000 * 3);
    }
    return Math.max(6, Math.sqrt(item.total_beds) * 0.5);
  };

  const getTooltipContent = (item) => {
    if (item.beds_per_1000 !== undefined) {
      return (
        <>
          <strong>{item.name}</strong>
          <br />
          Beds/1000: {item.beds_per_1000.toFixed(2)}
        </>
      );
    }
    return (
      <>
        <strong>{item.name}</strong>
        <br />
        Beds: {item.total_beds}
      </>
    );
  };

  return (
    <MapContainer className="map" center={DEFAULT_CENTER} zoom={DEFAULT_ZOOM}>
      <TileLayer
        attribution='&copy; <a href="https://osm.org">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MapZoomController selected={selected} />
      <ZoomHandler setZoom={setZoom} />

      {displayData.map((item, i) => (
        <CircleMarker
          key={i}
          center={[item.latitude, item.longitude]}
          radius={getRadius(item)}
          fillColor="rgba(0,123,255,0.6)"
          color="rgba(0,0,0,0.3)"
          weight={1}
          fillOpacity={0.7}
        >
          <Tooltip>
            <div style={{ textAlign: "center" }}>{getTooltipContent(item)}</div>
          </Tooltip>
        </CircleMarker>
      ))}
    </MapContainer>
  );
};

export default Map;
