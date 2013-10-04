var project = {
  load : function (filter, callback, target) {
    $.ajax({
      type: "POST",
      url: "/get/project",
      data: JSON.stringify(filter),
      success: function(data) {
        if(!data.error) {
          callback(data, target);
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
        }
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
    });
  },
}




















