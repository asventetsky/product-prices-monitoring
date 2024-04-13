import { useState } from 'react'
import { AreaChart } from "./AreaChart";
import { data } from "./data/";
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>PRODUCT PRICES MONITORING</h1>
      <AreaChart data={data} width={1000} height={400} />
    </>
  )
}

export default App
