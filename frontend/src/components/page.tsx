import LEDGrid from "./led-grid";
import { PiStream } from "./pi-stream";

export default function Page() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-black">
      <div className="grid grid-cols-1 sm:grid-cols-2">
        {/* LED Grid Container */}
        <div className="flex flex-1 bg-gray-200 p-4 rounded-lg shadow-md m-2 min-w-[40vw] aspect-square">
          {/* <h2 className="text-xl font-bold mb-4">LED Grid</h2> */}
          <LEDGrid />
        </div>
        {/* Twitch Player Container */}
        <div className="flex flex-1 bg-gray-200 p-4 rounded-lg shadow-md m-2 min-w-[40vw] aspect-square">
          {/* <h2 className="text-xl font-bold mb-4">Twitch Player</h2> */}
          {/* <TwitchStream /> */}
          <PiStream />
        </div>
      </div>
    </div>
  );
}
