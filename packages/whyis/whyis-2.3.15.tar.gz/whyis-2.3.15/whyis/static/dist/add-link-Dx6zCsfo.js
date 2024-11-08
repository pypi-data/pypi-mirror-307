import { V as l, p as u, c as n, n as p } from "./main-CZEa_tPp.js";
const c = l.component("add-link", {
  props: ["uri", "hideButton"],
  data: function() {
    return {
      id: null,
      property: null,
      propertyName: null,
      propertyQuery: null,
      propertyList: [],
      useCustom: !1,
      customPropertyURI: null,
      entity: null,
      entityName: null,
      entityQuery: null,
      entityList: [],
      status: !1,
      active: !1,
      awaitingResolve: !1,
      awaitingEntity: !1
    };
  },
  methods: {
    useCustomURI() {
      this.useCustom = !0, this.property = "Custom attribute";
    },
    // property selection methods
    showSuggestedProperties() {
      this.processAutocompleteMenu(), this.propertyList = this.getSuggestedProperties(this.uri);
    },
    resolveProperty(s) {
      var t = this;
      this.propertyQuery = s, t.awaitingResolve || setTimeout(function() {
        console.log(t.propertyQuery), s.label || (t.propertyList = t.getPropertyList(t.propertyQuery)), t.awaitingResolve = !1;
      }, 1e3), t.awaitingResolve = !0;
    },
    selectedPropertyChange(s) {
      this.property = s, s.preflabel ? this.propertyName = s.preflabel : this.propertyName = s.label, console.log(s);
    },
    // entity selection methods
    showNeighborEntities() {
      this.processAutocompleteMenu(), this.entityList = this.getNeighborEntities(this.uri);
    },
    resolveEntity(s) {
      var t = this;
      this.entityQuery = s, t.awaitingEntity || setTimeout(function() {
        let e = t.entityQuery;
        e.label || (e.length > 2 ? t.entityList = t.getEntityList(e) : t.entityList = t.getNeighborEntities(t.uri)), t.awaitingEntity = !1;
      }, 1e3), t.awaitingEntity = !0;
    },
    selectedEntityChange(s) {
      this.entity = s, this.entityName = s.label, console.log(s);
    },
    // Create dialog boxes
    showDialogBox() {
      this.propertyList = this.getSuggestedProperties(this.uri), this.active = !0;
    },
    resetDialogBox() {
      this.active = !this.active, this.property = null, this.propertyName = null, this.useCustom = !1, this.customPropertyURI = null, this.entity = null, this.entityName = null;
    },
    onCancel() {
      return this.resetDialogBox();
    },
    onSubmit() {
      return this.saveLink().then(() => window.location.reload()), this.resetDialogBox();
    },
    async saveLink() {
      let s = Promise.resolve(), t = {
        "@id": this.uri
      }, e = this.entity.node;
      this.entity.uri && (e = this.entity.uri);
      let i = null;
      this.property.node ? i = this.property.node : this.property.property ? i = this.property.property : this.customPropertyURI && (i = this.customPropertyURI), t[i] = {
        "@id": e
      }, console.log(t), await s;
      try {
        return u(t);
      } catch (r) {
        return alert(r);
      }
    },
    // Formats the dropdown menu. Runs only while the menu is open
    processAutocompleteMenu(s) {
      if (document.getElementsByClassName("md-menu-content-bottom-start").length >= 1)
        return status = !0;
    },
    async getSuggestedProperties(s) {
      return (await n.get(
        `${ROOT_URL}about?view=suggested_links&uri=${s}`
      )).data.outgoing;
    },
    async getPropertyList(s) {
      var t = [];
      const [e, i] = await n.all([
        n.get(
          `${ROOT_URL}about?term=*${s}*&view=resolve&type=http://www.w3.org/1999/02/22-rdf-syntax-ns%23Property`
        ),
        n.get(
          `${ROOT_URL}about?term=*${s}*&view=resolve&type=http://www.w3.org/2002/07/owl%23ObjectProperty`
        )
      ]).catch((o) => {
        throw o;
      });
      return t = i.data.concat(e.data).sort((o, a) => o.score < a.score ? 1 : -1), this.groupBy(t, "node");
    },
    async getNeighborEntities(s) {
      return (await n.get(
        `${ROOT_URL}about?view=neighbors&uri=${s}`
      )).data;
    },
    async getEntityList(s) {
      return (await n.get(
        `${ROOT_URL}about?term=*${s}*&view=resolve`
      )).data;
    },
    // Group entries by the value of a particular key
    groupBy(s, t) {
      let e = s.reduce(function(r, o) {
        return r[o[t]] = r[o[t]] || o, r;
      }, {});
      var i = Object.keys(e).map(function(r) {
        return e[r];
      });
      return i;
    }
  },
  created: function() {
    this.hideButton && (this.active = !0);
  }
});
var d = function() {
  var t = this, e = t._self._c;
  return t._self._setupProxy, e("div", [t.hideButton ? t._e() : e("div", { on: { click: t.showDialogBox } }, [t._t("default", function() {
    return [e("button", { staticClass: "md-button-icon" }, [e("i", [t._v("+ Add Link")]), e("md-tooltip", [t._v("Add a link to another entity.")])], 1)];
  })], 2), e("div", [e("md-dialog", { attrs: { "md-active": t.active, "md-click-outside-to-close": !0 }, on: { "update:mdActive": function(i) {
    t.active = i;
  }, "update:md-active": function(i) {
    t.active = i;
  } } }, [e("div", { staticClass: "utility-dialog-box_header" }, [e("md-dialog-title", [t._v("New Link")])], 1), e("div", { staticStyle: { margin: "20px" } }, [e("div", { staticClass: "md-layout md-gutter" }, [e("div", { staticClass: "md-layout-item" }, [e("md-autocomplete", { attrs: { value: t.propertyName, "md-options": t.propertyList, "md-open-on-focus": !0 }, on: { "md-changed": t.resolveProperty, "md-selected": t.selectedPropertyChange, "md-opened": t.showSuggestedProperties }, scopedSlots: t._u([{ key: "md-autocomplete-item", fn: function({ item: i }) {
    return [i.preflabel ? e("label", { attrs: { "md-term": "term", "md-fuzzy-search": "true" } }, [t._v(" " + t._s(i.preflabel) + " ")]) : e("label", { attrs: { "md-term": "term", "md-fuzzy-search": "true" } }, [t._v(" " + t._s(i.label) + " ")]), e("md-tooltip", [t._v(t._s(i.node) + t._s(i.property))])];
  } }, { key: "md-autocomplete-empty", fn: function({ term: i }) {
    return [i ? e("p", [t._v('No link types matching "' + t._s(i) + '" were found.')]) : e("p", [t._v("Type a property name.")]), e("a", { staticStyle: { cursor: "pointer" }, on: { click: t.useCustomURI } }, [t._v("Use a custom property URI")])];
  } }]) }, [e("label", [t._v("Link Type")])])], 1)]), t.useCustom ? e("div", { staticClass: "md-layout md-gutter" }, [e("div", { staticClass: "md-layout-item" }, [e("md-field", [e("label", [t._v("Full URI of property")]), e("md-input", { model: { value: t.customPropertyURI, callback: function(i) {
    t.customPropertyURI = i;
  }, expression: "customPropertyURI" } })], 1)], 1)]) : t._e(), t.property ? e("div", { staticClass: "md-layout md-gutter" }, [e("div", { staticClass: "md-layout-item" }, [e("md-autocomplete", { attrs: { value: t.entityName, "md-options": t.entityList, "md-open-on-focus": !0 }, on: { "md-changed": t.resolveEntity, "md-selected": t.selectedEntityChange, "md-opened": t.showNeighborEntities }, scopedSlots: t._u([{ key: "md-autocomplete-item", fn: function({ item: i }) {
    return [i.preflabel ? e("label", { attrs: { "md-term": "term", "md-fuzzy-search": "true" } }, [t._v(" " + t._s(i.preflabel) + " (" + t._s(i.class_label) + ") ")]) : e("label", { attrs: { "md-term": "term", "md-fuzzy-search": "true" } }, [t._v(" " + t._s(i.label) + " (" + t._s(i.class_label) + ") ")]), e("md-tooltip", [t._v(t._s(i.node) + t._s(i.uri))])];
  } }, { key: "md-autocomplete-empty", fn: function({ term: i }) {
    return [i ? e("p", [t._v('No entities matching "' + t._s(i) + '" were found.')]) : e("p", [t._v("Type an entity name.")])];
  } }], null, !1, 2843475858) }, [t.propertyName ? e("label", [t._v(t._s(t.propertyName))]) : e("label", [t._v("Linked entity")])])], 1)]) : t._e(), e("div", { staticClass: "utility-margin-big viz-2-col" }, [e("div", { staticClass: "utility-align--right utility-margin-top" }), e("div", { staticClass: "utility-align--right utility-margin-top" }, [e("md-button", { staticClass: "md-raised", on: { click: function(i) {
    return i.preventDefault(), t.onCancel.apply(null, arguments);
  } } }, [t._v(" Cancel ")]), e("md-button", { staticClass: "md-raised", on: { click: function(i) {
    return i.preventDefault(), t.onSubmit.apply(null, arguments);
  } } }, [t._v(" Add Link ")])], 1)])])])], 1)]);
}, y = [], m = /* @__PURE__ */ p(
  c,
  d,
  y,
  !1,
  null,
  null
);
const g = m.exports;
export {
  g as default
};
