import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  return (
    <>
    <h1>Hola te animas a colaborar</h1>
    <p>Este proyecto esta en crecimiento</p>
    <p>Tus PRs para nosotros nos sirve de mucho apoyo!.</p>
    <a href="https://github.com/elimenit/SanTelmoChico" className="button">Enlace al Repositorio</a>
    </>
  )
}

export default App
