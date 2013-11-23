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
    if($("#userstart").val() != "" && $("#usernewsalary").val() != "") {
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
    }
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
      if (property == "type")
        return;
      project[property] = $(this).val();
    });
    project.tags = new Array();
    $("#taglist .active").each(function (i) {
      project.tags[i] = {};
      project.tags[i] = $(this).text();
    });

    for(i = 0; i < project.tasks.length; i++) {
      project.tasks[i] = Number(project.tasks[i]);
    }
    project.responsible = {};
    if($("#responsibleid").val() == "0") {
      showmessage("error", "Select the responsible for the project");
      return;
    }
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
  production : function (prj, form, callback) {
    var url;
    url = "/update/project";
    var prod = {};
    if(!prj.economics) {
      prj.economics = new Array();
    }
    if($("#productionperiod").val() != "") {
      prod.period = $("#productionperiod").val();
      prod.budget = Number($("#productionbudget").val());
      prod.extra = Number($("#productionextra").val());
      prod.note = $("#productionnote").val();
      prod.invoiced = 0;
      prj.economics.push(prod);
    }
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(prj),
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
  },
  getbkgcolor : function(id) {
    var i;
    if(!this.prj)
      return "error";
    for(i = 0; i < this.prj.length; i++) {
      if(this.prj[i]._id == id)
        return this.prj[i].bkgcolor;
    }
    return "error";
  },
  gettxtcolor : function(id) {
    var i;
    if(!this.prj)
      return "error";
    for(i = 0; i < this.prj.length; i++) {
      if(this.prj[i]._id == id)
        return this.prj[i].txtcolor;
    }
    return "error";
  }
}

