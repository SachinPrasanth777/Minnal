from prisma import Prisma as PrismaClient


class Database:
    def __init__(self):
        self.prisma = PrismaClient()

    async def connect(self):
        await self.prisma.connect()

    async def disconnect(self):
        await self.prisma.disconnect()
