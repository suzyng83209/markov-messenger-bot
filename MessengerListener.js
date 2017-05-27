const login = require("facebook-chat-api");
const request = require("request");
const rp = require("request-promise");

const SEND = "https://senderbot.herokuapp.com/";

login(
  { email: "waterloogoosehonk@gmail.com", password: "HiIAmGoose101" },
  (err, api) => {
    if (err) return console.error(err);

    api.listen((err, message) => {
      if (err) return console.error(err);

      api.markAsRead(message.threadID, err => {
        if (err) console.error(err);
      });

      api.sendTypingIndicator(message.threadID);

      if (message.body) {

        var options = {
          uri: "http://www.sentimentanalysisengine.com/" +
            message.body.split(" ").join("%20"),
          headers: {
            "User-Agent": "Request-Promise"
          },
          json: true
        };

        rp(options)
          .then(function(data) {
            if (data.positive > 0.9) {
              request(SEND + "react~:love:~" + message.messageID);
            } else if (data.negative > 0.9) {
              request(SEND + "react~:sad:~" + message.messageID);
            }
          })
          .catch(console.error);
      }
    });
  }
);
