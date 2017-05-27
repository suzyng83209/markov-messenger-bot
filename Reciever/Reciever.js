const login = require("facebook-chat-api");
const UserInfo = require("./UserInfo.js");



login({ email: UserInfo.USER, password: UserInfo.PASSWORD }, (err, api) => {
  if (err) return console.error(err);



  api.listen((err, message) => {
    // TODO WHAT DO WHEN LISTEN
  });


});
