const express = require("express");
const app = express();
const request = require("request");

app.set("port", process.env.PORT || 8888);

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.post("/messenger", (req, res) => {
  console.log("post: message");
  console.log("request:" + req);
  console.error('request:' + req.toString());
  request(
    "https://senderbot.herokuapp.com/react~:love:~" + req.message.messageID, function(err, response, body) {
      console.error(err);
      console.log('body: ', body);
    }
  );
  res.send(req);
});

app.post("/history", (req, res) => {
  console.log("post: history");
  res.send(req);
});

app.listen(app.get("port"), function() {
  console.log("running on port ", app.get("port"));
});
