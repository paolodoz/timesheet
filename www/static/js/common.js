var user = {
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/user",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          callback(data, target);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  me : function (callback) {
    $.ajax({
      type: "GET",
      url: "/me",
      data : "",
      success: function(data) {
	callback(data);
      },
      dataType: "json",
    });
  }
}

var project = {
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/project",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          callback(data, target);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  remove : function (id, callback) {
    if (id == 0)
      return;
    var filter = [{}];
    filter[0]._id = id;
    $.ajax({
      type: "POST",
      url: "/remove/project",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          callback(data);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  update : function (isupdate, form, callback) {
    var project, _proj, url;
    if(isupdate) {
      _proj = {};
      project = _proj;
      url = "/update/project";
    } else {
      _proj = [{}];
      project = _proj[0];
      url = "/add/project";
    }
    $("#" + form + " input, #" + form + " select, #" + form + " textarea").each(function (){
      var property = $(this).attr("id").substr(7);
      if (property == "_id" && !isupdate)
        return;
      project[property] = $(this).val();
    });
    project.responsible = {};
    project.responsible._id = $("#responsibleid").val();
    project.responsible.name  = String.trim($("#usersForm h4 span").text());
    project.employees = new Array();
    $("#usersList .active").each(function (i) {
      project.employees[i] = {};
      project.employees[i]._id = this.id;
      project.employees[i].name = String.trim($(this).text());
    });
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(_proj),
      success: function(data) {
        if(!data.error) {
          callback(data);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  }
}

var customer = {
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/customer",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          callback(data, target);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  remove : function (id, callback) {
    if (id == 0)
      return;
    var filter = [{}];
    filter[0]._id = id;
    $.ajax({
      type: "POST",
      url: "/remove/customer",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          callback(data);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  update : function (isupdate, form, callback) {
    var customer, _cust, url;		
    if(isupdate) {
      _cust = {};
      customer = _cust;
      url = "/update/customer";
    } else {
      _cust = [{}];
      customer = _cust[0];
      url = "/add/customer";
    }
    $("#" + form + " input").each(function (){
      var property = $(this).attr("id").substr(4);
      if (property == "_id" && !isupdate)
        return;
      customer[property] = $(this).val();
    });
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(_cust),
      success: function(data) {
        if(!data.error) {
          callback(data);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
}

function showmessage(type, msg) {
  var box = $("#msgbox");
  box.removeClass();
  box.hide();
  if(type == "error") {
    box.addClass("alert alert-danger");
  } else {
    box.addClass("alert alert-success");
  }
  box.text(msg);
  box.fadeIn("slow").delay(5000).fadeOut("slow");
}


















