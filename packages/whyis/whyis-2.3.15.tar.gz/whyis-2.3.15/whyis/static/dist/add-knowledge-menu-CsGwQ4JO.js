import { V as n, n as i } from "./main-CZEa_tPp.js";
const r = n.component("add-knowledge-menu", {
  props: ["uri"],
  data: function() {
    return {
      whichAdd: ""
    };
  }
});
var u = function() {
  var t = this, d = t._self._c;
  return t._self._setupProxy, d("div", [d("md-menu", { attrs: { "md-size": "medium", "md-align-trigger": "" } }, [d("md-button", { attrs: { "md-menu-trigger": "" }, on: { click: function(e) {
    t.whichAdd = "";
  } } }, [d("md-icon", [t._v("menu")])], 1), d("md-menu-content", [d("md-menu-item", { on: { click: function(e) {
    t.whichAdd = "addLink";
  } } }, [t._v("Add Link")]), d("md-menu-item", { on: { click: function(e) {
    t.whichAdd = "addType";
  } } }, [t._v("Add Type")]), d("md-menu-item", { on: { click: function(e) {
    t.whichAdd = "addAttribute";
  } } }, [t._v("Add Attribute")])], 1)], 1), t.whichAdd == "addLink" ? d("add-link", { attrs: { uri: t.uri, hideButton: "true" } }) : t._e(), t.whichAdd == "addType" ? d("add-type", { attrs: { uri: t.uri, hideButton: "true" } }) : t._e(), t.whichAdd == "addAttribute" ? d("add-attribute", { attrs: { uri: t.uri, hideButton: "true" } }) : t._e()], 1);
}, c = [], o = /* @__PURE__ */ i(
  r,
  u,
  c,
  !1,
  null,
  null
);
const s = o.exports;
export {
  s as default
};
