import { V as l, c as s, n as r } from "./main-CZEa_tPp.js";
var o = [
  { mimetype: "application/rdf+xml", name: "RDF/XML", extensions: ["rdf"] },
  { mimetype: "application/ld+json", name: "JSON-LD", extensions: ["json", "jsonld"] },
  { mimetype: "text/turtle", name: "Turtle", extensions: ["ttl"] },
  { mimetype: "application/trig", name: "TRiG", extensions: ["trig"] },
  { mimetype: "application/n-quads", name: "n-Quads", extensions: ["nq", "nquads"] },
  { mimetype: "application/n-triples", name: "N-Triples", extensions: ["nt", "ntriples"] }
], i = {};
o.forEach(function(n) {
  i[n.name] = n;
});
const m = l.component("upload-knowledge", {
  props: ["active"],
  data: function() {
    return {
      formats: o,
      file: { name: "" },
      format_map: i,
      format: null,
      fileobj: "",
      status: !1,
      awaitingResolve: !1,
      awaitingEntity: !1
    };
  },
  methods: {
    // Create dialog boxes
    showDialogBox() {
      this.active = !0;
    },
    resetDialogBox() {
      this.active = !1, this.$emit("update:active", !1);
    },
    onCancel() {
      return this.resetDialogBox();
    },
    onSubmit() {
      return this.save().then(() => window.location.reload()), this.resetDialogBox();
    },
    handleFileUpload(n) {
      console.log(n), this.fileobj = n[0];
    },
    async save() {
      let n = this.format;
      if (n == null) {
        let e = this.formats.filter((a) => a.extensions.filter((t) => this.fileobj.name.endsWith(t)));
        e.length > 0 && (console.log("setting format", e[0]), n = e[0]);
      } else
        n = this.format_map[this.format];
      console.log(this.format);
      try {
        const e = {
          method: "post",
          url: `${ROOT_URL}pub`,
          data: this.fileobj,
          headers: { "Content-Type": n.mimetype }
        };
        return console.log(e), s(e);
      } catch (e) {
        return alert(e);
      }
    }
  }
});
var c = function() {
  var e = this, a = e._self._c;
  return e._self._setupProxy, a("md-dialog", { attrs: { "md-active": e.active, "md-click-outside-to-close": !0 }, on: { "update:mdActive": function(t) {
    e.active = t;
  }, "update:md-active": function(t) {
    e.active = t;
  } } }, [a("div", { staticStyle: { margin: "2em" } }, [a("md-dialog-title", [e._v("Upload Knowledge")]), a("md-field", [a("label", [e._v("RDF File")]), a("md-file", { attrs: { placeholder: "Upload Knowledge in RDF" }, on: { "md-change": function(t) {
    return e.handleFileUpload(t);
  } }, model: { value: e.file.name, callback: function(t) {
    e.$set(e.file, "name", t);
  }, expression: "file.name" } })], 1), a("md-field", [a("label", [e._v("Format")]), a("md-select", { attrs: { required: !0, name: "format", id: "format" }, model: { value: e.format, callback: function(t) {
    e.format = t;
  }, expression: "format" } }, e._l(e.formats, function(t) {
    return a("md-option", { attrs: { value: t.name } }, [e._v(e._s(t.name))]);
  }), 1)], 1), a("md-dialog-actions", [a("md-button", { staticClass: "md-primary", on: { click: function(t) {
    return t.preventDefault(), e.onCancel.apply(null, arguments);
  } } }, [e._v(" Cancel ")]), a("md-button", { staticClass: "md-primary", on: { click: function(t) {
    return e.onSubmit();
  } } }, [e._v(" Add ")])], 1)], 1)]);
}, d = [], f = /* @__PURE__ */ r(
  m,
  c,
  d,
  !1,
  null,
  null
);
const p = f.exports;
export {
  p as default
};
