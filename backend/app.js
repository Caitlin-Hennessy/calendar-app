var MongoClient = require("mongodb").MongoClient;
var mongoUrl = "mongodb://localhost:27017";
var express = require("express");
var cors = require("cors");
var bodyParser = require("body-parser");
var app = express();
app.use(cors());
app.use(bodyParser.json());
//app.use("/", express.static("public"));

var client = new MongoClient(mongoUrl);
client.connect(function(err) {
  if (err) throw err;
  var db = client.db("calendar_events");

  // app.all("/", (req, res, next) => {
  //   res.header("Access-Control-Allow-Origin", "*");
  //   res.header("Access-Control-Allow-Headers", "Content-Type");
  //   res.header("Access-Control-Allow-Methods", "*");
  //   next();
  // });

  app.post("/cisevents", (req, res) => {
    var params = {};
    db.collection("cis")
      .find(params)
      .toArray((err, cisevents) => {
        if (err) {
          //TODO - don't show error in response body
          throw err;
        }
        res.json(cisevents);
      });
  });

  // app.post("/faults", (req, res) => {
  //   var params = {
  //     geometry: {
  //       $geoWithin: {
  //         $geometry: {
  //           type: "Polygon",
  //           coordinates: req.body.coordinates
  //         }
  //       }
  //     }
  //   };
  //   db.collection("faults")
  //     .find(params)
  //     .toArray((err, faults) => {
  //       if (err) throw err;
  //       res.json(faults);
  //     });
  // });

  app.listen(3000, () => {
    console.log("Server running on 3000");
  });
});
