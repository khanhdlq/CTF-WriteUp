module.exports = {
    isOwner: function (request, response) {
      if (request.session.is_logined) {
        return true;
      } else {
        return false;
      }
    },
    statusUI: function (request, response) {
      var authStatusUI = 'Login and Use It'
      if (this.isOwner(request, response)) {
        authStatusUI = `Hello! ${request.session.nickname}`;
      }
      return authStatusUI;
    }
  }

  