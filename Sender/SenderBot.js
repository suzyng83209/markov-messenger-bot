const login = require("facebook-chat-api");
const UserInfo = require("./UserInfo.js");

class SenderBot {
  constructor () {
    login({ email: UserInfo.USER, password: UserInfo.PASSWORD }, (err, api) => {
        if(err) return console.error(err);
        // Here you can use the api
    });
  }
    // /////////////////////////////////////////////////////////
    // login({ email: UserInfo.USER, password: UserInfo.PASSWORD }, (err, api) => {
    //   if (err) return console.error(err);
    //
    //   send (textTosend)
    //
    //
    //   api.sendMessage(message.body, message.threadID);
    // });
}

module.exports = new SenderBot();
