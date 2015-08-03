import 'moment'
import m from 'mithril'

var url = 'http://' + window.location.host + '/api'

var Languages = {}

Languages.Items = function () {
  this.langs = m.prop(undefined)
  this.columns = m.prop([
    'name',
    'timestamp',
    'type',
    'group'
  ])
}

Languages.controller = function () {
  var ctrl = this

  ctrl.items = new Languages.Items()
  ctrl.sort_by = m.prop('timestamp')
  ctrl.ascending = m.prop(false)

  ctrl.fetch = function () {
    return m.request({method: 'GET', url: url}).then(function (data) {
      ctrl.items.langs(data['languages'])
    })
  }

  ctrl.sort = function (e) {
    var prop = e.target.getAttribute('data-sort-by')

    if (prop) {
      var list = ctrl.items.langs()

      list.sort(comparator)

      if (ctrl.sort_by() === prop) {
        if (ctrl.ascending() === true) {
          list.reverse()
        }

        ctrl.ascending(!ctrl.ascending())
      } else {
        ctrl.sort_by(prop)
        ctrl.ascending(true)
      }
    }
  }
}

Languages.view = function (ctrl) {
  return [
    m('table.mdl-data-table.mdl-js-data-table.mdl-shadow--4dp.mdl-cell.mdl-cell--12-col',
      m('thead',
        m('tr',
          ctrl.items.columns().map(function (c) {
            var selected = (ctrl.sort_by() === c)
            var selected_class = (selected ? 'selected' : 'unselected')

            var column_name = c.charAt(0).toUpperCase() + c.slice(1)

            if (column_name === 'Timestamp') {
              column_name = 'Added'
            }

            var order_char = ctrl.ascending() ? ' ▼' : ' ▲'

            column_name = selected ? column_name + order_char : column_name

            return m('th[data-sort-by=' + c + '].mdl-data-table__cell--non-numeric',
              {onclick: ctrl.sort.bind(ctrl),
              class: selected_class},
              column_name)
          })
        )
      ),
      ctrl.items.langs() ? ctrl.items.langs().map(function (l) {
        var name = l.name
        var relative_date = moment.unix(l.timestamp).fromNow()
        var type = l.type
        var group = l.group ? l.group : '-'

        return m('tr', {key: name},
          [
            m('td.mdl-data-table__cell--non-numeric', name),
            m('td.mdl-data-table__cell--non-numeric', relative_date),
            m('td.mdl-data-table__cell--non-numeric', type),
            m('td.mdl-data-table__cell--non-numeric', group)
          ]
        )
      })
        : ctrl.fetch()
    )
  ]
}

var comparator = function (a, b) {
  if (!(prop in a) && !(prop in b)) {
    return compareNames(a, b)
  }

  if (!(prop in b)) {
    return -1
  }

  if (!(prop in a)) {
    return 1
  }

  var a_prop = a[prop]
  var b_prop = b[prop]

  if ((typeof (a_prop) === 'string') && (typeof (b_prop) === 'string')) {
    a_prop = a_prop.toLowerCase()
    b_prop = b_prop.toLowerCase()
  }

  if (a_prop > b_prop) {
    return 1
  }

  if (a_prop < b_prop) {
    return -1
  }

  if (a_prop === b_prop) {
    return compareNames(a, b)
  }
}

var compareNames = function (a, b) {
  if (a.name > b.name) {
    return 1
  } else if (a.name < b.name) {
    return -1
  } else {
    return 0
  }
}

m.mount(document.getElementById('table'), Languages)
