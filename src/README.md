# start rabbit
```
docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 -p 5672:5672 rabbitmq:3-management
```

# start nameko
```
nameko run level shotgun gateway
```

# curl to create level
```
curl "http://localhost:8000/level/robot.aa.1000?create=true"
```