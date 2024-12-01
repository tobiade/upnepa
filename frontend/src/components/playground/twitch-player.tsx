import { TwitchEmbed } from "react-twitch-embed";

export default function TwitchStream() {
  return (
    <div className="flex-1 rounded-lg overflow-hidden shadow-lg">
      <TwitchEmbed
        channel="egbontobex"
        id="twitch-embed"
        darkMode={false}
        muted
        onVideoPause={() => console.log("Video paused")}
        width="100%"
        height="100%"
        withChat={false}
      />
    </div>
  );
}
