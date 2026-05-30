from flask import Flask, jsonify
import urllib.request
import time
from google.transit import gtfs_realtime_pb2

app = Flask(__name__)

FEEDS = {
    "7":   "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
    "ACE": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
    "G":   "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",
}

STOPS = {
    "7": {"manhattan": "719N", "other": "719S"},
    "E": {"manhattan": "F09N", "other": "F09S"},
    "G": {"manhattan": "G22N", "other": "G22S"},
}

LINE_TO_FEED = {
    "7": "7",
    "E": "ACE",
    "G": "G",
}

def fetch_arrivals(line, stop_id):
    try:
        feed_key = LINE_TO_FEED[line]
        url = FEEDS[feed_key]
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = response.read()
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(data)
        now = time.time()
        times = []
        for entity in feed.entity:
            if entity.HasField("trip_update"):
                trip = entity.trip_update
                if trip.trip.route_id == line:
                    for stu in trip.stop_time_update:
                        if stu.stop_id == stop_id:
                            arrival = stu.arrival.time
                            mins = round((arrival - now) / 60)
                            if 0 <= mins <= 30:
                                times.append(mins)
        return sorted(times)[:3]
    except Exception as e:
        return []

@app.route("/arrivals")
def arrivals():
    result = {}
    for line in ["7", "E", "G"]:
        result[line] = {
            "manhattan": fetch_arrivals(line, STOPS[line]["manhattan"]),
            "other":     fetch_arrivals(line, STOPS[line]["other"]),
        }
    return jsonify({
        "station": "Court Sq - LIC",
        "updated": time.strftime("%I:%M %p"),
        "trains": result
    })

if __name__ == "__main__":
    app.run()