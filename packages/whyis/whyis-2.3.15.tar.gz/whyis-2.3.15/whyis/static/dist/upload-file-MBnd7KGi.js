import { V as o, n as l } from "./main-CZEa_tPp.js";
const i = o.component("upload-file", {
  props: ["active", "label"],
  data: function() {
    return {
      upload_type: "http://purl.org/net/provenance/ns#File"
    };
  },
  methods: {
    // Create dialog boxes
    showDialogBox() {
      this.$emit("update:active", !0);
    },
    resetDialogBox() {
      this.$emit("update:active", !1);
    },
    onCancel() {
      return this.resetDialogBox();
    },
    onSubmit() {
      return this.save().then(() => window.location.reload()), this.resetDialogBox();
    }
  }
});
var n = function() {
  var e = this, t = e._self._c;
  return e._self._setupProxy, t("md-dialog", { attrs: { "md-active": e.active, "md-click-outside-to-close": !0 }, on: { "update:mdActive": function(a) {
    e.active = a;
  }, "update:md-active": function(a) {
    e.active = a;
  }, "md-clicked-outside": function(a) {
    return e.resetDialogBox();
  } } }, [t("md-dialog-title", [e._v("Upload File for " + e._s(e.label))]), t("form", { staticStyle: { margin: "2em" }, attrs: { id: "upload_form", enctype: "multipart/form-data", novalidate: "", method: "post", action: "" } }, [t("p", [t("md-radio", { attrs: { name: "upload_type", checked: "", value: "http://purl.org/net/provenance/ns#File" }, model: { value: e.upload_type, callback: function(a) {
    e.upload_type = a;
  }, expression: "upload_type" } }, [e._v("Single File")]), t("md-radio", { attrs: { name: "upload_type", value: "http://purl.org/dc/dcmitype/Collection" }, model: { value: e.upload_type, callback: function(a) {
    e.upload_type = a;
  }, expression: "upload_type" } }, [e._v("Collection")]), t("md-radio", { attrs: { name: "upload_type", value: "http://www.w3.org/ns/dcat#Dataset" }, model: { value: e.upload_type, callback: function(a) {
    e.upload_type = a;
  }, expression: "upload_type" } }, [e._v("Dataset")])], 1), t("md-field", [t("label", [e._v("File")]), t("md-file", { attrs: { name: "file", multiple: "", placeholder: "Add files here." } })], 1)], 1), t("md-dialog-actions", [t("md-button", { staticClass: "md-primary", on: { click: function(a) {
    return e.resetDialogBox();
  } } }, [e._v("Close")]), t("md-button", { staticClass: "md-primary", attrs: { form: "upload_form", type: "submit" } }, [e._v("Upload")])], 1)], 1);
}, d = [], r = /* @__PURE__ */ l(
  i,
  n,
  d,
  !1,
  null,
  null
);
const u = r.exports;
export {
  u as default
};
