import aioredis


async def get_redis():
    # Create a Redis connection
    redis = await aioredis.create_redis_pool('redis://redis:6382/0')
    return redis


async def close_redis(redis):
    # Close the Redis connection
    redis.close()
    await redis.wait_closed()
