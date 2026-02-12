import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import L, { LatLngExpression } from "leaflet";

type Kangaroo = {
  id: number;
  name: string;
  lat: number;
  lon: number;
  speed_kmh: number;
};

const kangarooIcon = L.icon({
  iconUrl: "/kangaroo.png",   // path in the public folder
  iconSize: [40, 40],         // tweak size to fit your image
  iconAnchor: [20, 40],       // point of the icon that is on the position
});

type TrackMap = Record<number, LatLngExpression[]>;

function App() {
  const [kangaroos, setKangaroos] = useState<Kangaroo[]>([]);
  const [tracks, setTracks] = useState<TrackMap>({});

  useEffect(() => {
    // Initial snapshot
    fetch("http://localhost:8000/kangaroos")
      .then((res) => res.json())
      .then((data: Kangaroo[]) => {
        setKangaroos(data);
        const initialTracks: TrackMap = {};
        data.forEach((k) => {
          initialTracks[k.id] = [[k.lat, k.lon]];
        });
        setTracks(initialTracks);
      });

    // WebSocket for live updates
    const ws = new WebSocket("ws://localhost:8000/ws/kangaroos");
    ws.onmessage = (event) => {
      const data: Kangaroo[] = JSON.parse(event.data);
      setKangaroos(data);
      setTracks((prev) => {
        const next: TrackMap = { ...prev };
        data.forEach((k) => {
          const prevTrack = next[k.id] ?? [];
          next[k.id] = [...prevTrack, [k.lat, k.lon]];
        });
        return next;
      });
    };

    return () => ws.close();
  }, []);

  // Center over Australia
  const center: LatLngExpression = [-25.0, 133.0];

  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <MapContainer center={center} zoom={4} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community'
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        />
        {kangaroos.map((k) => (
          <Marker
            key={k.id}
            position={[k.lat, k.lon]}
            icon={kangarooIcon}
          />
        ))}
        {Object.entries(tracks).map(([id, points]) => (
          <Polyline key={id} positions={points} color="orange" />
        ))}
      </MapContainer>
    </div>
  );
}

export default App;
