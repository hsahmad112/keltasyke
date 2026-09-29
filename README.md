### Background
Foli is the bus service in Turku Municipality. They offer an interface into their live and static data.

Foli uses Service Interface for Real-time Information (SIRI), to structure and provide realtime information about busses current location, delays, routes planned/taken, etc. 
[check for foli json (updated every 2-3 seconds)](http://data.foli.fi/siri/vm)

Foli also uses the General Transit Feed Specification (GTFS) for exchanging static information about routes, fi-sv-en translations of stopnames, trips, trip_notes, etc.
[GTFS.ZIP - static files ](http://data.foli.fi/gtfs/gtfs.zip)





### Scope
1. Stucture the static data and populate a postgreSQL db with said static data + some user tables (preference, service-alerts).
2. Use fastapi to async poll SIRI/vm at set interval (tick = 3,5,10 seconds?), get {location, lat, lng} for each bus and client per client session, compute haversine distance (as-the-crow-flies distance) for client's stored location at each tick interval showing all busses within N meters of distance.
3. React-based leaflet map with MUI shell, that allows user to subscribes to preferred busses/routes, shows client live position (throttled), renders both client and busses.
4. More complex ideas to implement once the db/backend/frontend scaffolding is up:
- Natural language parsing (voice/text) e.g. "I wanna get to martinsillan grilli by Martinsilta in Turku ASAP" and through that:
  - live time routing suggestions using n8n agents for intent understanding. 
  - Connect the suggested routes coordinates to live weather data (match on coordinates), to provide a (closer to) accurate estimation of weather at the departure, journey and destination.
  - Connect to Donkey Republics live api (stables.donkey.bike/api/public/gbfs/3.0/donkey_turku/), include their bikes as transport options.

### Wildcard idea: 
Use android devices' barometric sensor to get a (closer to) accurate idea of what floor a person is on (as pressure drops predictably with elevation) and include that in travel time.
As [barometric sensors are not accessible through browsers on smartphones](https://sensor-js.xyz/webs-sixth-sense-ccs18.pdf), it would require me to make this an actual android app. So Kotlin or React Native/Capacitor would be required to access the barometer natively on Android and iOS. 
Also afaik random (hi/lo-pressure) weather system can impact ambient readings, so a baseline would be required (local weather station at sea-level). And that still leaves the "how" to calculate average travel time for user (elevator vs stairs) and user speed. So yeah, wild wildcard >:D.
