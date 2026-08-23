import { useEffect } from "react";
import { useMap } from "react-leaflet";

export function MapRegistry({ mapId }) {
  const map = useMap();

  useEffect(() => {
    window.__reflexLeafletMaps ??= {};

    window.__reflexLeafletMaps[mapId] = map;

    return () => {
      if (window.__reflexLeafletMaps) {
        delete window.__reflexLeafletMaps[mapId];
      }
    };
  }, [map, mapId]);

  return null;
}