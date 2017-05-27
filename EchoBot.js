const login = require("facebook-chat-api");
const userInfo = require("./userInfo.js");

login({ email: userInfo.USERNAME, password: userInfo.PASSWORD }, (err, api) => {
  if (err) return console.error(err);

  let echoState = "INITIAL";

  api.listen((err, message) => {
    if (err) return console.error(err);

    api.markAsRead(message.threadID, err => {
      if (err) console.error(err);
    });

    switch (echoState) {
      case "ON":
        if (message.body === "/stop") {
          api.sendMessage(
            "Goodbye! Text '/startEcho' to resume.",
            message.threadID
          );
          echoState = "OFF";
        } else {
          api.sendMessage(message.body, message.threadID);
        }
        break;

      case "OFF":
        if (message.body === "/startEcho") {
          api.sendMessage("EchoBot will restart Echo", message.threadID);
          echoState = "ON";
        }
        break;

      case "INITIAL":
        api.sendMessage(message.body, message.threadID);
        api.sendMessage(
          "EchoBot will start echoing conversations. Text '/stop' to stop.",
          message.threadID
        );
        echoState = "ON";
        break;

      default:
        console.log("...");
    }
  });
});
