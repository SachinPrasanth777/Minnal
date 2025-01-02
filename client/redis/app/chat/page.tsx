'use client'

import { useEffect, useState } from 'react'
import { io, Socket } from 'socket.io-client'
import { MessageList } from '@/components/chat/message-list'
import { RoomList } from '@/components/chat/room-list'
import { MessageInput } from '@/components/chat/message-input'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

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
  const [socket, setSocket] = useState<Socket | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [rooms, setRooms] = useState<Room[]>([
    { id: '1', name: 'General', active: true },
    { id: '2', name: 'Random', active: false }
  ])
  const [currentRoom, setCurrentRoom] = useState('')
  const [newRoomName, setNewRoomName] = useState('')
  const [username, setUsername] = useState('User' + Math.floor(Math.random() * 1000))

  useEffect(() => {
    const newSocket = io('http://localhost:8000', {
      path: '/socket.io'
    })

    newSocket.on('connect', () => {
      console.log('Connected to server')
    })

    newSocket.on('welcome', (data) => {
      addMessage({
        id: Date.now().toString(),
        user: 'System',
        message: data.data,
        timestamp: new Date()
      })
    })

    newSocket.on('joined', (data) => {
      addMessage({
        id: Date.now().toString(),
        user: 'System',
        message: `Joined room: ${data.room}`,
        timestamp: new Date()
      })
    })

    newSocket.on('message', (data) => {
      addMessage({
        id: Date.now().toString(),
        user: data.user || 'Anonymous',
        message: data.message,
        timestamp: new Date()
      })
    })

    setSocket(newSocket)

    return () => {
      newSocket.close()
    }
  }, [])

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
        user: username
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
    }
  }

  return (
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
        <MessageList messages={messages} />
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={!currentRoom}
        />
      </div>
    </div>
  )
}

