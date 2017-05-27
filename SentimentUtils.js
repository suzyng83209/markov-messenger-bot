var http = require("http");

module.exports = {
  getSentiment: function(message, url) {
    var options = {
      host: url.concat("/"),
      path: message
    };

    callback = function(response) {
      var str = '';

      response.on('data', function(chunk) {
        str += chunk;
      });

      response.on('end', function() {
        data = JSON.parse(str);
        return data.positive;
      })
    }

    http.request(options, callback).end();
  },
  inRange: function(value, upperBound) {
    return value < upperBound;
  }
};
