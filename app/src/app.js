import moment from "moment";
import m from "mithril";

var Request = {
    data: m.prop(false),

    click: function () {
	return m.request({method: "GET", url: "http://" + window.location.host + "/api"}).then(Request.data);
    },

    view: function () {
	return [
            m("table.mdl-data-table.mdl-js-data-table.mdl-shadow--4dp.mdl-cell.mdl-cell--12-col",
              m("thead",
                m("tr",
                  m("th.mdl-data-table__cell--non-numeric", "Name"),
                  m("th.mdl-data-table__cell--non-numeric", "Added")
                 )
               ),

              this.data().languages.map(function (l) {
                  var relative_date = moment(l.time * 1000).fromNow();

		  return m("tr",
                           [m("td.mdl-data-table__cell--non-numeric", l.name),
                            m("td.mdl-data-table__cell--non-numeric", relative_date)]
                          );
              })
             )
	]
    }
};

Request.click()

m.mount(document.getElementById("table"), Request);
