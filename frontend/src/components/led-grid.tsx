import { memo, useEffect, useRef, useState } from "react";

const Cell = memo(({ isOn, onClick }: { isOn: boolean; onClick: () => void }) => (
  <div
    className={`rounded-full cursor-pointer transition-colors duration-200 border border-white/20 ${
      isOn ? "bg-red-500/50" : "bg-white/10"
    }`}
    onClick={onClick}
  />
));

export default function LEDGrid() {
  const [ledStates, setLedStates] = useState(Array(64).fill(false));
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const host = process.env.REACT_APP_WEBSOCKET_HOST;
    if (!host) {
      console.error("REACT_APP_WEBSOCKET_HOST environment variable is not set");
      return;
    }
    wsRef.current = new WebSocket(host);

    wsRef.current.onopen = () => {
      console.log("WebSocket connection established");
    };

    wsRef.current.onmessage = (event) => {
      const data: {
        ledStates?: {
          on?: { [key: string]: number[] };
          off?: { [key: string]: number[] };
        };
      } = JSON.parse(event.data);

        setLedStates(() => {
          const updatedStates = Array(64).fill(false);
          Object.entries(data.ledStates?.on || {}).forEach(([column, rows]) => {
            rows.forEach((row) => {
              const index = parseInt(column) + row * 8;
              updatedStates[index] = true;
            });
          });
          return updatedStates;
        });
    };

    wsRef.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    wsRef.current.onclose = () => {
      console.log("WebSocket connection closed");
    };

    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  const toggleLED = (index: number) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      setLedStates((prev) => {
        const updatedStates = [...prev];
        updatedStates[index] = !updatedStates[index];

        const column = index % 8;
        const row = Math.floor(index / 8);
        const state = updatedStates[index] ? "on" : "off";

        const ledStatesJson = {
          ledStates: {
            [state]: {
              [column]: [row],
            },
          },
        };

        wsRef.current?.send(JSON.stringify(ledStatesJson));
        console.log(`Toggled LED at index: ${index}`);
        return updatedStates;
      });
    } else {
      console.error("WebSocket is not connected");
    }
  };

  return (
    <div className="bg-black rounded-lg shadow-lg p-4 flex-1">
      <div className="grid grid-cols-8 grid-rows-8 gap-1 w-full h-full">
        {ledStates.map((isOn, index) => (
          <Cell key={index} isOn={isOn} onClick={() => toggleLED(index)} />
        ))}
      </div>
    </div>
  );
}
