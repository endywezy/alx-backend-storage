
Curriculum
Short Specializations
Average: 130.6%
You just released the advanced tasks of this project. Have fun!
0x02. Redis basic
Back-end
Redis
 Weight: 1
 Project will start Aug 14, 2024 6:00 AM, must end by Aug 15, 2024 6:00 AM
 Checker will be released at Aug 14, 2024 12:00 PM
 An auto review will be launched at the deadline


Resources
Read or watch:

Redis Crash Course Tutorial
Redis commands
Redis python client
How to Use Redis With Python
Learning Objectives
Learn how to use redis for basic operations
Learn how to use redis as a simple cache
Requirements
All of your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
All of your files should end with a new line
A README.md file, at the root of the folder of the project, is mandatory
The first line of all your files should be exactly #!/usr/bin/env python3
Your code should use the pycodestyle style (version 2.5)
All your modules should have documentation (python3 -c 'print(__import__("my_module").__doc__)')
All your classes should have documentation (python3 -c 'print(__import__("my_module").MyClass.__doc__)')
All your functions and methods should have documentation (python3 -c 'print(__import__("my_module").my_function.__doc__)' and python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)')
A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)
All your functions and coroutines must be type-annotated.
Install Redis on Ubuntu 18.04
$ sudo apt-get -y install redis-server
$ pip3 install redis
$ sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
Use Redis in a container
Redis server is stopped by default - when you are starting a container, you should start it with: service redis-server start

