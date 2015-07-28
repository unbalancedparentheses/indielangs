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
                  m("th.mdl-data-table__cell--non-numeric", "Added"),
                  m("th.mdl-data-table__cell--non-numeric", "Type"),
                  m("th.mdl-data-table__cell--non-numeric", "Group")
                 )
               ),

              this.data().languages.map(function (l) {
                  var name = l.name;
                  var relative_date = moment(l.timestamp * 1000).fromNow();
                  var group = l.group ? l.group : '-';
                  var type = l.type ? l.type : '-';

		  return m("tr",
                           [
                               m("td.mdl-data-table__cell--non-numeric", name),
                               m("td.mdl-data-table__cell--non-numeric", relative_date),
                               m("td.mdl-data-table__cell--non-numeric", type),
                               m("td.mdl-data-table__cell--non-numeric", group)
                           ]
                          );
              })
             )
	]
    }
};

Request.click()

m.mount(document.getElementById("table"), Request);
