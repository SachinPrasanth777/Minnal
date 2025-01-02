import { toast } from "@/hooks/use-toast"

export function showNotification(message: string, type: 'default' | 'success' | 'error' = 'default') {
  toast({
    description: message,
    variant: type === 'error' ? 'destructive' : 'default',
    duration: 3000,
  })
}

