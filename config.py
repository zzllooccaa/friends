import redis

cache = redis.StrictRedis(host='localhost'
                          , port='6379', charset="utf-8",
                          decode_responses=True)
