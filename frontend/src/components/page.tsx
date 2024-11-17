import LEDGrid from "./led-grid";
import TwitchStream from "./twitch-player";

export default function Page() {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4">
            <div className="flex flex-row items-center justify-center w-full">
                <div className="flex-1 bg-gray-200 p-4 rounded-lg shadow-md m-2 h-96">
                    <h2 className="text-xl font-bold mb-4">LED Grid</h2>
                    <LEDGrid />
                </div>
                <div className="flex-1 bg-gray-200 p-4 rounded-lg shadow-md m-2 h-96">
                    <h2 className="text-xl font-bold mb-4">Twitch Player</h2>
                    <TwitchStream />
                </div>
            </div>
        </div>
    );
};
