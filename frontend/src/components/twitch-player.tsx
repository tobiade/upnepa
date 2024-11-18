import { TwitchEmbed } from "react-twitch-embed";

export default function TwitchStream() {
  return (
    <div>
      <TwitchEmbed
        channel="egbontobex"
        id="twitch-embed"
        darkMode={false}
        muted
        onVideoPause={() => console.log("Video paused")}
        width="100%"
        height={480}
      />
    </div>
  );
}
