import asyncio
from backend.redis_client import RedisClient

async def test():
    rc = RedisClient()
    await rc.connect()
    print("Connected:", rc.is_connected())
    
    # Test set
    await rc.set_state("test_key", {"status": "ok", "value": 42})
    
    # Test get
    result = await rc.get_state("test_key")
    print("Get state:", result)
    
    # Test delete
    await rc.delete_state("test_key")
    after = await rc.get_state("test_key")
    print("After delete:", after)

asyncio.run(test())