var trip = {
  _trip: new Array(),
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/data/search_trips",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          _trip = data.records;
          callback(data.records, target);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  loaddetails : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/project",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          _trip = data.records;
          callback(data.records, target);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  remove : function (obj, callback) {
    $.ajax({
      type: "POST",
      url: "/data/push_trips",
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
  update : function (isupdate, form, callback) {
    var prj_arr = new Array(), url;
    prj_arr[0] = {};
    prj = prj_arr[0];
    url = "/data/push_trips";
    prj._id = $("#tripproject").val();
    prj.trips = new Array();
    prj.trips[0] = {}
    prj.trips[0].user_id = me._id;
    prj.trips[0].note = "";
    prj.trips[0].accommodation = {};
    $("#" + form + " input, #" + form + " select, #" + form + " checkbox, #" + form + " textarea").each(function (){
      var property = $(this).attr("id").substr(4);
      if (property == "project" || (property == "_id" && !isupdate))
        return;
      if($(this).is(':checkbox')) {
        prj.trips[0].accommodation[property] = $(this).is(':checked') ? true : false;
      }
      else {
        value = Number($(this).val());
        if(isNaN(value))
          prj.trips[0][property] = $(this).val();
        else
          prj.trips[0][property] = value;
      }
    });
    trip._update(url, prj_arr, callback);
  },
  updatestatus : function (prj_arr, callback) {
    trip._update("/data/push_trips", prj_arr, callback);
  },
  _update : function (url, prj, callback) {
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(prj),
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

var expence = {
  _expence: new Array(),
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/data/search_expences",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          _trip = data.records;
          callback(data.records, target);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  loaddetails : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/project",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          _trip = data.records;
          callback(data.records, target);
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
      url: "/remove/expences",
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
  update : function (isupdate, form, status, callback) {
    var i = 0, prj = [{}], url;
    url = "/data/push_expences";
    prj[0]._id = $("#expprj").val();
    prj[0].expences = new Array();
    prj[0].expences[0] = {};
    var expence = prj[0].expences[0];
    expence.trip_id = $("#exptrip").val();
    expence.user_id = me._id;
    expence.date = $("#expdate").val();
    expence.status = status;
    //file
    if(!$("#offerfile").next("p").hasClass("hidden")) {
      expence.file = {};
      expence.file._id = $("#offerfile").next("p").attr("id");
      expence.file.name = $("#offerfile").next("p").text();
    }
    expence.objects = new Array();
    $("#exptable tbody tr").each(function() {
      expence.objects[i] = {};
      var index = Number($(this).find("td:eq(0)").text());
      var elem = expence.objects[i];
      elem.date = $(this).find("input[name='" + index + "exp_date']").val();
      elem.city = $(this).find("input[name='" + index + "exp_city']").val();
      elem.amount = parseFloat($(this).find("input[name='" + index + "exp_amount']").val());
      elem.category = Number($(this).find("select[name='" + index + "exp_category']").val());
      elem.description = $(this).find("input[name='" + index + "exp_description']").val();
      if($(this).find("input[type='checkbox']").is(":checked"))
        elem.paidby = 1;
      else
        elem.paidby = 0;
      if(!$(this).find("p").hasClass("hidden")) {
        elem.file = {};
        elem.file._id = $(this).find("p").attr("id");
        elem.file.name = $(this).find("p").text();
      }
      i++;
    });
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(prj),
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
    var offer, _off, url, i;
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
      if (property == "file")
        return;
      if($(this).is(':checkbox')) {
        offer[property] = $(this).is(':checked') ? true : false;
      } else {
        value = Number($(this).val());
        if(isNaN(value) || value == 0)
          offer[property] = $(this).val();
        else
          offer[property] = value;
      }
    });
    offer.upload_files = new Array();
    i = 0;
    $("#offerfiles li").each(function () {
      offer.upload_files[i] = {};
      offer.upload_files[i].id = $(this).attr("id");
      offer.upload_files[i].name = $(this).text();
      i++;
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
  byuser: function (form, callback) {
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
          $('#reportwait').modal('hide');
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
  byproject: function (form, callback) {
    var report, url, hours, i=0;
    report = {};
    url = "/data/report_projects";
    report.start = $("#reportstart").val();
    report.end = $("#reportend").val();
    report.projects =  new Array();
    i = 0;
    $("#projectsList li.active").each(function() {
      report.projects[i++] = $(this).attr("id");
    });
    report.customers = new Array();
    if($("#reportcustomer").val() != "") {
      report.customers[0] = $("#reportcustomer").val();
    }
    i = 0;
    report.tags = new Array();
    $("#taglist li.active").each(function() {
      report.tags[i++] = $(this).text();
    });
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(report),
      success: function(data) {
        if(!data.error) {
          callback(data.records);
        } else {
          $('#reportwait').modal('hide');
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
}

var file = {
  upload: function(filename, upComplete, upFailed) {
    var fd = new FormData();
    fd.append("data", filename);
    var xhr = new XMLHttpRequest();
    xhr.addEventListener("load", upComplete, false);
    xhr.addEventListener("error", upFailed, false);
    xhr.open("POST", "/file/upload");
    xhr.send(fd);
  },
  delete: function(id, callback, param) {
    var filter = [{}];
    filter[0]._id = id;
    $.ajax({
      type: "POST",
      url: "/remove/upload",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          callback(param, data);
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  }
}

var tag = {
  load: function(container, count, edit) {
    var filter = { 'count':count };
    $.ajax({
      type: "POST",
      url: "/data/search_tags",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          var htmlli = "";
          for(var i = 0; i < data.records.length; i++) {
            htmlli += "<li>" + data.records[i] + "</li>";
          }
          if(edit) {
            htmlli += '<li><div class="input-group"><input type="text" class="form-control input-sm" id="projecttags" name="projecttags" placeholder="New tag"><span class="input-group-addon">Add</span></div></li>';
          }
          $("#" + container).html(htmlli);
          $("#" + container + " li").click(function() {
            $(this).toggleClass("active");
          });
          $("#" + container + " li:last").unbind();
          $("#" + container + " li span").click(function() {
            var text = $(this).prev().val();
            if(text == "")
              return;
            var newhtml = "<li class='active'>" + text + "</li>";
            $(this).prev().val("");
            $("#" + container + " li:last").before(newhtml);
            $("#" + container + " li:last").prev().click(function() {
              $(this).toggleClass("active");
            });
          });
        } else {
          showmessage("error", data.error);
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  }
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
  console.log(msg);
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
var expcategories = ["", "Hotel", "Transportation", "Food", "Other"];
var statuses = ["", "Rejected", "Draft", "Pending", "Approved by PM", "Approved by administration", "Refounded"];
var tasks = ["","Office","Away","Holiday","Bank Holiday","Leave","Unpaid leave"];
function getTaskName(id) {
  return tasks[id];
}

Date.prototype.getMonthName = function(lang) {
    lang = lang && (lang in Date.locale) ? lang : 'en';
    return Date.locale[lang].month_names[this.getMonth()];
};

Date.prototype.getMonthNameShort = function(lang) {
    lang = lang && (lang in Date.locale) ? lang : 'en';
    return Date.locale[lang].month_names_short[this.getMonth()];
};

Date.locale = {
    en: {
       month_names: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
       month_names_short: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    }
};

String.prototype.bool = function() {
    return (/^true$/i).test(this);
};

function capFirstLet(string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}
