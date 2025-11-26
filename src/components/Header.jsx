import React from 'react'

function Header() {
  return (
    <header className="text-center py-16 px-4">
      <img
        src="https://files.catbox.moe/01m1w1.jpg"
        alt="Admin Alert Bot Logo"
        className="w-36 h-36 rounded-full border-4 border-accent mx-auto animate-float"
        style={{ boxShadow: '0 0 30px rgba(0, 188, 212, 0.4)' }}
      />
      <h1 className="text-4xl font-bold mt-4 text-accent">
        Admin Alert (@NovaMentionBot)
      </h1>
      <p className="text-lg text-subtext mt-2">
        Your smart Telegram assistant for notifying group admins instantly 🚨
      </p>
    </header>
  )
}

export default Header
