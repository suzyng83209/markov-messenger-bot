const login = require("facebook-chat-api");
const userInfo = require("./User.js");

login({ email: userInfo.username, password: userInfo.password }, (err, api) => {
  if (err) return console.error(err);

  let echoState = 'INITIAL';

  api.listen((err, event) => {
    if (err) return console.error(err);

    api.markAsRead(event.threadID, (err) => {
      if (err) console.error(err);
    })

    switch(event.type) {
      case "message":
        switch(echoState) {
          case 'ON':
            if (event.body === '/stop') {
              api.sendMessage("Goodbye! Text '/startEcho' to resume.", event.threadID);
              echoState = 'OFF';
            } else {
              api.sendMessage(event.body, event.threadID);
            }
            break;

          case 'OFF':
            if (event.body === '/startEcho') {
              api.sendMessage("EchoBot will restart Echo", event.threadID);
              echoState = 'ON';
            }
            break;
          
          case 'INITIAL':
            api.sendMessage(event.body, event.threadID);
            api.sendMessage("EchoBot will start echoing conversations. Text '/stop' to stop.", event.threadID);
            echoState = 'ON';
            break;

          default:
            console.log('...');

        }
        break;

      case "event":
        console.log(event);
        break;
    }
  });
});
