import React from 'react'

function Features() {
  const features = [
    'Instantly notifies all visible group administrators when triggered.',
    'Automatically filters out bots and anonymous admins.',
    'Prevents spam with context-sensitive warnings.',
    'Beautifully formatted replies with clean inline HTML styling.',
    'Color-coded terminal logs with Colorama for easy monitoring.',
  ]

  return (
    <section className="max-w-4xl mx-auto my-8 bg-card rounded-2xl p-8 shadow-lg transition-transform duration-300 hover:-translate-y-1"
      style={{ boxShadow: '0 0 40px rgba(0, 188, 212, 0.15)' }}>
      
      <div className="mb-8">
        <h2 className="text-accent text-2xl font-semibold mb-4">
          🚀 What is Admin Alert?
        </h2>
        <p className="leading-relaxed">
          <span className="font-semibold">Admin Alert</span> is a powerful Telegram bot designed to alert group administrators when someone reports or mentions issues using commands like <code className="bg-hover px-2 py-1 rounded">@admin</code>, <code className="bg-hover px-2 py-1 rounded">.admin</code>, or <code className="bg-hover px-2 py-1 rounded">/admin</code>. It ensures that admin notifications are delivered efficiently and professionally.
        </p>
      </div>

      <div>
        <h2 className="text-accent text-2xl font-semibold mb-4">
          ✨ Key Features
        </h2>
        <ul className="space-y-2">
          {features.map((feature, index) => (
            <li key={index} className="flex items-start">
              <span className="text-accent mr-2">•</span>
              <span>{feature}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}

export default Features