Tasks
0. Writing strings to Redis
mandatory
Create a Cache class. In the __init__ method, store an instance of the Redis client as a private variable named _redis (using redis.Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string. The method should generate a random key (e.g. using uuid), store the input data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str, bytes, int or float.

bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

bob@dylan:~$ python3 main.py 
3a3e8231-b2f6-450d-8b0e-0f38f16e8ca2
b'hello'
bob@dylan:~$ 
Repo:

GitHub repository: alx-backend-storage
Directory: 0x02-redis_basic
File: exercise.py
 
1. Reading from Redis and recovering original type
mandatory
Redis only allows to store string, bytes and numbers (and lists thereof). Whatever you store as single elements, it will be returned as a byte string. Hence if you store "a" as a UTF-8 string, it will be returned as b"a" when retrieved from the server.

In this exercise we will create a get method that take a key string argument and an optional Callable argument named fn. This callable will be used to convert the data back to the desired format.

Remember to conserve the original Redis.get behavior if the key does not exist.

Also, implement 2 new methods: get_str and get_int that will automatically parametrize Cache.get with the correct conversion function.

The following code should not raise:

cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
Repo:

GitHub repository: alx-backend-storage
Directory: 0x02-redis_basic
File: exercise.py
 
2. Incrementing values
mandatory
Familiarize yourself with the INCR command and its python equivalent.

In this task, we will implement a system to count how many times methods of the Cache class are called.

Above Cache define a count_calls decorator that takes a single method Callable argument and returns a Callable.

As a key, use the qualified name of method using the __qualname__ dunder method.

Create and return function that increments the count for that key every time the method is called and returns the value returned by the original method.

Remember that the first argument of the wrapped function will be self which is the instance itself, which lets you access the Redis instance.

Protip: when defining a decorator it is useful to use functool.wraps to conserve the original function’s name, docstring, etc. Make sure you use it as described here.

Decorate Cache.store with count_calls.

bob@dylan:~$ cat main.py
#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))

bob@dylan:~$ ./main.py
b'1'
b'3'
bob@dylan:~$ 
Repo:

GitHub repository: alx-backend-storage
Directory: 0x02-redis_basic
File: exercise.py
 
3. Storing lists
mandatory
Familiarize yourself with redis commands RPUSH, LPUSH, LRANGE, etc.

In this task, we will define a call_history decorator to store the history of inputs and outputs for a particular function.

Everytime the original function will be called, we will add its input parameters to one list in redis, and store its output into another list.

In call_history, use the decorated function’s qualified name and append ":inputs" and ":outputs" to create input and output list keys, respectively.

call_history has a single parameter named method that is a Callable and returns a Callable.

In the new function that the decorator will return, use rpush to append the input arguments. Remember that Redis can only store strings, bytes and numbers. Therefore, we can simply use str(args) to normalize. We can ignore potential kwargs for now.

Execute the wrapped function to retrieve the output. Store the output using rpush in the "...:outputs" list, then return the output.

Decorate Cache.store with call_history.

bob@dylan:~$ cat main.py
#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

bob@dylan:~$ ./main.py
04f8dcaa-d354-4221-87f3-4923393a25ad
a160a8a8-06dc-4934-8e95-df0cb839644b
15a8fd87-1f55-4059-86aa-9d1a0d4f2aea
inputs: [b"('first',)", b"('secont',)", b"('third',)"]
outputs: [b'04f8dcaa-d354-4221-87f3-4923393a25ad', b'a160a8a8-06dc-4934-8e95-df0cb839644b', b'15a8fd87-1f55-4059-86aa-9d1a0d4f2aea']
bob@dylan:~$ 
Repo:

GitHub repository: alx-backend-storage
Directory: 0x02-redis_basic
File: exercise.py
 
4. Retrieving lists
mandatory
In this tasks, we will implement a replay function to display the history of calls of a particular function.

Use keys generated in previous tasks to generate the following output:

>>> cache = Cache()
>>> cache.store("foo")
>>> cache.store("bar")
>>> cache.store(42)
>>> replay(cache.store)
Cache.store was called 3 times:
Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20
Tip: use lrange and zip to loop over inputs and outputs.

Repo:

GitHub repository: alx-backend-storage
Directory: 0x02-redis_basic
File: exercise.py
 
5. Implementing an expiring web cache and tracker
#advanced
In this tasks, we will implement a get_page function (prototype: def get_page(url: str) -> str:). The core of the function is very simple. It uses the requests module to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code written in exercise.py.

Inside get_page track how many times a particular URL was accessed in the key "count:{url}" and cache the result with an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response and test your caching.

Bonus: implement this use case with decorators.

Repo:

GitHub repository: alx-backend-storage
Directory: 0x02-redis_basic
File: web.py
 
Copyright © 2024 ALX, All rights reserved.


Chat

New Conversation

🤓 Explain a complex thing

Explain Artificial Intelligence so that I can explain it to my six-year-old child.


🧠 Get suggestions and create new ideas

Please give me the best 10 travel ideas around the world


💭 Translate, summarize, fix grammar and more…

Translate "I love you into" French


GPT-3.5
Hello, how can I help you today?

Please explain in English: "Create a function named cleanSet that returns a string of all the set values that start with a specific string (startString).

It accepts two arguments: a set (Set) and a startString (String).

When a value starts with startString you only append the rest of the string. The string contains all the values of the set separated by -.

bob@dylan:~$ cat 8-main.js
import cleanSet from "./8-clean_set.js";

console.log(cleanSet(new Set(['bonjovi', 'bonaparte', 'bonappetit', 'banana']), 'bon'));
console.log(cleanSet(new Set(['bonjovi', 'bonaparte', 'bonappetit', 'banana']), ''));

bob@dylan:~$ 
bob@dylan:~$ npm run dev 8-main.js 
jovi-aparte-appetit

bob@dylan:~$"
GPT-3.5
The given code is creating a function called cleanSet that takes in a Set and a startString as arguments. This function will return a string containing all the values from the set that start with the specified startString. If no startString is provided, it will return all the values from the set.

In this example, when cleanSet is called with a set containing ['bonjovi', 'bonaparte', 'bonappetit', 'banana'] and a startString of 'bon', it will return "jovi-aparte-appetit" because those are the values in the set that start with "bon".

When cleanSet is called without a specific startString, it will return all the values in the set separated by '-'.

logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd54') }
2024-08-13T23:29:22.332+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd55') }
2024-08-13T23:29:22.332+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd56') }
2024-08-13T23:29:22.332+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd57') }
2024-08-13T23:29:22.332+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd58') }
2024-08-13T23:29:22.332+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd59') }
2024-08-13T23:29:22.332+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd5a') }
2024-08-13T23:29:22.332+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd5b') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd5c') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd5d') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd5e') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd5f') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd60') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd61') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd62') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd63') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd64') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd65') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd66') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd67') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd68') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd69') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd6a') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd6b') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd6c') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd6d') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd6e') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd6f') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd70') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd71') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd72') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd73') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd74') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd75') }
2024-08-13T23:29:22.333+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd76') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd77') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd78') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd79') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd7a') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd7b') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd7c') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd7d') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd7e') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd7f') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd80') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd81') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd82') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd83') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd84') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd85') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd86') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd87') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd88') }
2024-08-13T23:29:22.334+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd89') }
2024-08-13T23:29:22.339+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd8a') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd8b') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd8c') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd8d') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd8e') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd8f') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd90') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd91') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd92') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd93') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd94') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd95') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd96') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd97') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd98') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd99') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd9a') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd9b') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd9c') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd9d') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd9e') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bd9f') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda0') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda1') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda2') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda3') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda4') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda5') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda6') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda7') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda8') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bda9') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdaa') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdab') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdac') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdad') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdae') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdaf') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb0') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb1') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb2') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb3') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb4') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb5') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb6') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb7') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb8') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdb9') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdba') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdbb') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdbc') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdbd') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdbe') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdbf') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc0') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc1') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc2') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc3') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc4') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc5') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc6') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc7') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc8') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdc9') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdca') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdcb') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdcc') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdcd') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdce') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdcf') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd0') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd1') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd2') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd3') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd4') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd5') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd6') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd7') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd8') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdd9') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdda') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bddb') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bddc') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bddd') }
2024-08-13T23:29:22.340+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdde') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bddf') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde0') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde1') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde2') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde3') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde4') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde5') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde6') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde7') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde8') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bde9') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdea') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdeb') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdec') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bded') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdee') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdef') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf0') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf1') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf2') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf3') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf4') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf5') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf6') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf7') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf8') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdf9') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdfa') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdfb') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdfc') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdfd') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdfe') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bdff') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be00') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be01') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be02') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be03') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be04') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be05') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be06') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be07') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be08') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be09') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be0a') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be0b') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be0c') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be0d') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be0e') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be0f') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be10') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be11') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be12') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be13') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be14') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be15') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be16') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be17') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be18') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be19') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be1a') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be1b') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be1c') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be1d') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be1e') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be1f') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be20') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be21') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be22') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be23') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be24') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be25') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be26') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be27') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be28') }
2024-08-13T23:29:22.341+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be29') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be2a') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be2b') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be2c') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be2d') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be2e') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be2f') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be30') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be31') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be32') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be33') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be34') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be35') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be36') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be37') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be38') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be39') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be3a') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be3b') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be3c') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be3d') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be3e') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be3f') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be40') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be41') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be42') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be43') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be44') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be45') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be46') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be47') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be48') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be49') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be4a') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be4b') }
2024-08-13T23:29:22.342+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be4c') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be4d') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be4e') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be4f') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be50') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be51') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be52') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be53') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be54') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be55') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be56') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be57') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be58') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be59') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be5a') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be5b') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be5c') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be5d') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be5e') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be5f') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be60') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be61') }
2024-08-13T23:29:22.344+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be62') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be63') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be64') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be65') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be66') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be67') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be68') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be69') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be6a') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be6b') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be6c') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be6d') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be6e') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be6f') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be70') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be71') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be72') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be73') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be74') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be75') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be76') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be77') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be78') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be79') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be7a') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be7b') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be7c') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be7d') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be7e') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be7f') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be80') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be81') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be82') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be83') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be84') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be85') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be86') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be87') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be88') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be89') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be8a') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be8b') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be8c') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be8d') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be8e') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be8f') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be90') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be91') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be92') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be93') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be94') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be95') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be96') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be97') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be98') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be99') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be9a') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be9b') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be9c') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be9d') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be9e') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269be9f') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea0') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea1') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea2') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea3') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea4') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea5') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea6') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea7') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea8') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bea9') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beaa') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beab') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beac') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bead') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beae') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beaf') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb0') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb1') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb2') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb3') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb4') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb5') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb6') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb7') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb8') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beb9') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beba') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bebb') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bebc') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bebd') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bebe') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bebf') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec0') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec1') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec2') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec3') }
2024-08-13T23:29:22.352+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec4') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec5') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec6') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec7') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec8') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bec9') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beca') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269becb') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269becc') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269becd') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bece') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269becf') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed0') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed1') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed2') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed3') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed4') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed5') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed6') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed7') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed8') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bed9') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beda') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bedb') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bedc') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bedd') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bede') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bedf') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee0') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee1') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee2') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee3') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee4') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee5') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee6') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee7') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee8') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bee9') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beea') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beeb') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beec') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beed') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beee') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beef') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef0') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef1') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef2') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef3') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef4') }
2024-08-13T23:29:22.353+0100    [########################]  logs.nginx  13.4MB/13.4MB  (100.0%)
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef5') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef6') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef7') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef8') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bef9') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269befa') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269befb') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269befc') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269befd') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269befe') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269beff') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf00') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf01') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf02') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf03') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf04') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf05') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf06') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf07') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf08') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf09') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf0a') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf0b') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf0c') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf0d') }
2024-08-13T23:29:22.353+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf0e') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf0f') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf10') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf11') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf12') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf13') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf14') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf15') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf16') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf17') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf18') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf19') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf1a') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf1b') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf1c') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf1d') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf1e') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf1f') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf20') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf21') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf22') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf23') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf24') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf25') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf26') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf27') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf28') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf29') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf2a') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf2b') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf2c') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf2d') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf2e') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf2f') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf30') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf31') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf32') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf33') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf34') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf35') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf36') }
2024-08-13T23:29:22.354+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf37') }
2024-08-13T23:29:22.355+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf38') }
2024-08-13T23:29:22.355+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf39') }
2024-08-13T23:29:22.355+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf3a') }
2024-08-13T23:29:22.355+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf3b') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf3c') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf3d') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf3e') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf3f') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf40') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf41') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf42') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf43') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf44') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf45') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf46') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf47') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf48') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf49') }
2024-08-13T23:29:22.409+0100    continuing through error: E11000 duplicate key error collection: logs.nginx index: _id_ dup key: { _id: ObjectId('5a8faa0bd4321e185269bf4a') }
2024-08-13T23:29:22.409+0100    [########################]  logs.nginx  13.4MB/13.4MB  (100.0%)
2024-08-13T23:29:22.409+0100    no indexes to restore
2024-08-13T23:29:22.413+0100    finished restoring logs.nginx (0 documents, 94778 failures)
2024-08-13T23:29:22.414+0100    0 document(s) restored successfully. 94778 document(s) failed to restore.
GPT-3.5
The given log message is showing a series of duplicate key errors in the MongoDB collection "logs.nginx". Each error shows the index "_id_" with a duplicate key value for the field "_id" of type ObjectId. The errors continue to occur multiple times, indicating that there are multiple duplicated keys in the collection.

coin image
10
Upgrade



sudo apt-get -y install redis-server



Make a Review & Earn Credit ❤
Chat
Ask
Search
Write
Image
ChatPDF
Vision
Full Page
Invite & Earn


