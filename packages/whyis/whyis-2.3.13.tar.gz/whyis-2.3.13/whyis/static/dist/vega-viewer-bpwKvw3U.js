import { n as l, V as d, E as s, l as u, q as r, f as v, k as n, S as c } from "./main-C6jnxO2g.js";
import { V as m } from "./v-jsoneditor.min-zJh_utFy.js";
const p = {};
var h = function() {
  var t = this, a = t._self._c;
  return a("div", [t._v(" ▬▬▬▬▬ ▬▬▬▬ ▬▬▬ ▬▬▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬ ▬▬▬▬▬▬▬ ▬▬▬▬▬ ▬▬▬▬▬▬ ▬▬ ▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬▬ ▬▬ ▬▬ ▬▬▬ ▬▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬▬ ▬▬▬▬ ▬▬▬ ▬▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬▬ ▬▬▬▬ ▬▬▬ ▬▬▬▬▬▬▬ ▬▬▬▬▬ ▬▬▬▬▬▬ ▬▬ ▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬ ▬▬▬▬▬ ▬▬▬▬▬▬ ▬▬ ▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬ ▬ ▬▬▬ ▬▬▬▬▬▬ ▬▬ ▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬▬ ▬▬ ▬▬ ▬▬▬ ▬▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬▬ ▬▬▬▬ ▬▬▬ ▬▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬▬ ▬▬▬▬ ▬▬▬ ▬▬▬▬▬▬▬ ▬▬▬▬▬ ▬▬▬▬▬▬ ▬▬ ▬▬▬▬ ▬▬▬▬ ▬▬▬▬▬▬▬ ▬▬▬▬▬ ▬▬▬▬▬▬ ▬▬ ▬▬▬▬ ▬▬▬▬ ")]);
}, _ = [], f = /* @__PURE__ */ l(
  p,
  h,
  _,
  !1,
  null,
  null
);
const g = f.exports, b = d.component("vega-viewer", {
  data() {
    return {
      error: { status: !1, message: null },
      filter: !1,
      loading: !0,
      spec: null,
      chart: null,
      chartTags: [],
      args: null,
      authenticated: s.authUser,
      allowEdit: !1,
      vizOfTheDay: !1,
      voyager: {
        show: !1
      },
      specViewer: {
        show: !1,
        includeData: !1,
        jsonEditorOpts: {
          mode: "code",
          mainMenuBar: !1,
          onEditable: () => !1
        }
      }
    };
  },
  components: {
    tempFiller: g,
    VJsoneditor: m
  },
  computed: {
    specViewerSpec() {
      return this.specViewer.includeData ? this.spec : this.chart && this.chart.baseSpec;
    }
  },
  methods: {
    async loadVisualization() {
      if (this.chart = await u(this.pageUri), s.checkIfEditable(this.chart.uri), this.chart.query) {
        const i = await r(this.chart.query);
        this.spec = v(this.chart.baseSpec, i);
      } else
        this.spec = this.chart.baseSpec;
      this.chart.dataset && (this.spec = this.chart.baseSpec, this.spec.data = { url: `/about?uri=${this.chart.dataset}` }), this.loading = !1;
    },
    navBack(i) {
      return i && s.toggleVizOfTheDay(i), s.navTo("view", !0);
    },
    openVoyager() {
      n(this.chart.uri, "voyager");
    },
    shareChart() {
      return s.$emit("dialoguebox", {
        status: !0,
        share: !0,
        title: "Share Chart",
        message: "Copy the chart link above to share this chart",
        chart: this.chart.uri
      });
    },
    editChart() {
      return n(this.chart.uri, "edit");
    },
    chartQuery() {
      if (this.chart.query)
        return s.$emit("dialoguebox", {
          status: !0,
          query: !0,
          title: "Chart Query",
          message: "Copy and rerun query on a sparql endpoint",
          chart: this.chart.query
        });
    },
    slugify(i) {
      return c(i);
    },
    tableView() {
      this.chart.query && r(this.chart.query).then((i) => (console.log(i), s.$emit("dialoguebox", {
        status: !0,
        tableview: i,
        title: "Table View of Chart Data",
        chart: this.chart.query
      })));
    },
    slugify(i) {
      return c(i);
    }
  },
  beforeMount() {
    return this.loadVisualization();
  },
  destroyed() {
    this.error = { status: !1, message: null };
  },
  created() {
    this.loading = !0, s.$on("isauthenticated", (i) => this.authenticated = i).$on("allowChartEdit", (i) => this.allowEdit = i);
  }
});
var y = function() {
  var t = this, a = t._self._c;
  return t._self._setupProxy, a("div", [a("div", { staticClass: "utility-content__result" }, [t.loading ? t._e() : a("div", { staticClass: "utility-gridicon-single" }, [t.vizOfTheDay ? t._e() : a("div", [a("md-button", { staticClass: "md-icon-button", nativeOn: { click: function(e) {
    return e.preventDefault(), t.navBack.apply(null, arguments);
  } } }, [a("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "bottom" } }, [t._v(" Go Back ")]), a("md-icon", [t._v("arrow_back")])], 1)], 1), a("div", [a("md-button", { staticClass: "md-icon-button", nativeOn: { click: function(e) {
    return e.preventDefault(), t.shareChart.apply(null, arguments);
  } } }, [a("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "top" } }, [t._v(" Share Chart ")]), a("md-icon", [t._v("share")])], 1)], 1), t.chart.query ? a("div", [a("md-button", { staticClass: "md-icon-button", nativeOn: { click: function(e) {
    return e.preventDefault(), t.chartQuery.apply(null, arguments);
  } } }, [a("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "bottom" } }, [t._v(" Preview Chart Query ")]), a("md-icon", [t._v("preview")])], 1)], 1) : t._e(), a("div", [a("md-button", { staticClass: "md-icon-button", nativeOn: { click: function(e) {
    return e.preventDefault(), t.tableView.apply(null, arguments);
  } } }, [a("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "bottom" } }, [t._v(" View Data as Table ")]), a("md-icon", [t._v("table_view")])], 1)], 1), a("div", [a("md-button", { staticClass: "md-icon-button", nativeOn: { click: function(e) {
    e.preventDefault(), t.specViewer.show = !0;
  } } }, [a("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "bottom" } }, [t._v(" Preview Chart Spec ")]), a("md-icon", [t._v("integration_instructions")])], 1)], 1), a("div", [a("md-button", { staticClass: "md-icon-button", nativeOn: { click: function(e) {
    return e.preventDefault(), t.openVoyager();
  } } }, [a("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "bottom" } }, [t._v(" View Data in Voyager ")]), a("md-icon", [t._v("dynamic_form")])], 1)], 1), t.allowEdit ? a("div", [a("md-button", { staticClass: "md-icon-button", nativeOn: { click: function(e) {
    return e.preventDefault(), t.editChart.apply(null, arguments);
  } } }, [a("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "top" } }, [t._v(" Edit Chart ")]), a("md-icon", [t._v("edit")])], 1)], 1) : t._e()])]), a("div", { staticClass: "viz-3-col viz-u-mgup-sm" }, [a("div", { staticClass: "loading-dialog__justify" }, [a("div", { staticClass: "viz-sample" }, [t.vizOfTheDay ? a("div", { staticClass: "viz-sample__header viz-u-mgbottom" }, [a("md-icon", { staticStyle: { "font-size": "2rem !important", color: "gray !important" } }, [t._v("bar_chart")]), t._v(" Viz of the day ")], 1) : a("div", { staticClass: "viz-u-mgbottom-big viz-u-display__desktop" }), t.vizOfTheDay ? t._e() : a("div", { staticClass: "viz-sample__header viz-u-mgbottom" }, [t._v(" Chart Information ")]), a("div", { staticClass: "viz-sample__content" }, [t.loading ? a("temp-filler", { staticClass: "viz-sample__loading viz-sample__loading_anim" }) : a("div", {}, [a("div", { staticClass: "md-headline viz-u-mgup-sm btn--animated" }, [t._v(t._s(t.chart.title))]), a("div", { staticClass: "btn--animated" }, [t._v(" " + t._s(t.slugify(t.chart.description)) + " ")]), a("div", { staticClass: "viz-sample__list btn--animated" }, [a("ul", t._l(t.chartTags, function(e, o) {
    return a("li", { key: o, staticClass: "viz-u-postion__rel" }, [a("div", { staticClass: "viz-sample__content__card viz-u-display__hide viz-u-postion__abs" }, [t._v(" " + t._s(e.description) + " "), a("div", [a("a", { staticClass: "btn-text btn-text--simple", attrs: { target: "_blank", href: e.uri } }, [t._v("More")])])]), t._v(" " + t._s(e.title) + " ")]);
  }), 0)]), t.vizOfTheDay ? a("a", { staticClass: "btn btn_medium btn--primary viz-u-display__desktop btn--animated", on: { click: function(e) {
    return e.preventDefault(), t.navBack(!0);
  } } }, [t._v("View Gallery")]) : t._e()])], 1)])]), t.loading ? a("div", { staticClass: "loading-dialog", staticStyle: { margin: "auto" } }, [a("spinner", { attrs: { loading: t.loading } })], 1) : a("div", { staticClass: "loading-dialog", staticStyle: { margin: "auto" } }, [a("div", { staticClass: "viz-u-display__desktop", staticStyle: { "margin-bottom": "2rem" } }), a("vega-lite", { staticClass: "btn--animated", attrs: { spec: t.spec } }), t.vizOfTheDay ? a("a", { staticClass: "btn btn_small btn--primary utility-margin-big viz-u-display__ph", on: { click: function(e) {
    return e.preventDefault(), t.navBack(!0);
  } } }, [t._v("View Gallery")]) : t._e()], 1), a("md-dialog", { staticClass: "chart-spec", attrs: { "md-active": t.specViewer.show }, on: { "update:mdActive": function(e) {
    return t.$set(t.specViewer, "show", e);
  }, "update:md-active": function(e) {
    return t.$set(t.specViewer, "show", e);
  } } }, [a("md-dialog-title", [t._v("Chart Vega Spec")]), a("md-content", { staticClass: "vega-spec-container" }, [a("v-jsoneditor", { attrs: { options: t.specViewer.jsonEditorOpts }, model: { value: t.specViewerSpec, callback: function(e) {
    t.specViewerSpec = e;
  }, expression: "specViewerSpec" } })], 1), a("div", { staticClass: "vega-spec-controls" }, [a("md-checkbox", { model: { value: t.specViewer.includeData, callback: function(e) {
    t.$set(t.specViewer, "includeData", e);
  }, expression: "specViewer.includeData" } }, [t._v("Include data in spec")])], 1), a("md-dialog-actions", [a("md-button", { staticClass: "md-primary", on: { click: function(e) {
    t.specViewer.show = !1;
  } } }, [t._v("Close")])], 1)], 1), t.voyager.show ? a("data-voyager", { attrs: { data: t.spec.data } }) : t._e()], 1)]);
}, C = [], w = /* @__PURE__ */ l(
  b,
  y,
  C,
  !1,
  null,
  "1d4884e9"
);
const z = w.exports;
export {
  z as default
};
