const express = require("express");
const app = express();

app.set("port", process.env.PORT || 8888);

app.post("/", (req, res) => {
  console.log("post")
  res.send(req);
});

app.listen(app.get("port"), function() {
  console.log("running on port ", app.get("port"));
});
