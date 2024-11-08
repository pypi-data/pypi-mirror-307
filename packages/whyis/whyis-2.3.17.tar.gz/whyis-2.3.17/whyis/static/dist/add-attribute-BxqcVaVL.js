import { V as u, p as n, c as s, n as w } from "./main-CZEa_tPp.js";
const d = u.component("add-attribute", {
  props: ["uri", "hideButton"],
  data: function() {
    return {
      id: null,
      attribute: null,
      attributeName: null,
      useCustom: !1,
      customAttributeURI: null,
      query: null,
      awaitingResolve: !1,
      propertyList: [],
      value: null,
      datatype: null,
      language: null,
      status: !1,
      active: !1,
      datatypes: {
        null: {
          uri: null,
          label: "None",
          widget: "textarea"
        },
        "http://www.w3.org/2001/XMLSchema#string": {
          uri: "http://www.w3.org/2001/XMLSchema#string",
          label: "String",
          widget: "textarea"
        },
        "http://www.w3.org/2001/XMLSchema#date": {
          uri: "http://www.w3.org/2001/XMLSchema#date",
          label: "Date",
          widget: "date"
        },
        "http://www.w3.org/2001/XMLSchema#dateTime": {
          uri: "http://www.w3.org/2001/XMLSchema#dateTime",
          label: "DateTime",
          widget: "date"
        },
        "http://www.w3.org/2001/XMLSchema#integer": {
          uri: "http://www.w3.org/2001/XMLSchema#integer",
          label: "Integer",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#decimal": {
          uri: "http://www.w3.org/2001/XMLSchema#decimal",
          label: "Decimal",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#time": {
          uri: "http://www.w3.org/2001/XMLSchema#time",
          label: "Time",
          widget: "time"
        },
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML": {
          uri: "http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML",
          label: "HTML",
          widget: "textarea"
        },
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral": {
          uri: "http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral",
          label: "XML",
          widget: "textarea"
        },
        "http://www.w3.org/2001/XMLSchema#boolean": {
          uri: "http://www.w3.org/2001/XMLSchema#boolean",
          label: "Boolean",
          widget: "select",
          options: ["true", "false"]
        },
        "http://www.w3.org/2001/XMLSchema#byte": {
          uri: "http://www.w3.org/2001/XMLSchema#byte",
          label: "Byte",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#double": {
          uri: "http://www.w3.org/2001/XMLSchema#double",
          label: "Double",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#float": {
          uri: "http://www.w3.org/2001/XMLSchema#float",
          label: "Float",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#int": {
          uri: "http://www.w3.org/2001/XMLSchema#int",
          label: "Int",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#negativeInteger": {
          uri: "http://www.w3.org/2001/XMLSchema#negativeInteger",
          label: "Integer",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#positiveInteger": {
          uri: "http://www.w3.org/2001/XMLSchema#positiveInteger",
          label: "Integer",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#nonNegativeInteger": {
          uri: "http://www.w3.org/2001/XMLSchema#nonNegativeInteger",
          label: "Integer",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#nonPositiveInteger": {
          uri: "http://www.w3.org/2001/XMLSchema#nonPositiveInteger",
          label: "Integer",
          widget: "number"
        },
        "http://www.w3.org/2001/XMLSchema#short": {
          uri: "http://www.w3.org/2001/XMLSchema#short",
          label: "Short Integer",
          widget: "number"
        },
        "http://www.opengis.net/ont/geosparql#wktLiteral": {
          uri: "http://www.opengis.net/ont/geosparql#wktLiteral",
          label: "WKT Geometry",
          widget: "textarea"
        },
        "http://www.opengis.net/ont/geosparql#gmlLiteral": {
          uri: "http://www.opengis.net/ont/geosparql#gmlLiteral",
          label: "GML Geometry",
          widget: "textarea"
        }
      }
    };
  },
  methods: {
    showSuggestedAttributes() {
      this.processAutocompleteMenu();
    },
    useCustomURI() {
      this.useCustom = !0, this.attribute = "Custom attribute";
    },
    resolveAttribute(i) {
      var t = this;
      this.query = i, t.awaitingResolve || setTimeout(function() {
        console.log(t.query), t.query.label || (t.query.length > 2 ? t.propertyList = t.getAttributeList(t.query) : t.propertyList = t.getSuggestedAttributes(t.uri)), t.awaitingResolve = !1;
      }, 1e3), t.awaitingResolve = !0;
    },
    selectedAttributeChange(i) {
      this.attribute = i, console.log(i), i.range && this.datatypes[i.range] && (this.datatype = this.datatypes[i.range]), console.log(this);
    },
    selectedDatatypeChange(i) {
      console.log(this);
    },
    // Create dialog boxes
    showDialogBox() {
      this.propertyList = this.getSuggestedAttributes(this.uri), this.active = !0;
    },
    resetDialogBox() {
      this.active = !this.active, this.attribute = null, this.attributeName = null, this.useCustom = !1, this.customAttributeURI = null, this.value = null, this.language = null, this.datatype = null;
    },
    onCancel() {
      return this.resetDialogBox();
    },
    onSubmit() {
      return this.saveAttribute().then(() => window.location.reload()), this.resetDialogBox();
    },
    async saveAttribute() {
      let i = Promise.resolve(), t = {
        "@id": this.uri
      };
      this.datatype && (this.language = null), this.attribute.node ? t[this.attribute.node] = {
        "@value": this.value,
        "@lang": this.language,
        "@type": this.datatype
      } : this.customAttributeURI && (t[this.customAttributeURI] = {
        "@value": this.value,
        "@lang": this.language,
        "@type": this.datatype
      }), console.log(t), await i;
      try {
        return n(t);
      } catch (e) {
        return alert(e);
      }
    },
    // Formats the dropdown menu. Runs only while the menu is open
    processAutocompleteMenu(i) {
      if (document.getElementsByClassName("md-menu-content-bottom-start").length >= 1)
        return status = !0;
    },
    async getSuggestedAttributes(i) {
      return (await s.get(
        `${ROOT_URL}about?view=suggested_attributes&uri=${i}`
      )).data;
    },
    async getAttributeList(i) {
      var t = [];
      const [e, a] = await s.all([
        s.get(
          `${ROOT_URL}about?term=*${i}*&view=resolve&type=http://www.w3.org/1999/02/22-rdf-syntax-ns%23Property`
        ),
        s.get(
          `${ROOT_URL}about?term=*${i}*&view=resolve&type=http://www.w3.org/2002/07/owl%23DatatypeProperty`
        )
      ]).catch((r) => {
        throw r;
      });
      return t = a.data.concat(e.data).sort((r, o) => r.score < o.score ? 1 : -1), this.groupBy(t, "node");
    },
    // Group entries by the value of a particular key
    groupBy(i, t) {
      let e = i.reduce(function(l, r) {
        return l[r[t]] = l[r[t]] || r, l;
      }, {});
      var a = Object.keys(e).map(function(l) {
        return e[l];
      });
      return a;
    }
  },
  created: function() {
    this.hideButton && (this.active = !0);
  }
});
var g = function() {
  var t = this, e = t._self._c;
  return t._self._setupProxy, e("div", [t.hideButton ? t._e() : e("div", { on: { click: t.showDialogBox } }, [t._t("default", function() {
    return [e("button", { staticClass: "md-button-icon" }, [e("i", [t._v("+ Add attribute")]), e("md-tooltip", [t._v("Add data about this entity.")])], 1)];
  })], 2), e("div", [e("md-dialog", { attrs: { "md-active": t.active, "md-click-outside-to-close": !0 }, on: { "update:mdActive": function(a) {
    t.active = a;
  }, "update:md-active": function(a) {
    t.active = a;
  } } }, [e("div", { staticClass: "utility-dialog-box_header" }, [e("md-dialog-title", [t._v(" New Attribute")])], 1), e("div", { staticStyle: { margin: "20px" } }, [e("div", { staticClass: "md-layout md-gutter" }, [e("div", { staticClass: "md-layout-item" }, [e("md-autocomplete", { attrs: { value: t.attributeName, "md-options": t.propertyList, "md-open-on-focus": !0 }, on: { "md-changed": t.resolveAttribute, "md-selected": t.selectedAttributeChange, "md-opened": t.showSuggestedAttributes }, scopedSlots: t._u([{ key: "md-autocomplete-item", fn: function({ item: a }) {
    return [a.preflabel ? e("label", { attrs: { "md-term": "term", "md-fuzzy-search": "true" } }, [t._v(" " + t._s(a.preflabel) + " ")]) : e("label", { attrs: { "md-term": "term", "md-fuzzy-search": "true" } }, [t._v(" " + t._s(a.label) + " ")]), e("md-tooltip", [t._v(t._s(a.node) + t._s(a.property))])];
  } }, { key: "md-autocomplete-empty", fn: function({ term: a }) {
    return [a ? e("p", [t._v('No attributes matching "' + t._s(a) + '" were found.')]) : e("p", [t._v("Type a property name.")]), e("a", { staticStyle: { cursor: "pointer" }, on: { click: t.useCustomURI } }, [t._v("Use a custom attribute URI")])];
  } }]) }, [e("label", [t._v("Attribute")])])], 1), e("div", { staticClass: "md-layout-item md-size-20" }, [e("md-field", [e("label", [t._v("Data type")]), e("md-select", { attrs: { name: "datatype" }, on: { "md-selected": t.selectedDatatypeChange }, model: { value: t.datatype, callback: function(a) {
    t.datatype = a;
  }, expression: "datatype" } }, t._l(t.datatypes, function(a) {
    return e("md-option", { key: a.uri, attrs: { value: a.uri } }, [t._v(" " + t._s(a.label) + " ")]);
  }), 1)], 1)], 1), t.datatype ? t._e() : e("div", { staticClass: "md-layout-item md-size-20" }, [e("md-field", [e("label", [t._v("Language")]), e("md-input", { model: { value: t.language, callback: function(a) {
    t.language = a;
  }, expression: "language" } })], 1)], 1)]), t.useCustom ? e("div", { staticClass: "md-layout md-gutter" }, [e("div", { staticClass: "md-layout-item" }, [e("md-field", [e("label", [t._v("Full URI of attribute")]), e("md-input", { model: { value: t.customAttributeURI, callback: function(a) {
    t.customAttributeURI = a;
  }, expression: "customAttributeURI" } })], 1)], 1)]) : t._e(), t.attribute ? e("div", { staticClass: "md-layout md-gutter" }, [e("div", { staticClass: "md-layout-item" }, [e("md-field", [t.attribute.label ? e("label", [t._v(t._s(t.attribute.label))]) : e("label", [t._v("Value")]), t.datatype == null || t.datatypes[t.datatype].widget == "textarea" ? e("md-textarea", { attrs: { "md-autogrow": "" }, model: { value: t.value, callback: function(a) {
    t.value = a;
  }, expression: "value" } }) : e("md-input", { attrs: { type: t.datatypes[t.datatype].widget }, model: { value: t.value, callback: function(a) {
    t.value = a;
  }, expression: "value" } })], 1)], 1)]) : t._e(), e("div", { staticClass: "utility-margin-big viz-2-col" }, [e("div", { staticClass: "utility-align--right utility-margin-top" }), e("div", { staticClass: "utility-align--right utility-margin-top" }, [e("md-button", { staticClass: "md-raised", on: { click: function(a) {
    return a.preventDefault(), t.onCancel.apply(null, arguments);
  } } }, [t._v(" Cancel ")]), e("md-button", { staticClass: "md-raised", on: { click: function(a) {
    return a.preventDefault(), t.onSubmit.apply(null, arguments);
  } } }, [t._v(" Add Attribute ")])], 1)])])])], 1)]);
}, c = [], m = /* @__PURE__ */ w(
  d,
  g,
  c,
  !1,
  null,
  null
);
const h = m.exports;
export {
  h as default
};
