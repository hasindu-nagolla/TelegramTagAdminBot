import React from 'react'

function Footer() {
  return (
    <footer className="text-center py-8 text-subtext border-t border-hover mt-12 bg-gradient-to-b from-transparent to-[#0a0a0c]">
      <p>
        © 2025 Admin Alert Bot by{' '}
        <a
          href="https://github.com/hasindu-nagolla"
          target="_blank"
          rel="noopener noreferrer"
          className="text-accent hover:underline"
        >
          Hasindu
        </a>
        {' '}| Built with ❤️ & Code
      </p>
    </footer>
  )
}

export default Footer
