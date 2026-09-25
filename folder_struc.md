# folder strucure 
## hella wip

keltasyke - root

> backend
    > app
        > alerts
            > routes.py
        > telemetry
            > collector.py      # primary polling script for siri/vm
            > vm_cache.py       # in memory cache for siri/vm data
            > geocache.py       # if I had thought about debouncing logic, here is where I'd put it.       
        > preferences
            > routes.py         # CRUD against preference table in db
        > voice
            > routes.py         #
            > whisper_engine.py # waiting with this for now   
        > ws
            > busses.py         # primary route and connection management happens in here
        > reference
            > local_cache.py    # in memory cache of stops/routes/trips loaded from local db
    > config.py
    > db.py                     # Primary psql connection pool
    > main.py
> migrate

> data
    > static