(function( $ ){
  //rapidsearch plugin. Hide li elements that don't match the input text
  var methods = {
    init : function(options) {
      return this.each(function() {
        $(this).keyup(function () {
          compute(this);
        });
      });
    },
    update : function() {
      return this.each(function() {
        compute(this);
      });
    }
  };

  $.fn.rapidsearch = function (methodOrOptions) {
    if ( methods[methodOrOptions] ) {
      return methods[ methodOrOptions ].apply( this, Array.prototype.slice.call( arguments, 1 ));
    } else if ( typeof methodOrOptions === 'object' || ! methodOrOptions ) {
      // Default to "init"
      return methods.init.apply( this, arguments );
    } else {
      $.error( 'Method ' +  methodOrOptions + ' does not exist on rapidsearch plugin' );
    }
  }

  function compute (elem) {
    var list = elem.id.substr(3);
    var currenttext = $(elem).val().toLowerCase();
    if (currenttext == "") {
      resetvisibility($('#' + list + 'List li'));
      return;
    }
    filterlist($('#' + list + 'List li'), currenttext);
  }

  function resetvisibility(elem) {
    $(elem).each(function () {
      $(this).removeClass("hidden");
    });
  }

  function filterlist(list, currenttext) {
    $(list).each(function () {
      var elemname = $(this).text().toLowerCase();
      if (elemname.indexOf(currenttext) != -1)
        $(this).removeClass("hidden");
      else
        $(this).addClass("hidden");
    });
  }
})( jQuery );

Function.prototype.method = function (name, func) {
  if(!this.prototype[name]) {
    this.prototype[name] = func;
  }
}

