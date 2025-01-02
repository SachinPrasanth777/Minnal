import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { format } from "date-fns"

interface Message {
  id: string
  user: string
  message: string
  timestamp: Date
}

interface MessageListProps {
  messages: Message[]
}

export function MessageList({ messages }: MessageListProps) {
  return (
    <ScrollArea className="h-[calc(100vh-180px)] p-4">
      <div className="space-y-4">
        {messages.map((message) => (
          <div key={message.id} className="flex items-start gap-3">
            <Avatar>
              <AvatarImage src={`https://avatar.vercel.sh/${message.user}.png`} />
              <AvatarFallback>{message.user[0]}</AvatarFallback>
            </Avatar>
            <div className="grid gap-1">
              <div className="flex items-center gap-2">
                <div className="font-semibold">{message.user}</div>
                <div className="text-xs text-muted-foreground">
                  {format(message.timestamp, 'HH:mm')}
                </div>
              </div>
              <div className="text-sm text-muted-foreground">
                {message.message}
              </div>
            </div>
          </div>
        ))}
      </div>
    </ScrollArea>
  )
}

