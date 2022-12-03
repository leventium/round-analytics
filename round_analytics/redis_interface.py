import aioredis


class RedisStorage:
    @classmethod
    async def create(cls, connstring: str) -> RedisStorage:
        obj = cls()
        obj.redis = aioredis.from_url(connstring, decode_responses=True)
        await obj.redis.setnx("user_id_counter", 0)
        return obj
    
    async def close(self):
        await self.redis.close()
    
    async def get_inviters(self) -> list[str]:
        return await self.redis.lrange("inviters", 0, -1)
    
    async def put_inviter(self, inviter: str) -> None:
        inviter = inviter.lower()
        if inviter not in (await self.get_inviters()):
            await self.redis.rpush("inviters", inviter.lower())

    async def check_inviter(self, inviter: str) -> bool:
        inviter = inviter.lower()
        return inviter in (await self.get_inviters())
    
    async def __increase(self, map: str, inviter: str) -> None:
        inviter = inviter.lower()
        count = await self.redis.hget(map, inviter)
        if count is None:
            count = 0
        count = int(count) + 1
        await self.redis.hset(map, inviter, count)
    
    async def increase_visits(self, inviter: str) -> None:
        await self.__increase("visits", inviter)

    async def increase_downloads(self, inviter: str) -> None:
        await self.__increase("downloads", inviter)

    async def put_contact(self, inviter: str, name: str, contact: str) -> None:
        new_user_id = int(await self.redis.get("user_id_counter"))
        await self.redis.set("user_id_counter", new_user_id + 1)
        await self.redis.hset("user_name", new_user_id, name)
        await self.redis.hset("user_contact", new_user_id, contact)
        await self.redis.hset("user_inviter", new_user_id, inviter.lower())

    async def get_visit_stats(self) -> list[tuple]:
        """
        Returns list of tuplse in format [(inviter, visiters_count, downloaders_count)].
        Sorted by inviter.
        """
        result = []
        inviters = await self.get_inviters()
        for inviter in inviters:
            visits_count = await self.redis.hget("visits", inviter)
            downloads_count = await self.redis.hget("downloads", inviter)
            result.append((inviter, visits_count, downloads_count))
        return sorted(result, key=lambda inviter: inviter[0])

    async def get_contacts(self) -> list[tuple]:
        """
        Returns list of tuples in format [(name, contact, inviter)].
        Sorted by inviters.
        """
        result = []
        usernames = await self.redis.hgetall("user_name")
        for user_id, name in usernames.items():
            contact = await self.redis.hget("user_contact", user_id)
            inviter = await self.redis.hget("user_inviter", user_id)
            result.append((name, contact, inviter))
        return sorted(result, key=lambda user: user[2])
