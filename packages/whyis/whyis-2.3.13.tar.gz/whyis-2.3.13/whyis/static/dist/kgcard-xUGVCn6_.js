import { V as l, b as i, S as d, n as c } from "./main-C6jnxO2g.js";
const o = l.component("kgcard", {
  name: "kgcard",
  props: {
    entity: {
      require: !0
    }
  },
  data() {
    return {};
  },
  methods: {
    getViewUrl(r, t) {
      return i(r, t);
    },
    navigate(r) {
      return window.location = i(r.identifier, "view");
    },
    reduceDescription(r) {
      if (r == null) return r;
      let t, e, a;
      return t = r.split(" "), t.splice(15), e = t.reduce((n, s) => `${n} ${s}`, ""), a = d(e), `${a}...`;
    }
  }
});
var m = function() {
  var t = this, e = t._self._c;
  return t._self._setupProxy, e("md-card", { staticClass: "btn--animated" }, [e("md-card-media-cover", { attrs: { "md-solid": "" }, nativeOn: { click: function(a) {
    return a.preventDefault(), t.navigate(t.entity);
  } } }, [e("md-card-media", { attrs: { "md-ratio": "4:3" } }, [t.entity.thumbnail ? e("img", { attrs: { src: t.getViewUrl(t.entity.thumbnail), alt: t.entity.label } }) : e("img", { attrs: { src: t.$root.$data.root_url + "static/images/rdf_flyer.svg", alt: t.entity.label } })]), e("md-card-area", { staticClass: "utility-gridbg" }, [e("md-card-header", { staticClass: "utility-show_hide" }, [e("span", { staticClass: "md-subheading" }, [e("strong", [t._v(t._s(t.entity.label))])]), e("span", { staticClass: "md-body-1" }, [t._v(t._s(t.entity.description))])])], 1)], 1)], 1);
}, u = [], _ = /* @__PURE__ */ c(
  o,
  m,
  u,
  !1,
  null,
  null
);
const f = _.exports;
export {
  f as default
};
