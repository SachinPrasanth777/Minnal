import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { format } from "date-fns"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  user: string
  message: string
  timestamp: Date
}

interface MessageListProps {
  messages: Message[]
  currentUser: string
}

export function MessageList({ messages, currentUser }: MessageListProps) {
  return (
    <ScrollArea className="flex-1 p-4">
      <div className="space-y-6">
        {messages.map((message) => {
          const isCurrentUser = message.user === currentUser
          
          return (
            <div 
              key={message.id} 
              className={cn(
                "flex items-end gap-2 max-w-[80%]",
                isCurrentUser ? "ml-auto flex-row-reverse" : ""
              )}
            >
              <Avatar className="h-8 w-8 flex-shrink-0">
                <AvatarImage src={`https://avatar.vercel.sh/${message.user}.png`} />
                <AvatarFallback>{message.user[0]}</AvatarFallback>
              </Avatar>
              
              <div className={cn(
                "flex flex-col gap-1",
                isCurrentUser ? "items-end" : "items-start"
              )}>
                <div className={cn(
                  "rounded-2xl px-4 py-2 text-sm",
                  isCurrentUser 
                    ? "bg-primary text-primary-foreground rounded-br-none" 
                    : "bg-muted rounded-bl-none"
                )}>
                  {message.message}
                </div>
                <span className="text-xs text-muted-foreground px-2">
                  {format(message.timestamp, 'HH:mm')}
                </span>
              </div>
            </div>
          )
        })}
      </div>
    </ScrollArea>
  )
}