var baseObject = {
  _records: new Array(),
  loadurl : '',
  load : function (filter, callback) {
    args = [];
    for(var i=2; i<arguments.length; i++) {
      args.push(arguments[i]);
    }
    this._post(this.loadurl, filter, true, callback, args);
  },
  loadSingle : function (filter, callback) {
    args = [];
    for(var i=2; i<arguments.length; i++) {
      args.push(arguments[i]);
    }
    this._post(this.loadurl, filter, false, callback, args);
  },
  _post : function (targetUrl, data, save, callback, args) {
    var that = this;
    $.ajax({
      type: "POST",
      url: targetUrl,
      data: JSON.stringify(data),
      success: function(data) {
        if(data.error) {
          showmessage("error", data.error);
        } else if(data.records) {
          if(save)
            that._records = data.records;
          callback(data.records, args);
        } else {
          callback(data,args);
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
    this._post(this.removeurl, filter, false, callback, []);
  },
  getSingleProperty : function (id, property) {
    var i;
    if(!this._records)
      return "Error, data not available";
    for(i = 0; i < this._records.length; i++) {
      if(this._records[i]._id == id)
        return this._records[i][property];
    }
    return "Error, property " + property + " not found";
  }
}

var user = Object.create(baseObject);
user.loadurl = '/get/user';
user.me = function (callback) {
  var cookie = getCookie("userdata");
  if(cookie.length > 10) {
    var data = JSON.parse(cookie);
    $("span.badge").text(data.notifications);
    $("span.badge").removeClass("hidden");
    callback(data);
    return;
  }
  $.ajax({
    type: "GET",
    url: "/me",
    data : "",
    success: function (data) {
      setCookie("userdata",JSON.stringify(data),5);
      $("span.badge").text(data.notifications);
      $("span.badge").removeClass("hidden");
      callback(data);
    },
    dataType: "json",
  });
};
user.getname = function (id) {
  var i;
  if(!this._records)
    return "Error, data not available";
  for(i = 0; i < this._records.length; i++) {
    if(this._records[i]._id == id)
      return this._records[i].name + " " + this._records[i].surname;
  }
  return "User not found";
};
user.update = function (cuser, form, callback) {
  var datestart, i = 0;
  url = "/update/user";
  cuser.group = $("#usergroup").val();
  cuser.status = $("#userstatus").val();
  cuser.contract = $("#usercontract").val();
  if($("#userstart").val() != "" && $("#usernewsalary").val() != "") {
    datestart = new Date($("#userstart").val());
    datestart.setDate(datestart.getDate() -1);
    if(cuser.salary)
      i = cuser.salary.length;
    if( i == 0 ) {
      cuser.salary = new Array();
    } else {
      cuser.salary[i-1].to = datestart.simpleDate();
    }
    cuser.salary[i] = {}
    cuser.salary[i].cost = Number($("#usernewsalary").val());
    cuser.salary[i].from = $("#userstart").val();
    cuser.salary[i].to = "2099-12-31";
  }
  this._post(url, cuser, false, callback, []);
}

var project = Object.create(baseObject);
project.loadurl = '/get/project';
project.removeurl = '/remove/project';
project.update = function (isupdate, form, callback) {
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
  project.responsibles = new Array();
  project.employees = new Array();
  $("#usersList li.active").each(function() {
    var element = {};
    element._id = this.id;
    element.name = $(this).find(".user").text().trim();
    $(this).find(".active").each(function() {
      if($(this).text() == "Employee") {
        var copy_el = {};
        jQuery.extend(copy_el, element);
        project.employees.push(copy_el);
      } else {
        if($(this).text() == "Project Manager") {
          element.role = "project manager";
        } else {
          element.role = "account";
        }
        var copy_resp = {};
        jQuery.extend(copy_resp, element);
        project.responsibles.push(copy_resp);
      }
    });
  });
  this._post(url, _proj, false, callback, []);
};
project.production = function (prj, form, callback) {
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
  this._post(url, prj, false, callback, []);
};
project.getname = function (id) {
  return this.getSingleProperty(id,'name');
};
project.getbkgcolor = function (id) {
  return this.getSingleProperty(id,'bkgcolor');
};
project.gettxtcolor = function (id) {
  return this.getSingleProperty(id,'txtcolor');
};

var trip = Object.create(baseObject);
trip.loadurl = '/data/search_trips';
trip.loadDetails = function (filter, callback) {
  args = [];
  for(var i=2; i<arguments.length; i++) {
    args.push(arguments[i]);
  }
  this._post('/get/project', filter, false, callback, args);
};
trip.remove = function (obj, callback) {
  this._post('/data/push_trips', obj, false, callback, args);
};
trip.update = function (isupdate, form, callback) {
  var prj_arr = new Array(), url;
  prj_arr[0] = {};
  prj = prj_arr[0];
  url = "/data/push_trips";
  prj._id = $("#tripproject").val();
  prj.trips = new Array();
  prj.trips[0] = {}
  prj.trips[0].user_id = me._id;
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
  this._post(url, prj_arr, false, callback);
};
trip.get = function(id) {
  var i;
  for(i = 0; i < this._records.length; i++) {
    if(this._records[i]._id == id)
      return this._records[i];
  }
  return "Error, no trip found";
};

var expence = Object.create(baseObject);
expence.loadurl = '/data/search_expences';
expence.remove = '/remove/expences';
expence.update = function (isupdate, form, status, callback) {
  var i = 0, prj_arr = [{}], url;
  url = "/data/push_expences";
  prj_arr[0]._id = $("#expprj").val();
  prj_arr[0].expences = new Array();
  prj_arr[0].expences[0] = {};
  var expence_el = prj_arr[0].expences[0];
  if(isupdate)
    expence_el._id = $("#exp_id").val();
  expence_el.trip_id = $("#exptrip").val();
  if($("#expuser_id").is(":checked")) {
    expence_el.user_id = me._id;
  } else {
    expence_el.user_id = "0";
  }
  expence_el.date = $("#expdate").val();
  expence_el.status = status;
  //file
  if(!$("#offerfile").next("p").hasClass("hidden")) {
    expence_el.file = {};
    expence_el.file._id = $("#offerfile").next("p").attr("id");
    expence_el.file.name = $("#offerfile").next("p").text();
  }
  expence_el.objects = new Array();
  $("#exptable tbody tr").each(function() {
    expence_el.objects[i] = {};
    var index = Number($(this).find("td:eq(0)").text());
    var elem = expence_el.objects[i];
    elem.date = $(this).find("input[name='" + index + "exp_date']").val();
    elem.city = $(this).find("input[name='" + index + "exp_city']").val();
    elem.amount = parseFloat($(this).find("input[name='" + index + "exp_amount']").val());
    elem.category = Number($(this).find("select[name='" + index + "exp_category']").val());
    elem.description = $(this).find("input[name='" + index + "exp_description']").val();
    if($(this).find("input[name='" + index + "exp_paidby']").is(":checked"))
      elem.paidby = 1;
    else
      elem.paidby = 0;
    elem.invoice = $(this).find("input[name='" + index + "exp_invoice']").is(":checked");
    if(!$(this).find("p").hasClass("hidden")) {
      elem.file = {};
      elem.file._id = $(this).find("p").attr("id");
      elem.file.name = $(this).find("p").text();
    }
    i++;
  });
  this._post(url, prj_arr, false, callback, []);
};
expence.getexp = function(id) {
  var i;
  for(i = 0; i < this._records.length; i++) {
    if(this._records[i]._id == id)
      return this._records[i];
  }
  return "Error, expence not found";
};

var approval = Object.create(baseObject);
approval.search = function (filter, callback) {
  args = [];
  for(var i=2; i<arguments.length; i++) {
    args.push(arguments[i]);
  }
  this._post('/data/search_approvals', filter, false, callback, args);
};
approval.set = function (filter, callback) {
  args = [];
  for(var i=2; i<arguments.length; i++) {
    args.push(arguments[i]);
  }
  this._post('/data/approval', filter, false, callback, args);
};

var customer = Object.create(baseObject);
customer.loadurl = '/get/customer';
customer.removeurl = '/remove/customer';
customer.update = function (isupdate, form, callback) {
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
  $("#" + form + " input, #" + form + " textarea").each(function (){
    var property = $(this).attr("id").substr(4);
    if (property == "_id" && !isupdate)
      return;
    customer[property] = $(this).val();
  });
  this._post(url, _cust, false, callback, []);
};

var day = Object.create(baseObject);
day.loadurl = '/data/search_days';
day.update = function (obj, callback) {
  this._post('/data/push_days', obj, false, callback, []);
};

var offer = Object.create(baseObject);
offer.loadurl = '/get/offer';
offer.removeurl = '/remove/offer';
offer.update = function (isupdate, form, callback) {
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
  this._post(url, _off, false, callback, []);
};

var report = Object.create(baseObject);
report.byuser = function (form, callback) {
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
  this._post(url, report, false, callback, []);
};
report.byproject = function (form, callback) {
  var report, url, hours, i=0;
  report = {};
  url = "/data/report_projects";
  if($("#reportstart").val() == "")
    report.start = "2012-01-01";
  else
    report.start = $("#reportstart").val();
  report.end = $("#reportend").val();
  if($("#reportmode").is(":checked"))
    report.mode = 'total';
  else
    report.mode = 'project';
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
  this._post(url, report, false, callback, []);
};

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

var tag = Object.create(baseObject);
tag.loadurl = '/data/search_tags';

function generateTags(data, args) {
  var htmlli = "", container = args[0], edit = args[1];
  for(var i = 0; i < data.length; i++) {
    htmlli += "<li>" + data[i] + "</li>";
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

function generateDropDate(from,to) {
  var htmlselect = "<option value=''></option>";
  while (from < to) {
    htmlselect += "<option value='" + from.simpleDate() + "'>" + from.getMonthName() + " " + from.getFullYear() + "</option>";
    from = new Date(from.setMonth(from.getMonth() + 1));
  }
  return htmlselect;
}

var expcategories = ["", "Hotel", "Transportation", "Food", "Other"];
var statuses = ["", "Rejected", "Pending", "Draft", "Approved by PM", "Approved by administration", "Refounded"];
var tasks = ["","Office","Away","Holiday","Bank Holiday","Leave","Unpaid leave", "Short sick leave", "Long sick leave"];
function getTaskName(id) {
  return tasks[id];
}

Date.method('simpleDate', function() {
  var day,month;
  day = this.getDate();
  month = this.getMonth() + 1;
  day = (day < 10 ) ? "0" + day : day;
  month = (month < 10 ) ? "0" + month : month;
  return this.getFullYear() + "-" + month + "-" + day;
});

Date.method('getMonthName', function(lang) {
    lang = lang && (lang in Date.locale) ? lang : 'en';
    return Date.locale[lang].month_names[this.getMonth()];
});

Date.method('getMonthNameShort', function(lang) {
    lang = lang && (lang in Date.locale) ? lang : 'en';
    return Date.locale[lang].month_names_short[this.getMonth()];
});

Date.locale = {
    en: {
       month_names: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
       month_names_short: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    }
};

String.method('bool', function() {
    return (/^true$/i).test(this);
});

String.method('capitalizeFirst',function() {
  return this.charAt(0).toUpperCase() + this.slice(1);
});

function updateStatus(type, id, status, motivation) {
  var selelem, filter;
  if(type == "expence") {
    selelem = findExpence(id);
    filter = { project_id:selelem.project_id, expence_id: id, action:status, note:motivation};
  }
  else if(type == "trip") {
    selelem = findTrip(id);
    filter = { project_id:selelem.project_id, trip_id: id, action:status, note:motivation};
  }
  approval.set(filter, removeElement, "");
}

function generateExpencesList(data, args) {
  var i,j, container = args[0], approve = args[1];
  var username, name, total, htmllist = "";
  cur_expences = data;
  for(i=0;i < data.length; i++) {
      total = computeExpenceTotal(data[i].objects);
      name = project.getname(data[i].project_id);
      username = user.getname(data[i].user_id);
      htmllist += "<li id='" + data[i]._id + "'class='list-group-item'><span class='glyphicon glyphicon-list-alt'></span> <b>Project:</b> " + name + " <button data-toggle='popover' type='button' class='btn btn-default btn-sm'><span class='glyphicon glyphicon-info-sign'></span>  Details</button>";
      if(approve) {
        htmllist += " <button type='button' class='btn btn-success btn-sm'><span class='glyphicon glyphicon-thumbs-up'></span>  Accept</button>  <button type='button' class='btn btn-danger btn-sm'><span class='glyphicon glyphicon-thumbs-down'></span>  Reject</button>";
      }
      htmllist += "<p><span class='glyphicon glyphicon-user'></span> <b>User:</b> " + username + " <span class='glyphicon glyphicon-tasks'></span> <b>Grand Total:</b> " + total + "&euro; ";
      if(data[i].file) {
        htmllist += "<span class='glyphicon glyphicon-file'></span> <b>Global receipt file:</b> <a href='/file/download/" + data[i].file._id + "'>" + data[i].file.name + "</a>";
      }
      htmllist += "</p><div class='details hidden'></div></li>";
  }
  $("#" + container).html(htmllist);
  $("#" + container + " .list-group-item button.btn-default").click(function() {
    var curid = $(this).parent().attr("id");
    if($(this).parent().find(".details").hasClass("hidden"))
      generateExpencesDetails(curid, $(this).parent().find(".details"),approve);
    $(this).parent().find(".details").toggleClass("hidden");
  });
  if(approve) {
    $("#" + container + " .list-group-item button.btn-success").click(function() {
      cur_id = $(this).parent().attr("id");
      updateStatus("expence", cur_id, "approve", "");
    });
    $("#" + container + " .list-group-item button.btn-danger").click(function() {
      cur_id = $(this).parent().attr("id");
      $('#reject .modal-title').text("Reject expence request");
      $('#reject').modal('show');
    });
  }
}

function generateExpencesDetails(id, container, edit) {
  var j,html = '<table class="table table-striped table-condensed">';
  if(edit)
    html += '<thead><tr>';
  else
    html += '<thead><tr><th></th>';
  html += '<th>Date</th><th>City</th><th>Amount</th><th>Category</th><th>Description</th><th>Paid by company</th><th>Invoice</th><th>Receipt</th></thead><tbody>';
  var element = findExpence(id);
  for(j=0; j < element.objects.length; j++) {
    html += '<tr>' + generateExpencesDetailsRow(element.objects[j], edit) + '</tr>';
  }
  html += "</tbody></table>";
  $(container).html(html);
  if(!edit) {
    $(container).find("tr td:first-child").click(function() {
      editClick($(this));
    });
  }
}

function editClick(td) {
  $(td).nextAll("td").each(function(index) {
    var value = $(this).text();
    switch(index) {
      case 0:
      case 1:
      case 4:
        $(this).html('<input type="text" class="form-control" value="' + value + '">');
        break;
      case 2:
        $(this).html('<div class="col-lg-12 input-group"><input type="text" class="form-control" value="' + value.substr(0,value.length -1) +  '"><span class="input-group-addon">&euro;</span></div>');
        break;
      case 3:
        $(this).html('<select class="form-control"></select>');
        generateSelect($(this).find("select"));
        $(this).find("select option:contains(" + value + ")").attr('selected',true);
        break;
      case 5:
      case 6:
        if(value == "No")
          $(this).html('<input type="checkbox">');
        else
          $(this).html('<input type="checkbox" checked="checked">');
        break;
      default:
        break;
    }
  });
  $(td).parent().find("input[type='checkbox']").addClass('switch-small').attr('data-on-label','YES').attr('data-off-label','NO').bootstrapSwitch();
  $(td).unbind();
  $(td).html('<span class="glyphicon glyphicon-save"></span>  Save');
  $(td).click(function() {
    saveExpence($(this).closest("li").attr("id"),$(this));
  });
}

function generateExpencesDetailsRow(row,edit) {
  var html="";
  if(!edit)
      html += '<td><span class="glyphicon glyphicon-edit"></span>  Edit</td>'
    html += '<td>' + row.date +'</td><td>' + row.city + '</td><td>' + row.amount+ '&euro;</td><td>' + expcategories[row.category] + '</td><td>' + row.description +'</td><td>';
    if(row.paidby)
      html += 'Yes</td><td>';
    else
      html += 'No</td><td>';
    if(row.invoice)
      html += 'Yes</td><td>';
    else
      html += 'No</td><td>';
    if(row.file) {
      html += '<a href="/file/download/' + row.file._id + '">' + row.file.name + '</a><td>';
    } else {
      html += '</td>';
    }
    return html;
}

function saveExpence(id, td) {
  element = expence.getexp(id);
  var i = $(td).closest('tr').index();
  $(td).nextAll("td").each(function(index) {
    switch(index) {
      case 0:
        var value = $(this).find("input").val();
        element.objects[i].date = value;
        break;
      case 1:
        var value = $(this).find("input").val();
        element.objects[i].city = value;
        break;
      case 2:
        var value = $(this).find("input").val();
        element.objects[i].amount = parseFloat(value);
        break;
      case 3:
        var value = $(this).find("select").val();
        element.objects[i].category = Number(value);
        break;
      case 4:
        var value = $(this).find("input").val();
        element.objects[i].description = value;
        break;
      case 5:
        if($(this).find("input").is(":checked"))
          element.objects[i].paidby = 1;
        else
          element.objects[i].paidby = 0;
        break;
      case 6:
        element.objects[i].invoice = $(this).find("input").is(":checked");
        break;
      default:
        break;
      }
  });
  var prj_arr = [{}], url;
  url = "/data/push_expences";
  prj_arr[0]._id = element.project_id;
  delete element.project_id;
  prj_arr[0].expences = new Array();
  prj_arr[0].expences[0] = element;
  expence._post(url, prj_arr, false, nop, []);
  var newrow = $(td).parent();
  $(newrow).html(generateExpencesDetailsRow(element.objects[i],false));
  $(newrow).find("td:eq(0)").click(function() {
    editClick($(this));
  });
  element.project_id = prj_arr[0]._id;
}

function generateSelect(ref) {
  var htmlcat = "";
  for(i=1; i < expcategories.length; i++) {
    htmlcat += "<option value='" + i + "'>" + expcategories[i] + "</option>";
  }
  $(ref).html(htmlcat);
}

$(document).ready(function() {
  $("#helplink a").click(function(e) {
    e.preventDefault();
  });
  $("#helplink a").popover({
        html: true,
        placement: 'right',
        content: $("#help").html(),
    });
});

function computeExpenceTotal(array) {
  var j,total=0;
  for(j=0; j<array.length; j++) {
    total += array[j].amount;
  }
  return total;
}

function findExpence(id) {
  var i;
  for(i=0; i<cur_expences.length; i++) {
    if(cur_expences[i]._id == id)
      return cur_expences[i];
  }
}

function findTrip(id) {
  var i;
  for(i=0; i<cur_trips.length; i++) {
    if(cur_trips[i]._id == id)
      return cur_trips[i];
  }
}

function nop(){};

/* graph values */
var g_background = '#fff';
var g_gridLineColor = '#ccc';
var g_borderColor = '#999';
var g_colorsalary = '#ff0000';
var g_colorcosts = '#7f0000';
var g_colorbugdet = '#067f00';
var g_colorextra = '#0bff00';

function getColorForPercentage (pct) {
  if(pct<=0)
    return "#ff1500";
  if(pct<10)
    return "#e8750c";
  if(pct<20)
    return "#ffcc13";
  if(pct<30)
    return "#f2ff14";
  if(pct<50)
    return "#5fff1b";
  else
    return "#13ff1e";
}

function setCookie(c_name,value,expireminutes)
{
  var exdate = new Date();
  exdate.setMinutes(exdate.getMinutes()+expireminutes);
  document.cookie = c_name + "=" + escape(value) + ((expireminutes==null) ? "" : ";expires=" + exdate.toUTCString());
}

function getCookie(c_name)
{
  if (document.cookie.length>0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";",c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start,c_end));
    }
  }
  return "";
}
