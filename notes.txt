# data exploration

## SIRI VM - Vehicle Monitoring
http://data.foli.fi/siri/vm
Docs at: https://data.foli.fi/doc/siri/v0/vm-en
tldr: Provided data is not based on sole GPS acquired location but on backend systems educated guess based on vehicles odometer, it's GPS location, time spent after beginning of trip and/or previous stop, etc.


outputs json
Error looks like this: {"sys":"VM","status":"NO_SIRI_DATA","servertime":1433246350,"result":[]}
Pending looks like this: {"sys":"VM","status":"PENDING","servertime":1433246350,"result":[]}

sys	"VM" - Vehicle Monitoring 
status	"OK" - system status, check if OK.
servertime	1790227166 - unix, shows server date/time.
result	- dict contains:
    responsetimestamp	1790227165 - unix (1-sec delay, represents processing time before shipping response)
    producerref	"jlt" - some provider info
    responsemessageidentifier	"jlt-8020" - unique serial tracker, for this specific snapshot. 
    status	true
    moredata	false 
    vehicle - main payload, a dict which contains:
        20011 - vehicle_id, primary key for vehicles.
            recordedattime	1790227163 - unix, (3-sec delay from servertime, when the data was recorded)
            validuntiltime	1790227763 - unix, constantly 10 minutes ahead?
            linkdistance	697 - Unknown, but unique and constant for all busses
            percentage	22.81 - (.2f, 0-100), speed in percentage: Confirmed  through vehicleatstop (boolean) = vehicles not currently at stoppoint, or even vehicle on the actual move.
            lineref	"901" - Name of the line the bus is running on
            directionref	"1" - can be "0" or "1", indicates if it is running route A->B or B->A 
            publishedlinename	"901" - Name of the line the bus is running on, but the human readable version
            operatorref	"2" - corresponds to the agency_id in found here: http://data.foli.fi/gtfs/v0/agency
            originref	"8282" - refers to reference id for where the bus started its route. metadata for each is found here: http://data.foli.fi/gtfs/v0/stops, most relevant is origin lat/lon
            originname	"Korppoo"
            destinationref	"1990" - refers to same reference id as originref
            destinationname	"Linja-autoasema, tulolaituri"
            originaimeddeparturetime	1790220600 - Origin aimed departure, so when it should have departed
            destinationaimedarrivaltime	1790228700 - Origin aimed arrival, when it should aim to arrive at destination
            monitored	true - can be false, uncertain what that means, despite what it shows, they seem to have the same data structure.
            incongestion	false - traffic congestion, i am guessing? Boolean, never seen it true
            inpanic	false - no clue, but guessing if a panic button is pressed by the busdriver
            longitude	22.37132 
            latitude	60.4084
            delay	"-PT530S" - ignore use delaysecs instead.
            delaysecs	-530 - how many seconds the bus is delayed in seconds.
            blockref	"2901010100" - uncertain what it refers to , suffixed to to __tripref, unrealted for now*
            vehicleref	"20011" - vehicleref
            next_stoppointref	"6043" the next point where the bus is meant to stop - refers back to http://data.foli.fi/gtfs/v0/stops
            next_visitnumber	91 - number for next stoppoint on the route. atm the best way to get metadata (lon/lat, etc.) on each stoppoint is to use the stoppointref below, and find stop_code in stops.txt, but  onwardcalls next stop gets popped, we lose the ID, so not ideal. perhaps could be optimized?
            next_stoppointname	"Kaarina"
            vehicleatstop	false - boolean, whether or not the bus is at a stop point
            next_destinationdisplay	"Turku, linja-autoasema"
            next_aimedarrivaltime	1790227659 - aimed arrival time at the next stoppoint
            next_expectedarrivaltime	1790227115 - expected arrival time
            next_aimeddeparturetime	1790227659 - aimed departure time 
            next_expecteddeparturetime	1790227120 - expected departure time
            onwardcalls	- onwardcalls are the stop points the bus is scheduled to stop at /pass by on its route.  
                0	
                    stoppointref	"6134" - use to find metadata in stops.txt
                    visitnumber	92
                    stoppointname	"Kaarinan keskusurheilukenttä"
                    aimedarrivaltime	1790227740
                    expectedarrivaltime	1790227210
                    aimeddeparturetime	1790227740
                    expecteddeparturetime	1790227210
                1	{ … }
                2	{ … }
                3	{ … }
            originname_sv	"Korpo"  - swedish and english translations of orgin, desitnation, and display names.
            destinationname_sv	"Busstation, ankomstplattform"
            next_destinationdisplay_sv	"Åbo, busstation" 
            next_destinationdisplay_en	"Turku, bus station"
            __tripref	"00010296__2901010100" referenced here: http://data.foli.fi/gtfs/v0/trips/trip
            __routeref	"901" - the reference id for the route, metadata found here: http://data.foli.fi/gtfs/v0/routes
            __directionid	"1" - can be 1 or 0, direction which the bus is travelling, mirrors directionref
        20054
            ...
        ... 


Confirmed, percentage (.2f, 0-100) is related to vehicleatstop (boolean) = vehicles not currently at stop, or even vehicle on the actual move.

* ok genuine rabbithole: __tripref, blockref and relates back to files within gtfs.zip files: shapes.txt and stop_times.txt somehow. documentation here, but OOS for now: https://gtfs.org/documentation/schedule/reference/#shapestxt

# gtfs
http://data.foli.fi/gtfs/v0/
    "subpaths": [
        "agency",
        "stops",
        "routes",
        "trips",
        "trip_notes",
        "translations",
        "stop_times",
        "calendar",
        "calendar_dates",
        "shapes"
    ]