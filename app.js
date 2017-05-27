const login = require("facebook-chat-api");
const request = require("request");
const rp = require("request-promise");

const EMAIL = "waterloogoosehonk@gmail.com";
const PASSWORD = "HiIAmGoose101";
const SEND_URL = "https://senderbot.herokuapp.com/";
const ANALYZE_URL = "http://www.sentimentanalysisengine.com/";
const TOGGLE_URL = "http://toggleserver.herokuapp.com/get";

login({ email: EMAIL, password: PASSWORD }, (err, api) => {
  if (err) return console.error(err);

  api.listen((err, message) => {
    if (err) return console.error(err);

    api.markAsRead(message.threadID, err => {
      if (err) console.error(err);
    });

    rp({
      uri: TOGGLE_URL,
      headers: { "User-Agent": "Request-Promise" },
      json: true
    }).then(function(data) {
      if (data.botOn) {
        api.sendTypingIndicator(message.threadID);
        if (message.body) {
          var options = {
            uri: ANALYZE_URL + message.body.split(" ").join("%20"),
            headers: {
              "User-Agent": "Request-Promise"
            },
            json: true
          };

          rp(options)
            .then(function(data) {
              if (data.positive > 0.9) {
                request(SEND_URL + "react~:love:~" + message.messageID);
              } else if (data.negative > 0.9) {
                request(SEND_URL + "react~:sad:~" + message.messageID);
              }
            })
            .catch(console.error);
        }
      }
    });
  });
});
