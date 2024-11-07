import { V as r, E as s, n as o } from "./main-C6jnxO2g.js";
import { l as c } from "./orcid-lookup-MufoY1S_.js";
let l;
const u = () => (l = setInterval(() => {
  const a = document.getElementsByClassName("md-menu-content-bottom-start");
  if (a.length >= 1)
    return a[0].setAttribute("style", "z-index:1000 !important; width: 410px; max-width: 410px; position: absolute; top: 579px; left:50%; transform:translateX(-50%); will-change: top, left;"), status = !0;
}, 40), l), d = () => {
  if (l)
    return clearInterval(l);
}, m = r.component("dialogBox", {
  data() {
    return {
      active: !1,
      required: null,
      hasMessages: !1,
      loginRequestSent: !1,
      filterby: "title",
      selectedText: null,
      password: null,
      introTipScreen: 1,
      textarea: null,
      chartResults: {
        title: [],
        description: [],
        query: [],
        tableview: []
      },
      dialog: {
        status: !1
      },
      makeNew: {
        status: !1
      },
      agent: "",
      organization: {
        type: "Organization",
        name: ""
      },
      author: {
        type: "Person",
        name: "",
        "@id": null
      }
    };
  },
  computed: {
    messageClass() {
      return {
        "md-invalid": this.hasMessages
      };
    }
  },
  watch: {
    dialog(a, t) {
      a && a.share && this.copyText();
    }
  },
  components: {},
  destroy() {
    return d();
  },
  methods: {
    copyText() {
      setTimeout(() => {
        const a = document.getElementById("sharedlinktext");
        if (a)
          return a.select(), a.setSelectionRange(0, 99999), document.execCommand("copy"), s.$emit("snacks", { status: !0, message: "Chart link copied!", tip: "Paste Anywhere" });
      }, 800);
    },
    onConfirm() {
      return this.active = !this.active, this.loginRequestSent = !1, s.$emit("close-filter-box", this.active), s.filterChart(this.filterby, this.selectedText);
    },
    onSubmitNew() {
      if (this.active = !this.active, this.loginRequestSent = !1, this.agent === "author") {
        const a = c(this.author["@id"], "author");
        console.log(a);
      } else if (this.agent === "organization")
        return;
      s.$emit("close-filter-box", this.active);
    },
    onCancel() {
      this.active = !this.active, s.$emit("close-filter-box", this.active);
    },
    cancelDel() {
      this.active = !this.active, this.dialog = { status: !1 }, s.$emit("close-filter-box", this.active);
    },
    dialogAction() {
      return this.active = !this.active, this.dialog.delete ? s.deleteAChart(this.dialog.chart) : this.dialog.reset && s.resetChart(), this.dialog = { status: !1 }, s.$emit("close-filter-box", this.active);
    },
    nextScreen() {
      return this.introTipScreen += 1;
    },
    previousScreen() {
      if (this.introTipScreen >= 2)
        return this.introTipScreen -= 1;
    }
  },
  created() {
    s.$on("open-filter-box", (a) => {
      if (a.type == "filter")
        return this.active = a.open, u();
      this.active = a.open, this.loginRequestSent = !0;
    }).$on("appstate", (a) => {
      a.length >= 1 && (this.chartResults.title = a.map((t) => t.backup.title), this.chartResults.description = a.map((t) => t.backup.description), this.chartResults.query = a.map((t) => t.backup.query));
    }).$on("dialoguebox", (a) => {
      a && a.intro ? (this.active = a.status, this.dialog = a, this.introTipScreen = 1) : (this.active = a.status, this.dialog = a);
    }).$on("open-new-instance", (a) => {
      this.active = a.status, this.agent = a.type, this.makeNew = a;
    });
  }
});
var g = function() {
  var t = this, e = t._self._c;
  return t._self._setupProxy, e("div", [e("md-dialog", { attrs: { "md-active": t.active, "md-click-outside-to-close": !0 }, on: { "update:mdActive": function(i) {
    t.active = i;
  }, "update:md-active": function(i) {
    t.active = i;
  } } }, [t.dialog.intro ? e("div", { staticClass: "viz-intro" }, [e("div", { staticClass: "utility-gridicon utility-margin-top" }, [e("span", { staticClass: "viz-intro-title" }, [t._v("tips ˙")])]), e("intros", { attrs: { screen: t.introTipScreen } }), e("div", { staticClass: "utility-align--right" }, [t.introTipScreen == 1 ? e("a", { staticClass: "btn-text btn-text--primary btn--animated utility-margin-right", on: { click: function(i) {
    return i.preventDefault(), t.cancelDel.apply(null, arguments);
  } } }, [e("span", { staticClass: "md-title" }, [t._v(" Skip")])]) : e("a", { staticClass: "btn-text btn-text--primary btn--animated utility-margin-right", on: { click: function(i) {
    return i.preventDefault(), t.previousScreen.apply(null, arguments);
  } } }, [e("span", { staticClass: "md-title" }, [t._v("Previous")])]), t.introTipScreen <= 3 ? e("a", { staticClass: "btn-text btn-text--primary btn--animated", on: { click: function(i) {
    return i.preventDefault(), t.nextScreen.apply(null, arguments);
  } } }, [e("span", { staticClass: "md-title" }, [t._v("Next")])]) : e("a", { staticClass: "btn-text btn-text--primary btn--animated", on: { click: function(i) {
    return i.preventDefault(), t.cancelDel.apply(null, arguments);
  } } }, [e("span", { staticClass: "md-title" }, [t._v("Close")])])])], 1) : e("div", [e("div", { staticClass: "utility-dialog-box_header" }, [t.dialog.status ? e("md-dialog-title", [t._v(t._s(t.dialog.title))]) : t.makeNew.status ? e("md-dialog-title", [t._v(t._s(t.loginRequestSent ? "Login" : t.makeNew.title))]) : e("md-dialog-title", [t._v(t._s(t.loginRequestSent ? "Login" : "Filter Chart"))])], 1), t.dialog.status ? e("div", { staticClass: "utility-dialog-box_login" }, [t.dialog.share ? e("div", { staticStyle: { "margin-right": ".1rem !important" } }, [e("md-field", { staticStyle: { "max-width": "100%" } }, [e("label", [t._v("Chart Link")]), e("md-textarea", { attrs: { id: "sharedlinktext", "md-counter": "150" }, model: { value: t.dialog.chart, callback: function(i) {
    t.$set(t.dialog, "chart", i);
  }, expression: "dialog.chart" } }, [t._v(t._s(t.dialog.chart))])], 1), e("span", { staticClass: "md-subheading" }, [t._v(" " + t._s(t.dialog.message))])], 1) : t.dialog.tableview ? e("div", { staticStyle: { "margin-right": ".8rem !important" } }, [e("div", { staticClass: "viz-intro-query", staticStyle: { "min-height": "40rem !important" } }, [e("yasr", { attrs: { results: t.dialog.tableview } })], 1)]) : t.dialog.query ? e("div", { staticStyle: { "margin-right": ".8rem !important" } }, [e("div", { staticClass: "viz-intro-query" }, [e("yasqe", { attrs: { showBtns: !0 }, model: { value: t.dialog.query, callback: function(i) {
    t.$set(t.dialog, "query", i);
  }, expression: "dialog.query" } })], 1), e("span", { staticClass: "md-subheading" }, [t._v(" " + t._s(t.dialog.message))])]) : e("div", [e("span", { staticClass: "md-subheading" }, [t._v(t._s(t.dialog.message))])]), t.dialog.share || t.dialog.delete || t.dialog.query || t.dialog.diag || t.dialog.tableview ? e("div", { staticClass: "utility-margin-big viz-2-col" }, [e("div", { staticClass: "utility-margin-top" }), t.dialog.share || t.dialog.query || t.dialog.tableview ? e("div", { staticClass: "utility-align--right utility-margin-top" }, [e("a", { staticClass: "btn-text btn-text--default", on: { click: function(i) {
    return i.preventDefault(), t.cancelDel.apply(null, arguments);
  } } }, [t._v("Close")])]) : t.dialog.delete || t.dialog.diag ? e("div", { staticClass: "utility-align--right utility-margin-top" }, [e("a", { staticClass: "btn-text btn-text--default", on: { click: function(i) {
    return i.preventDefault(), t.cancelDel.apply(null, arguments);
  } } }, [t._v("Close")]), t._v("     "), t.dialog.btn ? t._e() : e("a", { staticClass: "btn-text btn-text--default", on: { click: function(i) {
    return i.preventDefault(), t.dialogAction.apply(null, arguments);
  } } }, [t._v(t._s(t.dialog.title))])]) : t._e()]) : t._e()]) : t.makeNew.status ? e("div", { staticClass: "utility-dialog-box_login" }, [t.makeNew.type === "organization" ? e("md-field", [e("label", [t._v("Name of Organization")]), e("md-input", { model: { value: t.organization.name, callback: function(i) {
    t.$set(t.organization, "name", i);
  }, expression: "organization.name" } })], 1) : t.makeNew.type === "author" ? e("div", [e("div", { staticClass: "md-layout md-gutter", staticStyle: { "align-items": "center", "justify-content": "center" } }, [e("div", { staticClass: "md-layout-item md-size-50" }, [e("md-field", [e("label", [t._v("Name")]), e("md-input", { attrs: { required: "" }, model: { value: t.author.name, callback: function(i) {
    t.$set(t.author, "name", i);
  }, expression: "author.name" } })], 1)], 1), e("div", { staticClass: "md-layout-item md-size-50" }, [e("md-field", [e("label", [t._v("ORCID Identifier")]), e("md-input", { staticStyle: { "max-width": "100%" }, attrs: { required: "" }, model: { value: t.author["@id"], callback: function(i) {
    t.$set(t.author, "@id", i);
  }, expression: "author['@id']" } })], 1)], 1)]), e("div", { staticStyle: { "margin-bottom": "40px", "text-align": "center" } }, [t._v(" Don't have an ORCID iD? "), e("a", { attrs: { href: "https://orcid.org/", target: "_blank" } }, [t._v("Create one here")])])]) : t._e(), e("div", { staticClass: "utility-margin-big viz-2-col" }, [e("div", { staticClass: "utility-align--right utility-margin-top" }), e("div", { staticClass: "utility-align--right utility-margin-top" }, [e("a", { staticClass: "btn-text btn-text--default", on: { click: function(i) {
    return i.preventDefault(), t.onCancel.apply(null, arguments);
  } } }, [t._v(" ← Exit")]), t._v("     "), e("a", { staticClass: "btn-text btn-text--default", on: { click: function(i) {
    return i.preventDefault(), t.onSubmitNew.apply(null, arguments);
  } } }, [t._v("Submit → ")])])])], 1) : e("div", { staticClass: "utility-dialog-box_login" }, [e("div", { staticClass: "md-layout-item" }, [e("md-field", [e("label", { attrs: { for: "movie" } }, [t._v("Filter By")]), e("md-select", { attrs: { name: "filterby", id: "filterby", placeholder: "Filter By" }, model: { value: t.filterby, callback: function(i) {
    t.filterby = i;
  }, expression: "filterby" } }, [e("md-option", { attrs: { value: "title" } }, [t._v("Chart Title")]), e("md-option", { attrs: { value: "query" } }, [t._v("Chart Query")]), e("md-option", { attrs: { value: "description" } }, [t._v("Chart Description")])], 1)], 1)], 1), e("md-autocomplete", { attrs: { "md-options": t.filterby == "title" ? t.chartResults.title : t.filterby == "query" ? t.chartResults.query : t.chartResults.description, "md-open-on-focus": !1 }, scopedSlots: t._u([{ key: "md-autocomplete-item", fn: function({ item: i, term: n }) {
    return [e("md-highlight-text", { attrs: { "md-term": n } }, [t._v(t._s(i))])];
  } }, { key: "md-autocomplete-empty", fn: function({ term: i }) {
    return [t._v(" No " + t._s(t.filterby) + ' matching "' + t._s(i) + '" were found. ')];
  } }]), model: { value: t.selectedText, callback: function(i) {
    t.selectedText = i;
  }, expression: "selectedText" } }, [e("label", [t._v("Filter Keyword")])]), e("div", { staticClass: "utility-margin-big viz-2-col" }, [e("div", { staticClass: "utility-align--right utility-margin-top" }), e("div", { staticClass: "utility-align--right utility-margin-top" }, [e("a", { staticClass: "btn-text btn-text--default", on: { click: function(i) {
    return i.preventDefault(), t.onCancel.apply(null, arguments);
  } } }, [t._v(" ← Exit")]), t._v("     "), e("a", { staticClass: "btn-text btn-text--default", on: { click: function(i) {
    return i.preventDefault(), t.onConfirm.apply(null, arguments);
  } } }, [t._v("Filter → ")])])])], 1)])])], 1);
}, p = [], v = /* @__PURE__ */ o(
  m,
  g,
  p,
  !1,
  null,
  null
);
const y = v.exports;
export {
  y as default
};
