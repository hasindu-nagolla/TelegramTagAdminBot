import React from 'react'

function HowItWorks() {
  return (
    <section className="max-w-4xl mx-auto my-8 bg-card rounded-2xl p-8 shadow-lg transition-transform duration-300 hover:-translate-y-1"
      style={{ boxShadow: '0 0 40px rgba(0, 188, 212, 0.15)' }}>
      
      <h2 className="text-accent text-2xl font-semibold mb-4">
        ⚙️ How It Works
      </h2>
      <p className="leading-relaxed mb-6">
        Whenever a user types <code className="bg-hover px-2 py-1 rounded">@admin</code> followed by a message, the bot scans, cleans, and sends a formatted report to the chat tagging all active admins.
      </p>

      <div className="text-center">
        <a
          href="https://t.me/AtzioBot"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block bg-accent text-black font-semibold py-3 px-8 rounded-full transition-all duration-300 hover:bg-[#00acc1] hover:-translate-y-0.5 hover:shadow-lg"
          style={{ boxShadow: '0 0 15px rgba(0, 188, 212, 0.3)' }}
        >
          ✨ Try Admin Alert Now
        </a>
      </div>
    </section>
  )
}

export default HowItWorks
