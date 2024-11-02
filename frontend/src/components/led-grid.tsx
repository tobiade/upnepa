'use client'

import { useEffect, useRef, useState } from 'react'

export default function LEDGrid() {
  const [ledStates, setLedStates] = useState(Array(64).fill(false))
  const videoRef = useRef<HTMLVideoElement>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    // Initialize WebSocket connection
    wsRef.current = new WebSocket('ws://192.168.0.225:8765')

    wsRef.current.onopen = () => {
      console.log('WebSocket connection established')
    }

    wsRef.current.onmessage = (event) => {
      const data: { ledStates?: { on?: { [key: string]: number[] }, off?: { [key: string]: number[] } } } = JSON.parse(event.data)
      if (data.ledStates && data.ledStates.on) {
        setLedStates(() => {
          const updatedLedStates = Array(64).fill(false)
          if (data.ledStates?.on) {
            Object.entries(data.ledStates.on).forEach(([column, rows]) => {
              (rows as number[]).forEach((row) => {
                const index = parseInt(column) + row * 8
                updatedLedStates[index] = true
              })
            })
          }
          return updatedLedStates
        })
      }
    }

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    wsRef.current.onclose = () => {
      console.log('WebSocket connection closed')
    }

    // Set up video stream
    if (videoRef.current) {
      videoRef.current.src = 'https://example.com/led-grid-stream' // Replace with actual stream URL
    }

    // Clean up WebSocket connection on component unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  const toggleLED = (index: number) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      setLedStates((prevStates) => {
        const updatedLedStates = [...prevStates]
        updatedLedStates[index] = !updatedLedStates[index]

        const column = index % 8
        const row = Math.floor(index / 8)
        const state = updatedLedStates[index] ? 'on' : 'off'

        const ledStatesJson = {
          ledStates: {
            [state]: {
              [column]: [row]
            }
          }
        }

        wsRef.current?.send(JSON.stringify(ledStatesJson))
        return updatedLedStates
      })
    } else {
      console.error('WebSocket is not connected')
    }
    console.log('Toggled LED at index:', index)
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-8">LED Grid Controller</h1>
      <div className="flex flex-col md:flex-row gap-8 w-full max-w-4xl">
        <div className="flex-1">
          <h2 className="text-xl font-semibold mb-4">Interactive LED Grid</h2>
          <div className="aspect-square bg-black rounded-lg overflow-hidden shadow-lg">
            <svg
              className="w-full h-full"
              viewBox="0 0 8 8"
              xmlns="http://www.w3.org/2000/svg"
            >
              {ledStates.map((isOn, index) => (
                <rect
                  key={index}
                  x={index % 8}
                  y={Math.floor(index / 8)}
                  width="1"
                  height="1"
                  fill={isOn ? 'rgba(255, 0, 0, 0.5)' : 'rgba(255, 255, 255, 0.1)'}
                  stroke="rgba(255, 255, 255, 0.2)"
                  strokeWidth="0.05"
                  className="cursor-pointer transition-colors duration-200"
                  onClick={() => toggleLED(index)}
                />
              ))}
            </svg>
          </div>
          <p className="mt-4 text-gray-600 text-center">Click on the grid to toggle LEDs red</p>
        </div>
        <div className="flex-1">
          <h2 className="text-xl font-semibold mb-4">Live Video Stream</h2>
          <div className="aspect-square bg-black rounded-lg overflow-hidden shadow-lg">
            <video
              ref={videoRef}
              className="w-full h-full object-cover"
              autoPlay
              muted
              loop
              playsInline
            />
          </div>
          <p className="mt-4 text-gray-600 text-center">Live feed of the LED grid</p>
        </div>
      </div>
    </div>
  )
}
