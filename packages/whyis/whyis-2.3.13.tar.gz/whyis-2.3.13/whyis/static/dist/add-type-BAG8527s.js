import { V as l, p as u, c as n, n as c } from "./main-C6jnxO2g.js";
const p = l.component("add-type", {
  props: ["uri", "hideButton"],
  data: function() {
    return {
      id: null,
      useCustom: !1,
      customTypeURI: null,
      typeList: [],
      selectedType: null,
      typeChips: [],
      status: !1,
      active: !1,
      query: null,
      awaitingResolve: !1
    };
  },
  methods: {
    showSuggestedTypes() {
      this.processAutocompleteMenu(), this.typeList = this.getSuggestedTypes(this.uri);
    },
    useCustomURI() {
      this.useCustom = !0;
    },
    submitCustomURI() {
      var i = {
        label: this.customTypeURI,
        node: this.customTypeURI
      };
      this.typeChips.push(i), this.customTypeURI = "", this.useCustom = !1;
    },
    resolveEntityType(i) {
      var t = this;
      this.query = i, t.awaitingResolve || setTimeout(function() {
        console.log(t.query), t.typeList = t.getTypeList(t.query), t.awaitingResolve = !1;
      }, 1e3), t.awaitingResolve = !0;
    },
    selectedTypeChange(i) {
      this.typeChips.push(i);
    },
    // Create dialog boxes
    showDialogBox() {
      this.active = !0;
    },
    removeChip(i) {
      this.typeChips.splice(i, 1);
    },
    resetDialogBox() {
      this.active = !this.active, this.typeChips = [], this.customTypeURI = "", this.useCustom = !1;
    },
    onCancel() {
      return this.resetDialogBox();
    },
    onSubmit() {
      return this.saveNewTypes().then(() => window.location.reload()), this.resetDialogBox();
    },
    async saveNewTypes() {
      let i = Promise.resolve();
      const t = this.processTypeChips(), e = {
        "@id": this.uri,
        "@type": t
      };
      await i;
      try {
        return u(e);
      } catch (s) {
        return alert(s);
      }
    },
    processTypeChips() {
      var i = this.typeChips;
      return Object.keys(i).map(function(t, e) {
        i[t].node && (i[t] = i[t].node);
      }), i;
    },
    // Formats the dropdown menu. Runs only while the menu is open
    processAutocompleteMenu(i) {
      if (document.getElementsByClassName("md-menu-content-bottom-start").length >= 1)
        return status = !0;
    },
    async getSuggestedTypes(i) {
      return (await n.get(
        `${ROOT_URL}about?view=suggested_types&uri=${i}`
      )).data;
    },
    async getTypeList(i) {
      var t = [];
      const [e, s] = await n.all([
        n.get(
          `${ROOT_URL}about?term=${i}*&view=resolve&type=http://www.w3.org/2000/01/rdf-schema%23Class`
        ),
        n.get(
          `${ROOT_URL}about?term=${i}*&view=resolve&type=http://www.w3.org/2002/07/owl%23Class`
        )
      ]).catch((a) => {
        throw a;
      });
      return t = s.data.concat(e.data).sort((a, r) => a.score < r.score ? 1 : -1), this.groupBy(t, "node");
    },
    // Group entries by the value of a particular key
    groupBy(i, t) {
      let e = i.reduce(function(o, a) {
        return o[a[t]] = o[a[t]] || a, o;
      }, {});
      var s = Object.keys(e).map(function(o) {
        return e[o];
      });
      return s;
    }
  },
  created: function() {
    this.hideButton && (this.active = !0);
  }
});
var d = function() {
  var t = this, e = t._self._c;
  return t._self._setupProxy, e("div", [t.hideButton ? t._e() : e("div", { on: { click: t.showDialogBox } }, [t._t("default", function() {
    return [e("button", { staticClass: "md-button-icon", staticStyle: { border: "none", background: "transparent" } }, [e("i", [t._v("+ Add type(s)")]), e("md-tooltip", [t._v("Specify additional type, subclass, or superclass.")])], 1)];
  })], 2), e("div", [e("md-dialog", { attrs: { "md-active": t.active, "md-click-outside-to-close": !0 }, on: { "update:mdActive": function(s) {
    t.active = s;
  }, "update:md-active": function(s) {
    t.active = s;
  } } }, [e("div", { staticClass: "utility-dialog-box_header" }, [e("md-dialog-title", [t._v(" Specify additional types/classes")])], 1), e("div", { staticStyle: { margin: "20px" } }, [e("md-autocomplete", { attrs: { value: t.selectedType, "md-options": t.typeList, "md-open-on-focus": !0 }, on: { "md-changed": t.resolveEntityType, "md-selected": t.selectedTypeChange, "md-opened": t.showSuggestedTypes, "md-closed": function(s) {
    return t.processAutocompleteMenu(!0);
  } }, scopedSlots: t._u([{ key: "md-autocomplete-item", fn: function({ item: s }) {
    return [s.preflabel ? e("label", { attrs: { "md-term": "term", "md-fuzzy-search": "true" } }, [t._v(" " + t._s(s.preflabel) + " ")]) : e("label", { attrs: { "md-term": "term", "md-fuzzy-search": "true" } }, [t._v(" " + t._s(s.label) + " ")]), e("md-tooltip", [t._v(t._s(s.node) + t._s(s.property))])];
  } }, { key: "md-autocomplete-empty", fn: function({ term: s }) {
    return [s ? e("p", [t._v('No types or classes matching "' + t._s(s) + '" were found.')]) : e("p", [t._v(" Enter a type name.")]), e("a", { staticStyle: { cursor: "pointer" }, on: { click: t.useCustomURI } }, [t._v("Use a custom type URI")])];
  } }]) }, [e("label", [t._v("Search for types")])]), t.useCustom ? e("div", { staticClass: "md-layout md-gutter" }, [e("div", { staticClass: "md-layout-item" }, [e("md-field", [e("label", [t._v("Full URI of type")]), e("md-input", { model: { value: t.customTypeURI, callback: function(s) {
    t.customTypeURI = s;
  }, expression: "customTypeURI" } }), e("md-button", { staticClass: "md-raised", on: { click: t.submitCustomURI } }, [t._v(" Confirm URI ")])], 1)], 1)]) : t._e(), t._l(t.typeChips, function(s, o) {
    return e("div", { key: o + "chips" }, [e("md-chip", { staticClass: "md-layout md-alignment-center-left", staticStyle: { "margin-bottom": "4px", "max-width": "fit-content" }, model: { value: t.typeChips[o], callback: function(a) {
      t.$set(t.typeChips, o, a);
    }, expression: "typeChips[key]" } }, [e("div", { staticClass: "md-layout-item", staticStyle: { "max-width": "fit-content" } }, [t.typeChips[o].preflabel ? e("div", [t._v(" " + t._s(t.typeChips[o].preflabel) + " ")]) : e("div", [t._v(" " + t._s(t.typeChips[o].label) + " ")])]), e("div", { staticClass: "md-layout-item", staticStyle: { "max-width": "fit-content" } }, [e("button", { staticStyle: { border: "none", "border-radius": "50%", "margin-left": "4px" }, on: { click: function(a) {
      return t.removeChip(o);
    } } }, [t._v("x")])])])], 1);
  }), e("div", { staticClass: "utility-margin-big viz-2-col" }, [e("div", { staticClass: "utility-align--right utility-margin-top" }), e("div", { staticClass: "utility-align--right utility-margin-top" }, [e("md-button", { staticClass: "md-raised", on: { click: function(s) {
    return s.preventDefault(), t.onCancel.apply(null, arguments);
  } } }, [t._v(" Cancel ")]), e("md-button", { staticClass: "md-raised", on: { click: function(s) {
    return s.preventDefault(), t.onSubmit.apply(null, arguments);
  } } }, [t._v(" Submit ")])], 1)])], 2)])], 1)]);
}, m = [], y = /* @__PURE__ */ c(
  p,
  d,
  m,
  !1,
  null,
  null
);
const v = y.exports;
export {
  v as default
};
