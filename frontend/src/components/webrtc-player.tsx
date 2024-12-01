
export const WebRTCPlayer = () => {
    const host = process.env.REACT_APP_WEBRTC_STREAM;
    if (!host) {
        throw("REACT_APP_WEBRTC_STREAM environment variable is not set");
    }
  return (
    <div className="flex flex-1 rounded-lg overflow-hidden shadow-lg"><iframe src={host} title="led-stream" className="flex-1"></iframe></div>
  )
}
