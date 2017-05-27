const login = require("facebook-chat-api");
const userInfo = require("./userInfo.js");
const sentimentUtils = require("./SentimentUtils.js");
const http = require("http");

login({ email: userInfo.USERNAME, password: userInfo.PASSWORD }, (err, api) => {
  if (err) return console.error(err);

  api.listen((err, message) => {
    if (err) return console.error(err);

    api.markAsRead(message.threadID, err => {
      if (err) console.error(err);
    });

    let positive = null;
    const { inRange } = sentimentUtils;

    http
      .get(
        "http://www.sentimentanalysisengine.com/".concat(
          message.body.split(" ").join("%20")
        ),
        res => {
          const { statusCode } = res;
          const contentType = res.headers["content-type"];

          let error;
          if (statusCode !== 200) {
            error = new Error(
              `Request Failed.\n` + `Status Code: ${statusCode}`
            );
          } else if (!/^application\/json/.test(contentType)) {
            error = new Error(
              `Invalid content-type.\n` +
                `Expected application/json but received ${contentType}`
            );
          }
          if (error) {
            console.error(error.message);
            res.resume();
            return;
          }

          res.setEncoding("utf8");
          let rawData = "";
          res.on("data", chunk => {
            rawData += chunk;
          });
          res.on("end", () => {
            try {
              const { positive } = JSON.parse(rawData);
              if (inRange(positive, 0.2)) {
                api.setMessageReaction(":angry:", message.messageId);
              } else if (inRange(positive, 0.4)) {
                api.setMessageReaction(":sad:", message.messageId);
              } else if (inRange(positive, 0.6)) {
                api.setMessageReaction(":like:", message.messageId);
              } else if (inRange(positive, 0.8)) {
                api.setMessageReaction(":wow:", message.messageId);
              } else {
                api.setMessageReaction(":love:", message.messageId);
              }
            } catch (e) {
              console.error(e.message);
            }
          });
        }
      )
      .on("error", e => {
        console.error(`Got error: ${e.message}`);
      });
  });
});
