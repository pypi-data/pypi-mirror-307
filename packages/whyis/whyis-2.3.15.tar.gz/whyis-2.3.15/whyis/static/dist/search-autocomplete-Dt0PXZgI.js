import { V as a, c as s, n } from "./main-CZEa_tPp.js";
const l = a.component("search-autocomplete", {
  data: () => ({
    query: null,
    selected: null,
    items: []
  }),
  methods: {
    resolveEntity(r) {
      this.items = s.get("/", {
        params: { view: "resolve", term: r + "*" },
        responseType: "json"
      }).then(function(e) {
        var o = e.data;
        return o.forEach(function(t) {
          t.toLowerCase = () => t.label.toLowerCase(), t.toString = () => t.label;
        }), o;
      });
    },
    selectedItemChange(r) {
      window.location.href = "/about?view=view&uri=" + window.encodeURIComponent(r.node);
    }
  },
  props: ["root_url", "axios"]
});
var c = function() {
  var e = this, o = e._self._c;
  return e._self._setupProxy, o("md-autocomplete", { staticClass: "search", attrs: { "md-input-name": "query", "md-options": e.items, "md-layout": "box" }, on: { "md-changed": e.resolveEntity, "md-selected": e.selectedItemChange }, scopedSlots: e._u([{ key: "md-autocomplete-item", fn: function({ item: t, term: d }) {
    return [o("span", { attrs: { "md-term": "searchText", "md-fuzzy-search": "true" } }, [e._v(e._s(t.label))]), t.label != t.preflabel ? o("span", [e._v("(preferred: " + e._s(t.preflabel) + ")")]) : e._e()];
  } }]), model: { value: e.selected, callback: function(t) {
    e.selected = t;
  }, expression: "selected" } }, [o("label", [e._v("Search")]), o("input", { directives: [{ name: "model", rawName: "v-model", value: e.query, expression: "query" }], attrs: { type: "hidden", name: "search" }, domProps: { value: e.query }, on: { input: function(t) {
    t.target.composing || (e.query = t.target.value);
  } } })]);
}, u = [], m = /* @__PURE__ */ n(
  l,
  c,
  u,
  !1,
  null,
  null
);
const p = m.exports;
export {
  p as default
};
