<!DOCTYPE html>
<html>
  <head>
    <title>Timesheet login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link rel="icon" href="/static/images/favicon.ico" />
    <link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
  </head>
  <body>
  
	% if message:
		<div class="alert alert-danger">${message}</div>
	% endif
  
<div class="row">
  <div class="col-lg-4 col-lg-offset-4"><h3>Timesheet login</h3>
<form class="form-horizontal" method="post" action="/auth/login">
  <div class="form-group">
    <label for="inputEmail" class="col-lg-3 control-label">Username</label>
    <div class="col-lg-5">
      <input type="text" class="form-control" id="inputEmail" placeholder="LDAP username" name="username">
    </div>
  </div>
  <div class="form-group">
    <label for="inputPassword" class="col-lg-3 control-label">Password</label>
    <div class="col-lg-5">
      <input type="password" class="form-control" id="inputPassword" placeholder="Password" name="password">
    </div>
  </div>
  <div class="form-group">
    <div class="col-lg-offset-3 col-lg-5">
      <div class="checkbox">
        <label>
          <input type="checkbox"> Remember me
        </label>
      </div>
    </div>
  </div>
  <div class="form-group">
    <div class="col-lg-offset-3 col-lg-5">
      <button type="submit" class="btn btn-default">Sign in</button>
    </div>
  </div>
</form>

</div>
</div>
    

    <!-- JavaScript plugins (requires jQuery) -->
    <script src="/static/js/jquery-1.10.2.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/static/js/bootstrap.min.js"></script>
    <script type="text/javascript">
      document.getElementById("inputEmail").focus();
    </script>
    <!-- Enable responsive features in IE8 with Respond.js (https://github.com/scottjehl/Respond) 
    <script src="/static/js/respond.js"></script> -->
  </body>
</html>

