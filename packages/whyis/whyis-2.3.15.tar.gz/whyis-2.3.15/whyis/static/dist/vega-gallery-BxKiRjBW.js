import { V as a, E as s, v as o, n as r } from "./main-CZEa_tPp.js";
const l = a.component("vega-gallery", {
  data() {
    return {
      filter: !1,
      bottomPosition: "md-bottom-right",
      speedDials: s.speedDials,
      authenticated: s.authUser,
      existingBkmk: {
        status: !1
      }
    };
  },
  components: {
    vizGrid: o
  },
  mounted() {
    return this.showIntro();
  },
  methods: {
    showIntro(i) {
      return s.tipController(i);
    },
    showFilterBox() {
      return s.$emit("open-filter-box", { open: !0, type: "filter" }), this.filter = !0;
    },
    newChart() {
      return s.navTo("new", !0);
    },
    cancelFilter() {
      return s.cancelChartFilter();
    }
  },
  created() {
    s.$on("close-filter-box", (i) => this.filter = i).$on("isauthenticated", (i) => this.authenticated = i).$on("gotexistingbookmarks", (i) => this.existingBkmk = i);
  }
});
var c = function() {
  var t = this, e = t._self._c;
  return t._self._setupProxy, e("div", [t.existingBkmk.status ? e("div", [e("spinner", { attrs: { loading: t.existingBkmk.status, text: t.existingBkmk.text } })], 1) : e("div", [e("viz-grid", { attrs: { authenticated: t.authenticated, instancetype: "http://semanticscience.org/resource/Chart" } }), t.speedDials ? e("md-speed-dial", { class: t.bottomPosition }, [e("md-speed-dial-target", { staticClass: "utility-float-icon" }, [e("md-icon", [t._v("menu")])], 1), e("md-speed-dial-content", [e("md-button", { staticClass: "md-icon-button", on: { click: function(n) {
    return n.preventDefault(), t.cancelFilter.apply(null, arguments);
  } } }, [e("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "left" } }, [t._v(" Cancel Filter ")]), e("md-icon", { staticClass: "utility-color" }, [t._v("search_off")])], 1), e("md-button", { staticClass: "md-icon-button", on: { click: t.showFilterBox } }, [e("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "left" } }, [t._v(" Filter ")]), e("md-icon", { staticClass: "utility-color" }, [t._v("search")])], 1), e("md-button", { staticClass: "md-icon-button", on: { click: function(n) {
    return n.preventDefault(), t.showIntro(!0);
  } } }, [e("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "left" } }, [t._v("Replay Tips")]), e("md-icon", { staticClass: "utility-color" }, [t._v("info")])], 1), t.authenticated !== void 0 ? e("md-button", { staticClass: "md-icon-button", on: { click: function(n) {
    return n.preventDefault(), t.newChart.apply(null, arguments);
  } } }, [e("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "left" } }, [t._v("Create New Chart")]), e("md-icon", { staticClass: "utility-color" }, [t._v("add")])], 1) : t._e()], 1)], 1) : t._e()], 1)]);
}, d = [], u = /* @__PURE__ */ r(
  l,
  c,
  d,
  !1,
  null,
  null
);
const p = u.exports;
export {
  p as default
};
