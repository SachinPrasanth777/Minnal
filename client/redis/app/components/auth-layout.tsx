import Image from 'next/image'

interface AuthLayoutProps {
  children: React.ReactNode
  title: string
  subtitle: string
}

export function AuthLayout({ children, title, subtitle }: AuthLayoutProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-6 space-y-4">
          <div className="flex justify-center">
            <Image
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-0KDQgzS6RFpdNDjQNyosYEpf7jZqcB.png"
              alt="Redis Logo"
              width={250}
              height={150}
              className="rounded-lg object-contain"
            />
          </div>
          <h2 className="text-2xl font-semibold text-center text-gray-800">{title}</h2>
          <p className="text-center text-gray-600">{subtitle}</p>
          {children}
        </div>
      </div>
    </div>
  )
}

