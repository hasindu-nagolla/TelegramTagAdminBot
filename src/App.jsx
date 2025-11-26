import React from 'react'
import Header from './components/Header'
import Features from './components/Features'
import HowItWorks from './components/HowItWorks'
import Footer from './components/Footer'

function App() {
  return (
    <div className="bg-bg text-text min-h-screen overflow-x-hidden">
      <Header />
      <Features />
      <HowItWorks />
      <Footer />
    </div>
  )
}

export default App
