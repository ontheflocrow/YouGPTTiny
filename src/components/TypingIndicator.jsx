import React from 'react'
import { motion } from 'framer-motion'
import { Zap } from 'lucide-react'

const TypingIndicator = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-start space-x-3"
    >
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 text-white flex items-center justify-center">
        <Zap className="w-4 h-4" />
      </div>
      
      <div className="message-bubble ai-message">
        <div className="typing-indicator">
          <div 
            className="typing-dot" 
            style={{ '--delay': '0ms' }}
          />
          <div 
            className="typing-dot" 
            style={{ '--delay': '150ms' }}
          />
          <div 
            className="typing-dot" 
            style={{ '--delay': '300ms' }}
          />
        </div>
      </div>
    </motion.div>
  )
}

export default TypingIndicator