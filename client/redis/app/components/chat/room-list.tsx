import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"

interface Room {
  id: string
  name: string
  active: boolean
}

interface RoomListProps {
  rooms: Room[]
  currentRoom: string
  onRoomSelect: (room: string) => void
}

export function RoomList({ rooms, currentRoom, onRoomSelect }: RoomListProps) {
  return (
    <ScrollArea className="h-[calc(100vh-100px)]">
      <div className="space-y-2 p-2">
        {rooms.map((room) => (
          <Button
            key={room.id}
            variant={currentRoom === room.name ? "secondary" : "ghost"}
            className="w-full justify-start"
            onClick={() => onRoomSelect(room.name)}
          >
            <div className="flex items-center gap-2">
              <div className={`h-2 w-2 rounded-full ${room.active ? 'bg-green-500' : 'bg-gray-300'}`} />
              {room.name}
            </div>
          </Button>
        ))}
      </div>
    </ScrollArea>
  )
}

