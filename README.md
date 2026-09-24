
 

### Background
Foli is the bus service in Turku Municipality. They offer an interface into their live and static data.

Foli also uses Service Interface for Real-time Information (SIRI), to structure and provide realtime information about busses current location, delays, routes planned/taken, etc. 
[check for foli json (updated every 2-3 seconds)](http://data.foli.fi/siri/vm)

Foli uses General Transit Feed Specification (GTFS) for exchanging static information about routes, fi-sv-en translations of stopnames, trips, trip_notes, etc.
[GTFS.ZIP - static files ](http://data.foli.fi/gtfs/gtfs.zip)


### Scope
1. Stucture the static data and populate a postgreSQL db with said static data.
2. Use fastapi to async poll SIRI/vm at set interval (tick = 3,5,10 seconds?), get {location, lat, lng} for each bus per client session, compute haversine distance (as-the-crow-flies distance) for client's stored location at each tick interval showing all busses within N meters of distance.
3. React-based leaflet map with MUI shell, that subscribes to busses, shows client live position (throttled), renders both client and busses.
4. platform to support client voice commands, through n8n agent workflows that decide intent. current ideas:
- route_tool
- disruption_tool
- schedule_tool

Voice capture though fast-whisper,  