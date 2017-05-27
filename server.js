const express = require("express");
const app = express();

app.set("port", process.env.PORT || 8888);

app.get("/", (req, res) => {
  res.send("Hello World");
})

app.post("/messenger", (req, res) => {
  console.log("post: message");
  console.log("request:" + req);
  res.send(req);
});

app.post("/history", (req, res) => {
  console.log("post: history");
  res.send(req);
})

app.listen(app.get("port"), function() {
  console.log("running on port ", app.get("port"));
});
