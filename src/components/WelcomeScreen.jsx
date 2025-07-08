import React from 'react'
import { motion } from 'framer-motion'
import { MessageSquare, Zap, Code, Lightbulb, BookOpen, Sparkles } from 'lucide-react'

const WelcomeScreen = ({ onNewConversation }) => {
  const features = [
    {
      icon: MessageSquare,
      title: 'Natural Conversations',
      description: 'Chat naturally with AI powered by TinyLlama'
    },
    {
      icon: Code,
      title: 'Code Assistance',
      description: 'Get help with programming and technical questions'
    },
    {
      icon: Lightbulb,
      title: 'Creative Ideas',
      description: 'Brainstorm and explore creative solutions'
    },
    {
      icon: BookOpen,
      title: 'Learning Support',
      description: 'Learn new concepts and get explanations'
    }
  ]

  const examplePrompts = [
    "Explain quantum computing in simple terms",
    "Help me write a Python function to sort a list",
    "What are some creative writing prompts?",
    "How do I start learning web development?"
  ]

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center justify-center mb-6">
            <div className="w-16 h-16 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center">
              <Zap className="w-8 h-8 text-white" />
            </div>
          </div>
          
          <h1 className="text-4xl font-bold text-slate-900 mb-4">
            Welcome to YOUGPT
          </h1>
          
          <p className="text-xl text-slate-600 mb-8 max-w-2xl mx-auto">
            Your collaborative AI partner powered by TinyLlama. Ready to help you with questions, 
            creative tasks, coding, and much more.
          </p>

          <motion.button
            onClick={onNewConversation}
            className="inline-flex items-center space-x-2 px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-xl font-medium transition-colors shadow-lg"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Sparkles className="w-5 h-5" />
            <span>Start Conversation</span>
          </motion.button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-16"
        >
          <h2 className="text-2xl font-semibold text-slate-900 mb-8">
            What can I help you with?
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
                className="glass-effect p-6 rounded-xl text-center hover:shadow-lg transition-shadow"
              >
                <feature.icon className="w-8 h-8 text-primary-500 mx-auto mb-4" />
                <h3 className="font-semibold text-slate-900 mb-2">{feature.title}</h3>
                <p className="text-sm text-slate-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>

          <div className="glass-effect p-6 rounded-xl">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              Try these example prompts:
            </h3>
            <div className="grid md:grid-cols-2 gap-3">
              {examplePrompts.map((prompt, index) => (
                <motion.button
                  key={index}
                  onClick={() => {
                    onNewConversation()
                    // You could auto-fill the input with this prompt
                  }}
                  className="text-left p-3 bg-white/50 hover:bg-white/80 rounded-lg transition-colors text-sm text-slate-700"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  "{prompt}"
                </motion.button>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default WelcomeScreen