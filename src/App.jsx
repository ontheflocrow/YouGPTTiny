import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Header from './components/Header'
import ChatInterface from './components/ChatInterface'
import Sidebar from './components/Sidebar'
import WelcomeScreen from './components/WelcomeScreen'
import { TinyLlamaService } from './services/TinyLlamaService'

function App() {
  const [conversations, setConversations] = useState([])
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [modelStatus, setModelStatus] = useState('ready')
  const tinyLlamaService = useRef(new TinyLlamaService())

  useEffect(() => {
    // Initialize with a welcome conversation
    const welcomeConversation = {
      id: 'welcome',
      title: 'Welcome to YOUGPT',
      messages: [
        {
          id: '1',
          type: 'ai',
          content: "Hello! I'm YOUGPT, your collaborative AI partner powered by TinyLlama. I'm here to help you with questions, creative tasks, coding, and much more. How can I assist you today?",
          timestamp: new Date().toISOString()
        }
      ],
      createdAt: new Date().toISOString()
    }
    
    setConversations([welcomeConversation])
    setCurrentConversationId('welcome')
  }, [])

  const getCurrentConversation = () => {
    return conversations.find(conv => conv.id === currentConversationId)
  }

  const createNewConversation = () => {
    const newConversation = {
      id: Date.now().toString(),
      title: 'New Conversation',
      messages: [],
      createdAt: new Date().toISOString()
    }
    
    setConversations(prev => [newConversation, ...prev])
    setCurrentConversationId(newConversation.id)
    setSidebarOpen(false)
  }

  const deleteConversation = (conversationId) => {
    setConversations(prev => prev.filter(conv => conv.id !== conversationId))
    
    if (currentConversationId === conversationId) {
      const remaining = conversations.filter(conv => conv.id !== conversationId)
      setCurrentConversationId(remaining.length > 0 ? remaining[0].id : null)
    }
  }

  const sendMessage = async (content) => {
    if (!currentConversationId || isLoading) return

    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      content,
      timestamp: new Date().toISOString()
    }

    // Add user message
    setConversations(prev => prev.map(conv => 
      conv.id === currentConversationId 
        ? { 
            ...conv, 
            messages: [...conv.messages, userMessage],
            title: conv.messages.length === 0 ? content.slice(0, 30) + (content.length > 30 ? '...' : '') : conv.title
          }
        : conv
    ))

    setIsLoading(true)
    setModelStatus('thinking')

    try {
      // Get AI response from TinyLlama service
      const aiResponse = await tinyLlamaService.current.generateResponse(content, getCurrentConversation()?.messages || [])
      
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: aiResponse,
        timestamp: new Date().toISOString()
      }

      // Add AI response
      setConversations(prev => prev.map(conv => 
        conv.id === currentConversationId 
          ? { ...conv, messages: [...conv.messages, aiMessage] }
          : conv
      ))
    } catch (error) {
      console.error('Error generating response:', error)
      
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: "I apologize, but I'm having trouble processing your request right now. Please try again in a moment.",
        timestamp: new Date().toISOString()
      }

      setConversations(prev => prev.map(conv => 
        conv.id === currentConversationId 
          ? { ...conv, messages: [...conv.messages, errorMessage] }
          : conv
      ))
    } finally {
      setIsLoading(false)
      setModelStatus('ready')
    }
  }

  const currentConversation = getCurrentConversation()

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <AnimatePresence>
        {sidebarOpen && (
          <Sidebar
            conversations={conversations}
            currentConversationId={currentConversationId}
            onSelectConversation={setCurrentConversationId}
            onNewConversation={createNewConversation}
            onDeleteConversation={deleteConversation}
            onClose={() => setSidebarOpen(false)}
          />
        )}
      </AnimatePresence>

      <div className="flex-1 flex flex-col">
        <Header 
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          modelStatus={modelStatus}
          conversationTitle={currentConversation?.title}
        />
        
        <main className="flex-1 overflow-hidden">
          {currentConversation ? (
            <ChatInterface
              conversation={currentConversation}
              onSendMessage={sendMessage}
              isLoading={isLoading}
            />
          ) : (
            <WelcomeScreen onNewConversation={createNewConversation} />
          )}
        </main>
      </div>
    </div>
  )
}

export default App