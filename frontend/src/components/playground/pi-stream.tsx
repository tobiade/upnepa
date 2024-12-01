import { useEffect } from "react";

export const PiStream = () => {
    useEffect(() => {
        // Initialize WebSocket connection
        const host = process.env.REACT_APP_LIVE_STREAM_URL;
        if (!host) {
            console.error("LIVE_STREAM_URL environment variable is not set");
            return;
        }
        const socket = new WebSocket(host);  
        const imageElement: HTMLImageElement = document.getElementById('vid') as HTMLImageElement; 
  
        socket.onopen = function(event) {  
            console.log('Connected to the WebSocket server.');  
        };  
  
        socket.onmessage = function(event) {  
            const imgBlob = new Blob([event.data], { type: 'image/jpeg' });  
            const imgUrl = URL.createObjectURL(imgBlob);  
            imageElement.src = imgUrl;  
        };  
  
        socket.onerror = function(error) {  
            console.error('WebSocket Error:', error);  
        };  
  
        socket.onclose = function(event) {  
            console.log('Disconnected from the WebSocket server.');  
        };  
    })

  return (
    <div className="flex-1 rounded-lg overflow-hidden shadow-lg"><img id="vid" /></div>
  )
}