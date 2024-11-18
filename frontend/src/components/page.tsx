import LEDGrid from "./led-grid";
import TwitchStream from "./twitch-player";

export default function Page() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <div className="grid grid-cols-1 sm:grid-cols-2">
        {/* LED Grid Container */}
        <div className="flex-1 bg-gray-200 p-4 rounded-lg shadow-md m-2 min-w-96 w-[35vw]">
          <h2 className="text-xl font-bold mb-4">LED Grid</h2>
          <LEDGrid />
        </div>
        {/* Twitch Player Container */}
        <div className="flex-1 bg-gray-200 p-4 rounded-lg shadow-md m-2 min-w-96 w-[35vw]">
          <h2 className="text-xl font-bold mb-4">Twitch Player</h2>
          <TwitchStream />
        </div>
      </div>
    </div>
  );
}
