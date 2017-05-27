const login = require("facebook-chat-api");
const userInfo = require("./userInfo.js");
const request = require("request");

login({ email: userInfo.USERNAME, password: userInfo.PASSWORD }, (err, api) => {
  if (err) return console.error(err);

  api.listen((err, message) => {
    if (err) return console.error(err);

    api.markAsRead(message.threadID, err => {
      if (err) console.error(err);
    });

    request.post(
      { url: "localhost:8888/messenger", formData: message },
      function callback(err, httpResponse, body) {
        if (err) {
          return console.error("failed", err);
        }
        console.log(body);
      }
    );
  });
});
