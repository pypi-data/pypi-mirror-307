import { V as t, n as s } from "./main-C6jnxO2g.js";
const n = t.component("accordion", {
  props: {
    startOpen: {
      type: Boolean,
      default: () => !1
    },
    title: {
      type: String
    }
  },
  data() {
    return {
      open: this.startOpen
    };
  },
  methods: {
    toggleOpen() {
      this.open = !this.open;
    }
  }
});
var a = function() {
  var e = this, o = e._self._c;
  return e._self._setupProxy, o("div", { staticClass: "accordion" }, [o("md-toolbar", [o("div", { staticClass: "accordion-toolbar-row", on: { click: e.toggleOpen } }, [o("h3", { staticClass: "md-title" }, [e._v(e._s(e.title))]), o("div", { staticClass: "accordion-icons" }, [o("md-icon", { directives: [{ name: "show", rawName: "v-show", value: !e.open, expression: "!open" }] }, [e._v(" expand_more ")]), o("md-icon", { directives: [{ name: "show", rawName: "v-show", value: e.open, expression: "open" }] }, [e._v(" expand_less ")])], 1)])]), e.open ? o("div", { staticClass: "accordion-content" }, [e._t("default")], 2) : e._e()], 1);
}, r = [], c = /* @__PURE__ */ s(
  n,
  a,
  r,
  !1,
  null,
  "4c253cb1"
);
const p = c.exports;
export {
  p as default
};
