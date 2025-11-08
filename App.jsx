import React, {useEffect, useState, useRef} from 'react'
import axios from 'axios'
import { Line } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js'
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

export default function App(){
    const [ticks, setTicks] = useState([])
    const wsRef = useRef(null)

    useEffect(()=>{
        // fetch sample ticks from backend
        axios.get('/api/sample-ticks').then(r=> setTicks(r.data.ticks || []))
        // open websocket for live simulated ticks
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
        const wsUrl = `${protocol}://${window.location.host}/ws/ticks/SAMPLE`
        wsRef.current = new WebSocket(wsUrl)
        wsRef.current.onmessage = (evt) => {
            const d = JSON.parse(evt.data)
            setTicks(t=> [...t.slice(-199), {ts: d.ts, price: d.price}])
        }
        return ()=> wsRef.current && wsRef.current.close()
    },[])

    const data = {
        labels: ticks.map(t=> new Date(t.ts).toLocaleTimeString()),
        datasets: [{label:'SAMPLE', data: ticks.map(t=> t.price), tension:0.2}]
    }

    return (
        <div style={{fontFamily:'Inter, system-ui, sans-serif', padding:20}}>
            <h1>PSX Trader — Starter</h1>
            <p>A developer scaffold: FastAPI backend + React frontend. Replace the simulated feed with real PSX data and broker integration.</p>
            <div style={{maxWidth:900}}>
                <Line data={data} />
            </div>
        </div>
    )
}
