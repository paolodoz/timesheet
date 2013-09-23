<!DOCTYPE html>
<html>
  <head>
    <title></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link rel='stylesheet' type='text/css' href='/static/css/redmond/jquery-ui-1.10.3.custom.min.css' />
    <link href="/static/css/timesheet.css" rel="stylesheet" media="screen">
    <!-- JavaScript plugins (requires jQuery) -->
    <script src="/static/js/jquery-1.10.2.js"></script>
    <script src="/static/js/jquery-ui-1.10.3.custom.min.js"></script>

  </head>
  <body>
<div class="row">
<div class="col-lg-12"><h2>Timesheet</h2></div>
</div>
<div class="row">
    <div class="col-lg-2">
<ul class="nav nav-pills nav-stacked">
  <li>
    <a href="#">
      <span class="badge pull-right">5</span>
      Notifiche
    </a>
  </li>
  <li class="active">
    <a href="#">
      Consuntivazione
    </a>
  </li>
  <li>
    <a href="#">
      Trasferte
    </a>
  </li>
<li>
    <a href="#">
      Note spese
    </a>
  </li>
<li><hr></li>
 <li class="dropdown">
    <a href="#" data-toggle="dropdown" role="button">Report<b class="caret"></b></a>
	<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menurep">
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Per utente</a></li>
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Per commessa</a></li>
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Per cliente</a></li>
            <li class="divider" role="presentation"></li>
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Totale mese</a></li>
        </ul>
  </li>
  <li class="dropdown">
    <a href="#" data-toggle="dropdown" role="button">Clienti<b class="caret"></b></a>
	<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menucust">
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Aggiungi</a></li>
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Elimina</a></li>
            <li class="divider" role="presentation"></li>
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Elenco</a></li>
        </ul>
  </li>
  <li>
    <a href="#">
      Commesse
    </a>
  </li>

  <li class="dropdown">
    <a href="#" data-toggle="dropdown" role="button">Fatture<b class="caret"></b></a>
	<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menuin">
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Crea Nuova</a></li>
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Visualizza esistenti</a></li>
        </ul>
  </li>


</ul>




</div>
<div class="col-lg-9">
  ${view}

</div>
</div>  

    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/fullcalendar.min.js"></script>
    <!-- Enable responsive features in IE8 with Respond.js (https://github.com/scottjehl/Respond) 
    <script src="/static/js/respond.js"></script> -->
  </body>
</html>

