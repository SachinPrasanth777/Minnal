'use client'

import { useEffect, useState } from 'react'
import { io, Socket } from 'socket.io-client'
import { MessageList } from '@/components/chat/message-list'
import { RoomList } from '@/components/chat/room-list'
import { MessageInput } from '@/components/chat/message-input'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { showNotification } from '@/lib/notifications'
import { ToastProvider } from '@/components/providers/toast-provider'
import { useRouter } from 'next/navigation'

interface Message {
  id: string
  user: string
  message: string
  timestamp: Date
}

interface Room {
  id: string
  name: string
  active: boolean
}

export default function ChatPage() {
  const router = useRouter()
  const [socket, setSocket] = useState<Socket | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [rooms, setRooms] = useState<Room[]>([
    { id: '1', name: 'General', active: true },
    { id: '2', name: 'Random', active: false }
  ])
  const [currentRoom, setCurrentRoom] = useState('')
  const [newRoomName, setNewRoomName] = useState('')
  const [currentUser, setCurrentUser] = useState('')

  useEffect(() => {
    const token = localStorage.getItem('token')
    
    if (!token) {
      router.push('/login')
      return
    }

    const newSocket = io('http://localhost:8000', {
      path: '/socket.io',
      extraHeaders: {
        Authorization: `Bearer ${token}`
      }
    })

    newSocket.on('connect', () => {
      showNotification('Connected to server', 'success')
    })

    newSocket.on('connect_error', (error) => {
      if (error.message === 'No token provided' || error.message.includes('unauthorized')) {
        showNotification('Authentication failed', 'error')
        router.push('/login')
      } else {
        showNotification('Failed to connect to server', 'error')
      }
    })

    newSocket.on('disconnect', () => {
      showNotification('Disconnected from server', 'error')
    })

    newSocket.on('welcome', (data) => {
      // Extract email from welcome message and set as current user
      const email = data.data.split(' ')[1].replace('!', '')
      setCurrentUser(email)
      showNotification(data.data)
    })

    newSocket.on('joined', (data) => {
      showNotification(`Joined room: ${data.room}`, 'success')
    })

    newSocket.on('message', (data) => {
      if (data.user !== 'System') {
        addMessage({
          id: Date.now().toString(),
          user: data.user || 'Anonymous',
          message: data.message || data.content,
          timestamp: new Date(data.timestamp || Date.now())
        })
      }
    })

    setSocket(newSocket)

    return () => {
      newSocket.close()
    }
  }, [router])

  const addMessage = (message: Message) => {
    setMessages(prev => [...prev, message])
  }

  const handleRoomSelect = (room: string) => {
    if (socket && room) {
      socket.emit('join_room', { room })
      setCurrentRoom(room)
      setMessages([])
    }
  }

  const handleSendMessage = (message: string) => {
    if (socket && currentRoom && message) {
      socket.emit('chat_message', {
        room: currentRoom,
        message,
        user: currentUser
      })
    }
  }

  const handleCreateRoom = () => {
    if (newRoomName.trim()) {
      const newRoom = {
        id: Date.now().toString(),
        name: newRoomName,
        active: true
      }
      setRooms(prev => [...prev, newRoom])
      setNewRoomName('')
      handleRoomSelect(newRoom.name)
      showNotification(`Created new room: ${newRoom.name}`, 'success')
    }
  }

  return (
    <>
      <ToastProvider />
      <div className="flex h-screen">
        {/* Sidebar */}
        <div className="w-64 border-r bg-gray-50/50">
          <div className="p-4 border-b">
            <Dialog>
              <DialogTrigger asChild>
                <Button className="w-full">Create Room</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Create a new room</DialogTitle>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <Input
                    value={newRoomName}
                    onChange={(e) => setNewRoomName(e.target.value)}
                    placeholder="Enter room name"
                  />
                  <Button onClick={handleCreateRoom}>Create</Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>
          <RoomList
            rooms={rooms}
            currentRoom={currentRoom}
            onRoomSelect={handleRoomSelect}
          />
        </div>

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          <div className="p-4 border-b">
            <h2 className="text-xl font-semibold">{currentRoom || 'Select a room'}</h2>
          </div>
          <MessageList 
            messages={messages} 
            currentUser={currentUser}
          />
          <MessageInput
            onSendMessage={handleSendMessage}
            disabled={!currentRoom}
          />
        </div>
      </div>
    </>
  )
}

