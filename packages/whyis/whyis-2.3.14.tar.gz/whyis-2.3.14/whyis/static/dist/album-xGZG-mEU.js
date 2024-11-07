import { V as i, c as o, n as r } from "./main-CZEa_tPp.js";
const l = i.component("album", {
  name: "album",
  props: {
    instancetype: {
      type: String,
      require: !0
    }
  },
  data() {
    return {
      results: [],
      loading: !1,
      loadError: !1,
      otherArgs: null,
      pageSize: 24
    };
  },
  watch: {},
  components: {},
  methods: {
    async loadPage() {
      if (this.results.length % this.pageSize > 0)
        return;
      const s = await o.get(
        `${ROOT_URL}about`,
        {
          params: {
            view: "instances",
            uri: this.instancetype,
            limit: this.pageSize,
            offset: this.results.length
          }
        }
      );
      this.results.push(...s.data);
    },
    async scrollBottom() {
      Math.ceil(window.innerHeight + window.scrollY) >= document.body.offsetHeight && await this.loadPage();
    }
  },
  async mounted() {
    window.addEventListener("scroll", this.scrollBottom), this.loading = !0, await this.loadPage(), this.loading = !1;
  },
  async unmounted() {
    window.removeEventListener("scroll", this.scrollBottom);
  },
  created() {
  }
});
var c = function() {
  var t = this, e = t._self._c;
  return t._self._setupProxy, e("div", {}, [t.loading ? e("spinner", { attrs: { loading: t.loading, text: "Loading..." } }) : e("div", [e("div", { staticClass: "album" }, t._l(t.results, function(a, n) {
    return e("kgcard", { key: n, attrs: { entity: a } });
  }), 1)])], 1);
}, d = [], u = /* @__PURE__ */ r(
  l,
  c,
  d,
  !1,
  null,
  "8d49e3f2"
);
const h = u.exports;
export {
  h as default
};
