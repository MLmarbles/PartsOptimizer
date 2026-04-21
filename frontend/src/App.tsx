import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import BuildPage from './pages/BuildPage'
import FaqPage from './pages/FaqPage'
import FpsEstimatorPage from './pages/FpsEstimatorPage'

function App() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <div className="pt-16">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/build" element={<BuildPage />} />
          <Route path="/faq" element={<FaqPage />} />
          <Route path="/fps-estimator" element={<FpsEstimatorPage />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
