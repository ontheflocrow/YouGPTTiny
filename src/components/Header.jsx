import React from 'react'
import { motion } from 'framer-motion'
import { Menu, Zap, Circle } from 'lucide-react'

const Header = ({ onToggleSidebar, modelStatus, conversationTitle }) => {
  const getStatusColor = () => {
    switch (modelStatus) {
      case 'ready': return 'text-green-500'
      case 'thinking': return 'text-yellow-500'
      case 'error': return 'text-red-500'
      default: return 'text-gray-500'
    }
  }

  const getStatusText = () => {
    switch (modelStatus) {
      case 'ready': return 'Ready'
      case 'thinking': return 'Thinking...'
      case 'error': return 'Error'
      default: return 'Offline'
    }
  }

  return (
    <header className="glass-effect border-b border-white/20 px-4 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={onToggleSidebar}
            className="p-2 hover:bg-white/20 rounded-lg transition-colors"
          >
            <Menu className="w-5 h-5 text-slate-600" />
          </button>
          
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Zap className="w-4 h-4 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-semibold text-slate-900">YOUGPT</h1>
                <p className="text-xs text-slate-500">Powered by TinyLlama</p>
              </div>
            </div>
            
            {conversationTitle && (
              <div className="hidden md:block">
                <span className="text-slate-400">•</span>
                <span className="ml-2 text-sm text-slate-600 max-w-xs truncate">
                  {conversationTitle}
                </span>
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <motion.div
            animate={modelStatus === 'thinking' ? { scale: [1, 1.1, 1] } : {}}
            transition={{ repeat: Infinity, duration: 1 }}
          >
            <Circle className={`w-3 h-3 ${getStatusColor()} fill-current`} />
          </motion.div>
          <span className={`text-sm font-medium ${getStatusColor()}`}>
            {getStatusText()}
          </span>
        </div>
      </div>
    </header>
  )
}

export default Header