const login = require("facebook-chat-api");
const userInfo = require("./User.js");

login({ email: userInfo.username, password: userInfo.password }, (err, api) => {
  if (err) return console.error(err);

  api.listen((err, message) => {
    api.sendMessage(message.body, message.threadID);
  });
});
