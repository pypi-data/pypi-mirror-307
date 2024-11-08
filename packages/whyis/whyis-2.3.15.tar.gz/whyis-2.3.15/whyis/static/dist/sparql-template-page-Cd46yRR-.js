import { q as T, y as I, z as f, i as S, k as _, D as q, o as w, n as R } from "./main-CZEa_tPp.js";
import { d as O } from "./debounce-BezZ7Sd5.js";
const x = "http://www.w3.org/1999/02/22-rdf-syntax-ns#", N = "http://www.w3.org/2000/01/rdf-schema#", d = "http://schema.org/";
loadSparqlTemplatesQuery = `
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX sp: <http://spinrdf.org/sp>
PREFIX spin: <http://spinrdf.org/spin#>
PREFIX spl: <http://spinrdf.org/spin#>
PREFIX whyis: <http://vocab.rpi.edu/whyis/>
PREFIX nanomine_templates: <http://nanomine.org/query/>

CONSTRUCT {
    ?template a whyis:SparqlTemplate  ;
        spin:labelTemplate ?labelTemplate ;
        sp:text ?query ;
        spin:constraint ?constraint .
    ?constraint sp:varName ?varName ;
        schema:option ?option .
    ?option rdfs:label ?optLabel ;
        schema:value ?optValue ;
        schema:identifier ?optId ;
        schema:position ?optPosition .
}
WHERE {
    ?template a whyis:SparqlTemplate  ;
        spin:labelTemplate ?labelTemplate ;
        sp:text ?query ;
        spin:constraint ?constraint .
    ?constraint sp:varName ?varName ;
        schema:option ?option .
    ?option rdfs:label ?optLabel ;
        schema:position ?optPosition .
    OPTIONAL { ?option schema:value ?optValue } .
    OPTIONAL { ?option schema:identifier ?optId } .
}
`;
const y = "http://spinrdf.org/sp", v = `${y}in#`, j = "http://vocab.rpi.edu/whyis/SparqlTemplate", C = x + "type";
async function P() {
  const a = await T(loadSparqlTemplatesQuery), e = {}, t = [];
  a.results.bindings.forEach((s) => {
    const n = s.subject.value, o = s.predicate.value;
    let p = s.object.value;
    s.object.type === "literal" && s.object.datatype && (p = I.fromRdf(f.literal(p, f.namedNode(s.object.datatype)))), o === C && p === j && t.push(n);
    let c = e[n];
    c || (c = {}, e[n] = c);
    let m = c[o];
    m || (m = /* @__PURE__ */ new Set(), c[o] = m), m.add(p);
  });
  const i = t.map((s) => l(s)).map(V);
  return i.sort((s, n) => s.id > n.id ? 1 : -1), i;
  function l(s, n) {
    if (n = n || /* @__PURE__ */ new Set(), n.has(s) || !e.hasOwnProperty(s))
      return s;
    n.add(s);
    const o = e[s], p = { uri: s };
    return Object.entries(o).forEach(([c, m]) => {
      const g = [...m].map((E) => l(E, n));
      p[c] = g;
    }), p;
  }
}
const h = Object.freeze({
  VAR: "var",
  TEXT: "text"
}), u = Object.freeze({
  ANY: "any",
  LITERAL: "literal",
  IDENTIFIER: "identifier"
});
function V(a) {
  const e = a[`${v}labelTemplate`][0];
  return {
    id: a.uri,
    display: e,
    displaySegments: k(e),
    SPARQL: a[`${y}text`][0],
    options: $(a[`${v}constraint`])
  };
}
function $(a) {
  return Object.fromEntries(
    a.map((e) => [
      e[`${y}varName`][0],
      A(e[`${d}option`])
    ])
  );
}
function A(a) {
  return Object.fromEntries(
    a.map((e) => [
      e[`${N}label`][0],
      Q(e),
      e[`${d}position`][0]
    ]).sort((e, t) => e[2] > t[2] ? 1 : -1)
  );
}
function Q(a) {
  let e = {
    type: u.ANY
  };
  return a[`${d}value`] ? (a[`${d}value`], e = {
    type: u.LITERAL,
    value: a[`${d}value`][0]
  }) : a[`${d}identifier`] && (e = {
    type: u.IDENTIFIER,
    value: a[`${d}identifier`][0]
  }), e;
}
const b = /{\?([^}]+)}/g, L = new RegExp(`${b.source}|[^{]+`, "g");
function k(a) {
  return a.match(L).map((e) => {
    let t;
    const r = b.exec(e);
    return r ? t = {
      type: h.VAR,
      varName: r[1]
    } : t = {
      type: h.TEXT,
      text: e
    }, t;
  });
}
const F = {
  data() {
    return {
      loadingTemplates: !0,
      queryTemplates: {},
      TextSegmentType: h,
      selTemplateId: null,
      query: "",
      varSelections: {},
      results: null,
      execQueryDebounced: O(this.execQuery, 300)
    };
  },
  computed: {
    templateIds() {
      return Object.keys(this.queryTemplates);
    },
    selectedTemplate() {
      return this.queryTemplates[this.selTemplateId];
    },
    currentIndex() {
      return this.templateIds.indexOf(this.selTemplateId);
    },
    totalTemplateCount() {
      return this.templateIds.length;
    }
  },
  methods: {
    ...S("vizEditor", ["setQuery"]),
    selectQueryForVizEditor() {
      this.setQuery(this.query), this.toVizEditor();
    },
    toVizEditor() {
      _(w.CHART_EDITOR, q.NEW);
    },
    async loadSparqlTemplates() {
      this.loadingTemplates = !0;
      try {
        const a = await P();
        this.queryTemplates = {}, a.forEach((e) => this.queryTemplates[e.id] = e), console.log("qtemps", this.queryTemplates), this.selTemplateId = a.length > 0 ? a[0].id : null;
      } finally {
        this.loadingTemplates = !1;
      }
    },
    shiftTemplate(a) {
      let e = this.currentIndex + a;
      for (; e >= this.totalTemplateCount; )
        e -= this.totalTemplateCount;
      for (; e < 0; )
        e += this.totalTemplateCount;
      this.selTemplateId = this.templateIds[e], console.log("shifted", e, this.selTemplateId, this.templateIds);
    },
    populateSelections() {
      this.selectedTemplate && (this.varSelections = Object.fromEntries(
        Object.entries(
          this.selectedTemplate.options
        ).map(([a, e]) => [a, Object.keys(e)[0]])
      ));
    },
    getOptVal(a, e) {
      return this.selectedTemplate.options[a][e];
    },
    buildQuery() {
      if (!this.selectedTemplate)
        return;
      this.query = this.selectedTemplate.SPARQL, this.selectedTemplate.options;
      const a = Object.fromEntries(
        Object.entries(this.varSelections).filter((e) => this.getOptVal(...e).type !== u.ANY)
      );
      if (Object.keys(a).length > 0) {
        const e = Object.keys(a).map((r) => `?${r}`).join(" "), t = Object.entries(a).map((r) => {
          const i = this.getOptVal(...r);
          let l;
          if (i.type === u.LITERAL)
            l = i.value, typeof l != "number" && (l = `"${l}"`);
          else if (i.type === u.IDENTIFIER)
            l = `<${i.value}>`;
          else
            throw `Unknown option value type: ${i.type}`;
          return l;
        }).join(" ");
        this.query += `
VALUES (${e}) {
  (${t})
}
`;
      }
    },
    async execQuery() {
      console.log("querying...."), this.results = null, this.results = await T(this.query), console.log("done", this.results);
    }
  },
  created() {
    this.loadSparqlTemplates();
  },
  watch: {
    // The following reactive watchers are used due to limitations of not being
    // able to deep watch dependencies of computed methods.
    selectedTemplate: {
      handler: "populateSelections"
    },
    varSelections: {
      handler: "buildQuery",
      deep: !0
    },
    query: {
      handler: "execQueryDebounced"
    }
  }
};
var D = function() {
  var e = this, t = e._self._c;
  return t("div", { staticClass: "sparql-template-page" }, [e.loadingTemplates ? t("div", [t("md-progress-spinner", { attrs: { "md-mode": "indeterminate" } })], 1) : e.totalTemplateCount === 0 ? t("div", [t("p", [e._v("No templates were loaded")])]) : t("div", [t("div", { staticClass: "button-row" }, [t("div", [t("md-button", { staticClass: "md-icon-button", nativeOn: { click: function(r) {
    return r.preventDefault(), e.selectQueryForVizEditor();
  } } }, [t("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "bottom" } }, [e._v(" Select current query and return to Viz Editor ")]), t("md-icon", [e._v("check")])], 1), t("md-button", { staticClass: "md-icon-button", nativeOn: { click: function(r) {
    return r.preventDefault(), e.toVizEditor();
  } } }, [t("md-tooltip", { staticClass: "utility-bckg", attrs: { "md-direction": "bottom" } }, [e._v(" Return to viz editor ")]), t("md-icon", [e._v("arrow_back")])], 1)], 1)]), t("md-toolbar", [t("h3", { staticClass: "md-title" }, [e._v("Query Template")])]), t("div", { staticClass: "display" }, [t("md-button", { staticClass: "template-back", on: { click: function(r) {
    return e.shiftTemplate(-1);
  } } }, [t("md-icon", [e._v("chevron_left")])], 1), t("md-button", { staticClass: "template-next", on: { click: function(r) {
    return e.shiftTemplate(1);
  } } }, [t("md-icon", [e._v("chevron_right")])], 1), t("p", { staticClass: "display-text" }, e._l(e.selectedTemplate.displaySegments, function(r, i) {
    return t("span", { key: i }, [r.type == e.TextSegmentType.TEXT ? t("span", { domProps: { innerHTML: e._s(r.text) } }) : t("span", [t("select", { directives: [{ name: "model", rawName: "v-model", value: e.varSelections[r.varName], expression: "varSelections[segment.varName]" }], attrs: { id: r.varName, name: r.varName }, on: { change: function(l) {
      var s = Array.prototype.filter.call(l.target.options, function(n) {
        return n.selected;
      }).map(function(n) {
        var o = "_value" in n ? n._value : n.value;
        return o;
      });
      e.$set(e.varSelections, r.varName, l.target.multiple ? s : s[0]);
    } } }, e._l(e.selectedTemplate.options[r.varName], function(l, s) {
      return t("option", { key: s, domProps: { value: s } }, [e._v(" " + e._s(s) + " ")]);
    }), 0)])]);
  }), 0)], 1), t("div", { staticClass: "display-count-indicator" }, [t("p", [e._v("Query template " + e._s(e.currentIndex + 1) + " of " + e._s(e.totalTemplateCount))])]), e.query ? t("div", { staticClass: "query" }, [t("accordion", { attrs: { startOpen: !1, title: "SPARQL Query" } }, [t("yasqe", { attrs: { value: e.query, readonly: "true" } })], 1)], 1) : e._e(), t("div", { staticClass: "results" }, [t("accordion", { attrs: { startOpen: !0, title: "SPARQL Results" } }, [e.results ? t("div", [t("yasr", { attrs: { results: e.results } })], 1) : t("md-progress-spinner", { attrs: { "md-diameter": 30, "md-stroke": 3, "md-mode": "indeterminate" } })], 1)], 1)], 1)]);
}, z = [], X = /* @__PURE__ */ R(
  F,
  D,
  z,
  !1,
  null,
  "bfbba95d"
);
const H = X.exports;
export {
  H as default
};
