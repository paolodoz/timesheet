var user = {
  usr: new Array(),
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/user",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          user.usr = data.records;
          callback(data, target);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  update : function(cuser, form, callback) {
    var datestart, i = 0;
    url = "/update/user";
    cuser.group = $("#usergroup").val();
    datestart = new Date($("#userstart").val());
    datestart.setDate(datestart.getDate() -1);
    if(cuser.salary)
      i = cuser.salary.length;
    if( i == 0 ) {
      cuser.salary = new Array();
    } else {
      cuser.salary[i-1].to = simpleDate(datestart);
    }
    cuser.salary[i] = {}
    cuser.salary[i].cost = Number($("#usernewsalary").val());
    cuser.salary[i].from = $("#userstart").val();
    cuser.salary[i].to = "2099-12-31";
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(cuser),
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
  },
  getname : function(id) {
    var i;
    if(!this.usr)
      return "error";
    for(i = 0; i < this.usr.length; i++) {
      if(this.usr[i]._id == id)
        return this.usr[i].name + " " + this.usr[i].surname;
    }
    return "error";
  }
}

var project = {
  prj: new Array(),
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/project",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          project.prj = data.records;
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
    for(i = 0; i < project.tasks.length; i++) {
      project.tasks[i] = Number(project.tasks[i]);
    }
    project.responsible = {};
    project.responsible._id = $("#responsibleid").val();
    project.responsible.name  = $("#usersForm h4 span").text().trim();
    project.employees = new Array();
    $("#usersList .active").each(function (i) {
      project.employees[i] = {};
      project.employees[i]._id = this.id;
      project.employees[i].name = $(this).text().trim();
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
  },
  getname : function(id) {
    var i;
    if(!this.prj)
      return "error";
    for(i = 0; i < this.prj.length; i++) {
      if(this.prj[i]._id == id)
        return this.prj[i].name;
    }
    return "error";
  }
}

var trip = {
  _trip: new Array(),
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/trip",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          _trip = data.records;
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
      url: "/remove/trip",
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
    var trip, _trip, url;
    if(isupdate) {
      _trip = {};
      trip = _trip;
      url = "/update/trip";
    } else {
      _trip = [{}];
      trip = _trip[0];
      url = "/add/trip";
    }

    trip.accommodation = {};
    $("#" + form + " input, #" + form + " select, #" + form + " checkbox, #" + form + " textarea").each(function (){
      var property = $(this).attr("id").substr(4);
      if (property == "_id" && !isupdate)
        return;
      if($(this).is(':checkbox')) 
      {
        trip.accommodation[property] = $(this).is(':checked') ? true : false;
      }
      else
        trip[property] = $(this).val();
    });

    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(_trip),
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
  getname : function(id) {
    var i;
    for(i = 0; i < _trip.length; i++) {
      if(_trip[i]._id == id)
        return _trip[i].name;
    }
    return "error";
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

var day  = {
  load : function (filter, callback) {
    $.ajax({
      type: "POST",
      url: "/data/search_days",
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
  update : function (isupdate, obj, callback) {
    $.ajax({
      type: "POST",
      url: '/data/push_days',
      data: JSON.stringify(obj),
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

var offer = {
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/offer",
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
      url: "/remove/offer",
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
    var offer, _off, url;
    if(isupdate) {
      _off = {};
      offer = _off;
      url = "/update/offer";
    } else {
      _off = [{}];
      offer = _off[0];
      url = "/add/offer";
    }
    $("#" + form + " input, #" + form + " select, #" + form + " textarea").each(function (){
      var value, property = $(this).attr("id").substr(5);
      if (property == "_id" && !isupdate)
        return;
      if($(this).is(':checkbox')) {
        offer[property] = $(this).is(':checked') ? true : false;
      } else {
        value = Number($(this).val());
        if(isNaN(value))
          offer[property] = $(this).val();
        else
          offer[property] = value;
      }
    });
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(_off),
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

var report = {
  load: function (form, callback) {
    var report, url, hours, i;
    report = {};
    url = "/data/report_users_hours";
    report.start = $("#reportstart").val();
    report.end = $("#reportend").val();
    report.projects =  new Array();
    if($("#reportproject").val() != "")
      report.projects[0] = $("#reportproject").val();
    hours = $("label.active").children().attr("id").substr(5);
    if(hours == "B") {
      report.hours_standard = true;
      report.hours_extra = true;
    } else if(hours == "N") {
      report.hours_standard = true;
      report.hours_extra = false;
    } else {
      report.hours_standard = false;
      report.hours_extra = true;
    }
    report.users_ids = new Array();
    i = 0;
    $("#usersList li.active").each(function() {
      report.users_ids[i++] = $(this).attr("id");
    });
    report.tasks = new Array();
    i = 0;
    $("#reporttasks > option:selected").each(function() {
      report.tasks[i++] = Number($(this).val());
    });
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(report),
      success: function(data) {
        if(!data.error) {
          callback(data.records);
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

function simpleDate(date) {
  var day,month;
  day = date.getDate();
  month = date.getMonth() + 1;
  day = (day < 10 ) ? "0" + day : day;
  month = (month < 10 ) ? "0" + month : month;
  return date.getFullYear() + "-" + month + "-" + day;
}

String.prototype.bool = function() {
    return (/^true$/i).test(this);
};
