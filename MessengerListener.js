const login = require("facebook-chat-api");
const request = require("request");

login({ email: 'waterloogoosehonk@gmail.com', password: 'HiIAmGoose101' }, (err, api) => {
  if (err) return console.error(err);

  api.listen((err, message) => {
    if (err) return console.error(err);

    api.markAsRead(message.threadID, err => {
      if (err) console.error(err);
    });

    let timestamp = undefined;
    api.getThreadHistory(message.threadID, 50, timestamp, (err, history) => {
      if (err) return console.error(err);
      if (timestamp != undefined) history.pop();
      timestamp = history[0].timestamp;
      request.post(
        { url: "localhost:8888/history", formData: history },
        function callback(err, httpsResponse, body) {
          if (err) {
            return console.error("failed: ", err);
          }
          console.log(body);
        }
      );
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
