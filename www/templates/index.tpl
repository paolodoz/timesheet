<!DOCTYPE html>
<html>
  <head>
    <title></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link rel="icon" href="/static/images/favicon.ico" />
    <link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen" />
    <link href="/static/css/bootstrap-switch.min.css" rel="stylesheet" media="screen" />
    <link href="/static/css/bootstrap-datepicker.css" rel="stylesheet" media="screen" />
    <link href="/static/css/bootstrap-slider.css" rel="stylesheet" media="screen" />
    <link href="/static/css/flat-ui-fonts.css" rel="stylesheet" media="screen" />
    <link href="/static/css/timesheet.css" rel="stylesheet" media="screen" />
    <!-- JavaScript plugins (requires jQuery) -->
    <script src="/static/js/jquery-1.10.2.js"></script>
    <script src="/static/js/json2.js"></script>
    <script src="/static/js/jquery.validate.min.js"></script>
    <script src="/static/js/common.js"></script>
  </head>
  <body>
<div class="row">
<div class="col-lg-4"><h2>Timesheet</h2></div>
<div class="col-lg-4">
<div id="msgbox"></div>
</div>
</div>
<div class="row">
    <div class="col-lg-2">
<ul class="nav nav-pills nav-stacked">
  <li class="${'active' if view == 'index' else ''}">
    <a href="/">
      <span class="badge pull-right hidden"></span>
      <span class="glyphicon glyphicon-cog"></span> Control Panel
    </a>
  </li>
  
% if not 'calendar' in user_views_restrictions:
  
  <li class="${'active' if view == 'calendar' else ''}">
    <a href="/index/calendar" id="menu_calendar"><span class="glyphicon glyphicon-calendar"></span> Calendar</a>
  </li>
  
% endif


% if not 'trips' in user_views_restrictions:

   <li class="${'active' if view == 'trips' else ''} dropdown">
	<a href="#" data-toggle="dropdown" role="button"><span class="glyphicon glyphicon-globe"></span> Trips<b class="caret"></b></a>
        <ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menu_trips">
            <li role="presentation"><a href="/index/trips" tabindex="-1" role="menuitem">List</a></li>
        </ul>
   </li>

% endif   
   

% if not 'expences' in user_views_restrictions:
   
  <li class="${'active' if view == 'expences' else ''} dropdown">
    <a href="#" data-toggle="dropdown" role="button"><span class="glyphicon glyphicon-credit-card"></span> Expences<b class="caret"></b></a>
      <ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menu_expences">
        <li role="presentation"><a href="/index/expences" tabindex="-1" role="menuitem">New</a></li>
        <li role="presentation"><a href="/index/expences_archive" tabindex="-1" role="menuitem">Archive</a></li>
      </ul>
  </li>
% endif   


% if not 'reports' in user_views_restrictions:
	
		
		<li><hr></li>
		
	 <li class="${'active' if view == 'reports' else 'active' if view == 'reports_prj' else ''} dropdown">
	    <a href="#" data-toggle="dropdown" role="button"><span class="glyphicon glyphicon-stats"></span> Report<b class="caret"></b></a>
		<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menu_reports">
	            <li role="presentation"><a href="/index/reports" tabindex="-1" role="menuitem">By user</a></li>
	            <li role="presentation"><a href="/index/reports_prj" tabindex="-1" role="menuitem">By project</a></li>
<!--	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Per cliente</a></li>
	            <li class="divider" role="presentation"></li>
	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Totale mese</a></li>-->
	        </ul>
	  </li>
	  
% endif


% if not 'customers' in user_views_restrictions:

	  <li class="${'active' if view == 'customers' else ''} dropdown">
	    <a href="#" data-toggle="dropdown" role="button"><span class="glyphicon glyphicon-list-alt"></span> Customers<b class="caret"></b></a>
		<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menu_customers">
	            <li role="presentation"><a href="/index/customers" tabindex="-1" role="menuitem">List</a></li>
	        </ul>
	  </li>
	  
%endif


% if not 'projects' in user_views_restrictions:
	  
	<li class="${'active' if view == 'projects' else 'active' if view == 'offers' else 'active' if view == 'production' else ''} dropdown">
	    <a href="#" data-toggle="dropdown" role="button"><span class="glyphicon glyphicon-list-alt"></span> Projects<b class="caret"></b></a>
		<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menu_projects">
	            <li role="presentation"><a href="/index/projects" tabindex="-1" role="menuitem">List</a></li>
	            <li role="presentation"><a href="/index/offers" tabindex="-1" role="menuitem">Offers</a></li>
	            <li role="presentation"><a href="/index/production" tabindex="-1" role="menuitem">Production</a></li>
	        </ul>
	  </li>

%endif


% if not 'users' in user_views_restrictions:

	<li class="${'active' if view == 'users' else ''}">
	    <a href="/index/users" id="menu_users"><span class="glyphicon glyphicon-user"></span> Users</a>
	</li>

%endif
	  

% if not 'invoices' in user_views_restrictions:
	  
	  <li class="${'active' if view == 'invoice' else ''} dropdown">
	    <a href="#" data-toggle="dropdown" role="button"><span class="glyphicon glyphicon-list-alt"></span> Invoices<b class="caret"></b></a>
		<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menu_invoices">
	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">New</a></li>
	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">List</a></li>
	        </ul>
	  </li>

% endif


<li><hr></li>
	
<li id="helplink">
  <a href="/index/help"><span class="glyphicon glyphicon-question-sign"></span> Help</a>
</li>

<li>
  <a href="/auth/logout"><span class="glyphicon glyphicon-off"></span> Logout</a>
</li>



</ul>




</div>
<div class="col-lg-9">
  ${view_page}
</div>
</div>  

    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/bootstrap-datepicker.js"></script>
    <script src="/static/js/bootstrap-slider.js"></script>
    <script src="/static/js/fullcalendar.min.js"></script>

    <!-- Enable responsive features in IE8 with Respond.js (https://github.com/scottjehl/Respond) 
    <script src="/static/js/respond.js"></script> -->
  </body>
</html>

