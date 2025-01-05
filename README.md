<h1 align="center">⚡ Minnal</h1>

<div align="center">
  <p>A real-time chat application built with modern technologies</p>
</div>

## 🚀 Features

- Real-time messaging with WebSocket
- Room-based chat system
- User authentication
- Message history persistence
- Real-time notifications
- Responsive design
- Scalable architecture

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Static type checking
- **Tailwind CSS** - Utility-first CSS framework
- **Socket.IO Client** - Real-time client-server communication
- **Shadcn/UI** - Re-usable components

### Backend
- **FastAPI** - Modern Python web framework
- **Socket.IO** - Real-time bidirectional event-based communication
- **Prisma** - Next-generation ORM
- **PostgreSQL** - Primary database
- **Redis** - Caching and pub/sub messaging
- **Python 3.11** - Latest Python features
- **JWT** - Authentication mechanism

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 🏗️ Architecture

```mermaid
graph LR
    Client[Next.js Client] <--> WebSocket[Socket.IO]
    WebSocket <--> Server[FastAPI Server]
    Server <--> Redis[(Redis)]
    Server <--> DB[(PostgreSQL)]
```

## 🚦 Prerequisites

- Node.js 18+
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL
- Redis

## ⚙️ Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/minnal.git
cd minnal
```

2. Run the client
```bash
cd client && cd redis
npm install
npm run dev
```

3. Run the server
```bash
docker compose up --build
```

4. Format the code
```bash
black format .
```

## 🛫 Environment Setup

Create a `.env` file in the root directory:

```env
# Database Configuration
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_NAME=cache_db
DATABASE_URL=postgresql://${DB_USERNAME}:${DB_PASSWORD}@postgres:5432/${DB_NAME}?schema=public

# Cache Configuration
REDIS_URL=redis_cache

# Security
SECRET=your_secret_here
API_KEY=your_api_key_here
```

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Socket.IO Documentation](https://socket.io/docs/v4)
- [Prisma Documentation](https://www.prisma.io/docs)
