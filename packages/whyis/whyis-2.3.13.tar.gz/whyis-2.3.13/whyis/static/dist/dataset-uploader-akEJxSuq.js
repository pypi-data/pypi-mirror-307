import { g as Z, r as N, p as V, t as H, u as w, c, w as J, V as j, x as X, E as u, k as K, n as Q } from "./main-C6jnxO2g.js";
import { l as tt } from "./orcid-lookup-MufoY1S_.js";
var I = { exports: {} }, O = typeof crypto < "u" && crypto.getRandomValues && crypto.getRandomValues.bind(crypto) || typeof msCrypto < "u" && typeof window.msCrypto.getRandomValues == "function" && msCrypto.getRandomValues.bind(msCrypto);
if (O) {
  var E = new Uint8Array(16);
  I.exports = function() {
    return O(E), E;
  };
} else {
  var z = new Array(16);
  I.exports = function() {
    for (var t = 0, e; t < 16; t++)
      t & 3 || (e = Math.random() * 4294967296), z[t] = e >>> ((t & 3) << 3) & 255;
    return z;
  };
}
var M = I.exports, B = [];
for (var g = 0; g < 256; ++g)
  B[g] = (g + 256).toString(16).substr(1);
function et(a, t) {
  var e = t || 0, i = B;
  return [
    i[a[e++]],
    i[a[e++]],
    i[a[e++]],
    i[a[e++]],
    "-",
    i[a[e++]],
    i[a[e++]],
    "-",
    i[a[e++]],
    i[a[e++]],
    "-",
    i[a[e++]],
    i[a[e++]],
    "-",
    i[a[e++]],
    i[a[e++]],
    i[a[e++]],
    i[a[e++]],
    i[a[e++]],
    i[a[e++]]
  ].join("");
}
var G = et, at = M, it = G, L, S, x = 0, D = 0;
function st(a, t, e) {
  var i = t && e || 0, s = t || [];
  a = a || {};
  var n = a.node || L, o = a.clockseq !== void 0 ? a.clockseq : S;
  if (n == null || o == null) {
    var r = at();
    n == null && (n = L = [
      r[0] | 1,
      r[1],
      r[2],
      r[3],
      r[4],
      r[5]
    ]), o == null && (o = S = (r[6] << 8 | r[7]) & 16383);
  }
  var m = a.msecs !== void 0 ? a.msecs : (/* @__PURE__ */ new Date()).getTime(), p = a.nsecs !== void 0 ? a.nsecs : D + 1, F = m - x + (p - D) / 1e4;
  if (F < 0 && a.clockseq === void 0 && (o = o + 1 & 16383), (F < 0 || m > x) && a.nsecs === void 0 && (p = 0), p >= 1e4)
    throw new Error("uuid.v1(): Can't create more than 10M uuids/sec");
  x = m, D = p, S = o, m += 122192928e5;
  var f = ((m & 268435455) * 1e4 + p) % 4294967296;
  s[i++] = f >>> 24 & 255, s[i++] = f >>> 16 & 255, s[i++] = f >>> 8 & 255, s[i++] = f & 255;
  var h = m / 4294967296 * 1e4 & 268435455;
  s[i++] = h >>> 8 & 255, s[i++] = h & 255, s[i++] = h >>> 24 & 15 | 16, s[i++] = h >>> 16 & 255, s[i++] = o >>> 8 | 128, s[i++] = o & 255;
  for (var v = 0; v < 6; ++v)
    s[i + v] = n[v];
  return t || it(s);
}
var nt = st, ot = M, rt = G;
function dt(a, t, e) {
  var i = t && e || 0;
  typeof a == "string" && (t = a === "binary" ? new Array(16) : null, a = null), a = a || {};
  var s = a.random || (a.rng || ot)();
  if (s[6] = s[6] & 15 | 64, s[8] = s[8] & 63 | 128, t)
    for (var n = 0; n < 16; ++n)
      t[i + n] = s[n];
  return t || rt(s);
}
var lt = dt, ct = nt, Y = lt, U = Y;
U.v1 = ct;
U.v4 = Y;
var mt = U;
const W = /* @__PURE__ */ Z(mt), $ = {
  title: "",
  description: "",
  contactpoint: {
    "@type": "individual",
    "@id": null,
    name: "",
    cpfirstname: "",
    cplastname: "",
    cpemail: ""
  },
  contributor: [],
  author: [],
  datepub: {
    "@type": "date",
    "@value": ""
  },
  datemod: {
    "@type": "date",
    "@value": ""
  },
  refby: [],
  distribution: {
    accessURL: null
  },
  depiction: {
    name: "",
    accessURL: null
  }
}, R = "http://w3.org/ns/dcat#", l = "http://purl.org/dc/terms/", y = "http://www.w3.org/2006/vcard/ns#", b = "http://xmlns.com/foaf/0.1/", d = {
  baseSpec: "http://semanticscience.org/resource/hasValue",
  title: `${l}title`,
  description: `${l}description`,
  contactpoint: `${R}contactpoint`,
  cpemail: `${y}email`,
  cpfirstname: `${y}given-name`,
  cplastname: `${y}family-name`,
  individual: `${y}individual`,
  author: `${l}creator`,
  name: `${b}name`,
  contributor: `${l}contributor`,
  organization: `${b}Organization`,
  person: `${b}Person`,
  onbehalfof: "http://www.w3.org/ns/prov#actedOnBehalfOf",
  specializationOf: "http://www.w3.org/ns/prov#specializationOf",
  datepub: `${l}issued`,
  datemod: `${l}modified`,
  date: "https://www.w3.org/2001/XMLSchema#date",
  refby: `${l}isReferencedBy`,
  // distribution: `${dcat}distribution`,
  depiction: `${b}depiction`,
  hasContent: "http://vocab.rpi.edu/whyis/hasContent",
  accessURL: `${R}accessURL`
}, pt = "dataset";
function P(a) {
  var t;
  return arguments.length === 0 ? t = W() : t = a, `${w}/${pt}/${t}`;
}
function ut(a) {
  a = Object.assign({}, a), a.context = JSON.stringify(a.context);
  const t = {
    "@id": a.uri,
    "@type": []
  };
  return a["@type"] != null && t["@type"].push(a["@type"]), Object.entries(a).filter(([e, i]) => d[e]).forEach(([e, i]) => {
    var s = {};
    console.log(e), A(i) || (s = k([e, i]), t[d[e]] = [s]);
  }), t;
}
function A(a) {
  if (a === "" || a === null || a === [] || a === "undefined")
    return !0;
  if (Array.isArray(a)) {
    let i = a.length === 0;
    for (var t in a)
      i = i || A(a[t]);
    return i;
  } else if (typeof a == "object") {
    let i = !1;
    for (var e in a)
      i = i || A(a[e]);
    return i;
  }
  return !1;
}
function k([a, t]) {
  if (Array.isArray(t)) {
    var e = [];
    for (var i in t)
      e.push(k([a, t[i]]));
    return e;
  } else {
    var s = {};
    for (var i in t)
      i === "@type" || i === "@value" || i === "@id" ? (s[i] = t[i], d.hasOwnProperty(t[i]) && (s[i] = d[t[i]])) : d.hasOwnProperty(i) ? s[d[i]] = k([d[i], t[i]]) : s["@value"] = t;
    return s;
  }
}
function ft() {
  return Object.assign({}, $);
}
function ht(a, t) {
  return J(a).then((e) => {
    const i = `${a}_assertion`;
    for (let s of e)
      if (s["@id"] === i) {
        for (let n of s["@graph"])
          if (n["@id"] === t)
            return gt(n);
      }
  });
}
function vt(a) {
  return N(a).then((t) => {
    if (t.length > 0) {
      const e = t[0].np;
      return ht(e, a);
    }
  });
}
function gt(a) {
  const t = Object.assign({}, $);
  return Object.entries($).forEach(([e]) => {
    let i = d[e];
    var s = a[i];
    console.log(s), i in a && typeof s < "u" && (console.log(s[0]), typeof s[0]["@value"] < "u" && (t[e] = a[i][0]["@value"]));
  }), t;
}
async function yt(a, t) {
  let e = Promise.resolve();
  a.uri ? e = bt(a.uri) : arguments.length === 1 ? a.uri = P() : a.uri = P(t);
  const i = ut(a);
  await e;
  try {
    return V(i);
  } catch (s) {
    return alert(s);
  }
}
function bt(a) {
  return N(a).then(
    (t) => {
      console.log("in delete"), console.log(t.np), Promise.all(t.map((e) => H(e.np)));
    }
  );
}
async function _t(a, t) {
  let e = new FormData(), i = Array(a.length);
  e.append("upload_type", "http://www.w3.org/ns/dcat#Dataset"), Array.from(Array(a.length).keys()).map((o) => {
    e.append(a[o].label, a[o]), i[o] = {
      "@id": `${w}/dataset/${t}/${a[o].name.replace(/ /g, "_")}`,
      "http://www.w3.org/2000/01/rdf-schema#label": a[o].label
    };
  });
  const s = `${w}/dataset/${t}`, n = `${window.location.origin}/about?uri=${s}`;
  c.post(
    n,
    e,
    {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    }
  ), Array.from(Array(a.length).keys()).map((o) => {
    i[o]["http://www.w3.org/2000/01/rdf-schema#label"] != "" && V(i[o]);
  });
}
async function wt(a, t) {
  const e = `${w}/dataset/${t}/depiction`, i = `${window.location.origin}/about?uri=${e}`;
  let s = new FormData();
  s.append("upload_type", "http://purl.org/net/provenance/ns#File"), s.append("depiction", a);
  var n = {
    "@id": e,
    file: s
  };
  return await fetch(i, {
    method: "POST",
    body: n,
    headers: {
      Accept: "application/json",
      "Content-Type": "multipart/form-data"
    }
  }), [e, i];
}
async function St(a) {
  return await c.get(`/doi/${a}?view=describe`, {
    headers: {
      Accept: "application/json"
    }
  });
}
async function xt(a) {
  const t = await c.get(`/about?uri=${a}&view=describe`, {
    headers: {
      Accept: "application/json"
    }
  });
  var e = t.data;
  if ("@graph" in t.data)
    for (var i in t.data["@graph"])
      t.data["@graph"][i]["@id"] === a && (e = t.data["@graph"][i]);
  return e;
}
function Dt(a) {
  const t = document.getElementsByClassName("md-menu-content-bottom-start");
  if (t.length >= 1)
    return t[0].style["z-index"] = 12, t[0].style.width = "75%", t[0].style["max-width"] = "75%", status = !0;
}
async function Ct(a) {
  const [t, e] = await c.all([
    c.get(
      `/?term=${a}*&view=resolve&type=http://xmlns.com/foaf/0.1/Person`
    ),
    c.get(
      `/?term=${a}*&view=resolve&type=http://schema.org/Person`
    )
  ]).catch((s) => {
    throw s;
  });
  var i = t.data.concat(e.data).sort((s, n) => s.score < n.score ? 1 : -1);
  return i;
}
async function It(a) {
  return (await c.get(
    `/?term=${a}*&view=resolve&type=http://schema.org/Organization`
  )).data;
}
j.use(X);
const _ = 0, T = 1, q = 2, C = 3, $t = W(), At = j.component("dataset-uploader", {
  props: [
    "datasetType"
  ],
  data() {
    return {
      dataset: {
        "@type": this.datasetType,
        title: "",
        description: "",
        contactpoint: {
          "@type": "individual",
          "@id": null,
          name: "",
          cpfirstname: "",
          cplastname: "",
          cpemail: ""
        },
        contributor: [],
        author: [],
        datepub: {
          "@type": "date",
          "@value": ""
        },
        datemod: {
          "@type": "date",
          "@value": ""
        },
        refby: [],
        depiction: {
          name: "",
          accessURL: null,
          "@id": null,
          hasContent: null
        }
      },
      generatedUUID: $t,
      doi: "",
      doiLoading: !1,
      cpID: "",
      cpIDError: !1,
      contributors: [],
      distr_upload: [],
      rep_image: [],
      // Stepper data
      active: "first",
      first: !1,
      second: !1,
      third: !1,
      //handle uploads
      uploadedFiles: [],
      uploadedImg: [],
      uploadError: null,
      distrStatus: _,
      depictStatus: _,
      isInvalidUpload: !1,
      isInvalidForm: !1,
      authenticated: u.authUser,
      autocomplete: {
        availableInstitutions: [],
        availableAuthors: []
      },
      loading: !1,
      loadingText: "Loading Existing Datasets",
      /// search
      query: null,
      selectedAuthor: [],
      // TODO: deal with empty orgs
      editableOrgs: !0
    };
  },
  methods: {
    loadDataset() {
      let a;
      this.pageView === "new" ? a = Promise.resolve(ft()) : a = vt(this.pageUri), a.then((t) => {
        this.dataset = t, this.dataset["@type"] = this.datasetType, this.loading = !1;
      });
    },
    dateFormat(a, t) {
      return moment(a).format("YYYY-MM-DD");
    },
    removeElement: function(a) {
      this.contributors.splice(a, 1);
    },
    editDois: function() {
      this.doi !== "" && (this.dataset.refby = "https://dx.doi.org/" + this.doi);
    },
    /* 
      Contributor and author handling: User facing 
    */
    handleContrAuth: function() {
      for (var a in this.contributors) {
        let t = this.contributors[a], e = {
          "@id": t["@id"],
          "@type": "person",
          name: t.name
        };
        t.onbehalfof.name !== null && t.onbehalfof.name !== void 0 && (e.onbehalfof = {
          "@id": t.onbehalfof["@id"],
          "@type": "organization",
          name: t.onbehalfof.name
        }), "specializationOf" in t && (e.specializationOf = {
          "@id": t.specializationOf["@id"]
        }), this.dataset.author.push(e);
      }
    },
    /*
      Distribution and representation handling: server
    */
    handleDistrUpload(a) {
      let t = a;
      for (var e = 0; e < t.length; e++) {
        var i = t[e];
        this.uploadedFiles.some((s) => s.name === i.name) ? alert(`${i.name} has already been uploaded`) : (this.isInvalidUpload = !1, i.label = this.createDefaultLabel(i.name), this.uploadedFiles.push(i));
      }
    },
    /* 
      Helper to generate a default rdfs:label for distributions
    */
    createDefaultLabel(a) {
      var t = a.split(".");
      t.pop();
      var e = t.join("."), i = e.replace(/_/g, " ");
      return i.replace(/[^a-zA-Z0-9]+/g, " ").trim();
    },
    handleImgUpload(a) {
      this.uploadedImg = a;
    },
    removeFile(a) {
      this.uploadedFiles.splice(a, 1);
      const t = document.querySelector("#distrFiles");
      this.distr_upload = [], t.value = "";
    },
    async saveDistribution() {
      let a = this.uploadedFiles;
      if (this.distrStatus = T, !a.length)
        return this.distrStatus = _;
      await _t(a, this.generatedUUID).then((t) => {
        this.distrStatus = q;
      }).catch((t) => {
        this.uploadError = t.response, this.distrStatus = C;
      });
    },
    async saveRepImg() {
      const a = this.uploadedImg;
      if (this.depictStatus = T, !a.length)
        return this.depictStatus = _;
      await wt(a[0], this.generatedUUID).then((t) => {
        this.dataset.depiction.accessURL = t[1], this.dataset.depiction["@id"] = t[0], this.dataset.depiction.name = a[0].name, this.depictStatus = q;
      }).catch((t) => {
        this.uploadError = t.response, this.depictStatus = C;
      });
    },
    removeImage() {
      document.querySelector("#repImgUploader").value = "", document.querySelector("#depictImg").src = "", this.rep_image = [], this.uploadedImg = [], document.querySelector("#depictWrapper").style.visibility = "hidden";
    },
    // Load a thumbnail of the representative image
    previewFile() {
      const a = document.querySelector("#depictImg"), t = document.querySelector("#depictWrapper"), e = document.querySelector("#repImgUploader").files[0], i = new FileReader(), s = this.dataset;
      i.addEventListener("load", function() {
        t.style.visibility = "visible", a.src = i.result, s.depiction.hasContent = i.result;
      }, !1), e && i.readAsDataURL(e);
    },
    async checkFirstPage() {
      this.doiLoading = !0, this.uploadedFiles.length ? (this.saveRepImg(), this.saveDistribution(), this.doi === "" ? (this.doiLoading = !1, this.setDone("first", "second")) : await this.getDOI()) : (this.isInvalidUpload = !0, this.doiLoading = !1);
    },
    checkSecondPage() {
      const a = this.dataset.title === "", t = this.cpID === null || this.cpID === "", e = this.dataset.contactpoint.cpfirstname === "", i = this.dataset.contactpoint.cplastname === "", s = this.dataset.contactpoint.cpemail === "", n = this.dataset.description === "";
      a || t || e || i || s || n ? this.isInvalidForm = !0 : this.validEmail(this.dataset.contactpoint.cpemail) ? (this.isInvalidForm = !1, this.dataset.contactpoint["@id"] = `http://orcid.org/${this.cpID}`, this.dataset.contactpoint.name = this.dataset.contactpoint.cpfirstname.concat(" ", this.dataset.contactpoint.cplastname), this.setDone("second", "third"), this.handleContrAuth(), this.editDois()) : (this.dataset.contactpoint.cpemail = "", this.isInvalidForm = !0);
    },
    // Handle steppers
    setDone(a, t) {
      this[a] = !0, t && (this.active = t);
    },
    // Use regex for valid email format
    validEmail(a) {
      var t = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return t.test(a);
    },
    // Submit and post as nanopublication
    submitForm: function() {
      try {
        yt(this.dataset, this.generatedUUID).then(() => K(this.dataset.uri, "view"));
      } catch (a) {
        this.uploadError = a.response, this.distrStatus = C;
      }
    },
    async resolveEntityAuthor(a) {
      this.autocomplete.availableAuthors = await Ct(a);
    },
    async resolveEntityInstitution(a) {
      this.autocomplete.availableInstitutions = await It(a);
    },
    selectedAuthorChange(a) {
      document.createElement("tr");
      var t;
      a.label ? t = a.label : t = a.name, this.contributors.push({
        "@id": a.node,
        name: t,
        onbehalfof: {
          name: null
        }
      }), this.selectedAuthor = "";
    },
    selectedOrgChange(a, t) {
      var e = this.contributors[a].onbehalfof;
      return e.name = t.label, e["@id"] = t.node, t.label;
    },
    //TODO: decide how to deal with not having organizations available
    addAuthor(a) {
      document.createElement("tr"), this.contributors.push({
        "@id": a["@id"],
        name: a.name,
        onbehalfof: {
          name: null
        }
      });
    },
    async getDOI() {
      if (this.doi === "")
        return;
      const a = await St(this.doi);
      await this.useDescribedDoi(a, this.doi).then((t) => {
        this.doiLoading = !1, this.setDone("first", "second");
      }).catch((t) => {
        throw this.doiLoading = !1, this.setDone("first", "second"), t;
      });
    },
    // Fill the form with available data from doi
    async useDescribedDoi(a, t) {
      const e = a.data["@graph"];
      for (var i in e) {
        let n = e[i];
        if (n["@id"] == `http://dx.doi.org/${t}` && ("dc:title" in n && (this.dataset.title = n["dc:title"]), "dc:date" in n && (this.dataset.datemod["@value"] = n["dc:date"]["@value"], this.dataset.datepub["@value"] = n["dc:date"]["@value"]), "dc:creator" in n))
          for (var s in n["dc:creator"])
            await this.getAuthorDescribed(n["dc:creator"][s]["@id"]);
      }
    },
    async getAuthorDescribed(a) {
      const t = await xt(a);
      var e = {
        "@id": t["@id"],
        name: t["foaf:name"],
        onbehalfof: {
          name: null
        }
      };
      return "owl:sameAs" in t && (e.specializationOf = {}, e.specializationOf["@id"] = t["owl:sameAs"]["@id"]), "prov:specializationOf" in t && (e.specializationOf = {}, e.specializationOf["@id"] = t["prov:specializationOf"]["@id"]), this.contributors.push(e), e;
    },
    async lookupOrcid() {
      this.cpIDError = !1, await tt(this.cpID, "contactPoint").then((a) => {
        let t = a;
        if (t === "Invalid")
          return this.resetContactPoint();
        "schema:familyName" in t && (this.dataset.contactpoint.cplastname = t["schema:familyName"]), "schema:givenName" in t && (this.dataset.contactpoint.cpfirstname = t["schema:givenName"]);
      }).catch((a) => {
        throw a;
      });
    },
    // Clear contact point values
    resetContactPoint() {
      this.cpIDError = !0, this.dataset.contactpoint.cplastname = "", this.dataset.contactpoint.cpfirstname = "";
    },
    // Create dialog boxes
    showNewInstitution() {
      u.$emit("open-new-instance", { status: !0, title: "Add new institution", type: "organization" });
    },
    showNewAuthor() {
      u.$emit("open-new-instance", { status: !0, title: "Add new author", type: "author" }).$on("authorSelected", (a) => this.addAuthor(a));
    },
    // Modify styling of menu to override bad width
    setListStyle(a) {
      return Dt();
    }
  },
  created() {
    if (this.loading = !0, u.authUser == null)
      return this.loading = !1;
    this.loadDataset(), u.$on("isauthenticated", (a) => this.authenticated = a);
  }
});
var kt = function() {
  var t = this, e = t._self._c;
  return t._self._setupProxy, e("div", [[e("div", [t.loading ? e("div", [e("spinner", { attrs: { loading: t.loading, text: t.loadingText } })], 1) : t.authenticated ? e("div", [e("div", {}), e("md-card", { staticStyle: { margin: "10px" } }, [e("form", { staticClass: "modal-content", attrs: { action: "", method: "post", enctype: "multipart/form-data", upload_type: "http://www.w3.org/ns/dcat#Dataset" } }, [e("md-steppers", { attrs: { "md-active-step": t.active, "md-linear": "" }, on: { "update:mdActiveStep": function(i) {
    t.active = i;
  }, "update:md-active-step": function(i) {
    t.active = i;
  } } }, [e("md-step", { attrs: { id: "first", "md-label": "Upload files", "md-done": t.first }, on: { "update:mdDone": function(i) {
    t.first = i;
  }, "update:md-done": function(i) {
    t.first = i;
  } } }, [e("div", { staticStyle: { margin: "20px" } }, [e("md-field", { staticStyle: { "max-width": "100%" } }, [e("label", [t._v("DOI of related publication (e.g., 10.1000/000)")]), e("md-input", { model: { value: t.doi, callback: function(i) {
    t.doi = i;
  }, expression: "doi" } })], 1), e("md-field", { class: { "md-invalid": t.isInvalidUpload }, staticStyle: { "max-width": "none" } }, [e("label", [t._v("Select files to upload for this dataset")]), e("md-file", { attrs: { id: "distrFiles", multiple: "", required: "", isInvalidValue: "false" }, on: { change: function(i) {
    return t.handleDistrUpload(i.target.files);
  } }, model: { value: t.distr_upload, callback: function(i) {
    t.distr_upload = i;
  }, expression: "distr_upload" } }), t.distrStatus === 3 ? e("span", { staticStyle: { color: "red" } }, [t._v("Error in upload. Please try again")]) : t._e(), e("span", { staticClass: "md-error", staticStyle: { "margin-left": "40px" } }, [t._v("At least one distribution is required")])], 1), e("div", { staticClass: "large-12 medium-12 small-12 cell", staticStyle: { margin: "20px" } }, t._l(t.uploadedFiles, function(i, s) {
    return e("div", { key: s + "listing", staticClass: "file-listing" }, [e("div", { staticClass: "md-layout", staticStyle: { "margin-left": "10px", "align-items": "center" } }, [e("div", { staticClass: "md-layout-item" }, [t._v(t._s(i.name) + " ")]), e("div", { staticClass: "md-layout-item" }, [e("md-field", { staticStyle: { "max-width": "90%" } }, [e("label", [t._v("Label")]), e("md-input", { model: { value: i.label, callback: function(n) {
      t.$set(i, "label", n);
    }, expression: "file.label" } }), e("md-tooltip", { attrs: { "md-delay": "300" } }, [t._v("Provide a human-readable label or leave as the default")])], 1)], 1), e("div", { staticClass: "md-layout-item" }, [e("md-button", { staticClass: "remove-file md-raised", on: { click: function(n) {
      return t.removeFile(s);
    } } }, [t._v("Remove file")])], 1)])]);
  }), 0), e("md-field", { staticStyle: { "max-width": "none" } }, [e("label", [t._v("Select a representative image to use as thumbnail")]), e("md-file", { attrs: { id: "repImgUploader", accept: "image/*" }, on: { change: function(i) {
    t.handleImgUpload(i.target.files), t.previewFile();
  } }, model: { value: t.rep_image, callback: function(i) {
    t.rep_image = i;
  }, expression: "rep_image" } }), t.depictStatus === 3 ? e("span", { staticStyle: { color: "red" } }, [t._v("Error in upload. Please try again")]) : t._e()], 1), e("div", { staticStyle: { "margin-left": "40px", visibility: "hidden" }, attrs: { id: "depictWrapper" } }, [e("figure", [e("img", { staticStyle: { height: "200px" }, attrs: { id: "depictImg", src: require(""), alt: "Image preview..." } }), e("figcaption", [t._v(t._s(t.dataset.depiction.name))])]), e("md-button", { staticClass: "close md-raised", staticStyle: { "margin-left": "40px" }, attrs: { type: "button" }, on: { click: function(i) {
    return t.removeImage();
  } } }, [t._v("Remove image")])], 1)], 1), e("div", { staticClass: "md-layout", staticStyle: { "align-items": "center" } }, [e("div", { staticClass: "md-layout-item" }, [e("md-button", { staticClass: "md-raised md-primary", on: { click: function(i) {
    return t.checkFirstPage();
  } } }, [t._v(" Upload and continue ")])], 1), t.doiLoading ? e("div", { staticClass: "md-layout-item" }, [e("md-progress-spinner", { attrs: { "md-diameter": 30, "md-stroke": 3, "md-mode": "indeterminate" } })], 1) : t._e(), e("div", { staticClass: "md-layout-item" }), e("div", { staticClass: "md-layout-item" })])]), e("md-step", { attrs: { id: "second", "md-label": "Provide additional info", "md-done": t.second }, on: { "update:mdDone": function(i) {
    t.second = i;
  }, "update:md-done": function(i) {
    t.second = i;
  } } }, [e("div", { staticClass: "md-layout" }, [e("md-content", { staticStyle: { width: "100%", margin: "20px" } }, [e("div", { staticClass: "md-headline", staticStyle: { "margin-top": "10px" } }, [t._v(" General Information ")]), e("md-field", { class: { "md-invalid": t.isInvalidForm && t.dataset.title === "" }, staticStyle: { "max-width": "100%" } }, [e("label", [t._v("Title")]), e("md-input", { attrs: { required: "" }, model: { value: t.dataset.title, callback: function(i) {
    t.$set(t.dataset, "title", i);
  }, expression: "dataset.title" } }), e("span", { staticClass: "md-error" }, [t._v("Title required")])], 1), e("div", { staticClass: "md-subheading", staticStyle: { "margin-top": "40px" } }, [t._v("Contact Point")]), e("div", { staticClass: "md-layout md-gutter", staticStyle: { "align-items": "center" } }, [e("div", { staticClass: "md-layout-item md-size-30" }, [e("md-field", { class: { "md-invalid": t.isInvalidForm && (t.cpID === null || t.cpID === "") }, staticStyle: { "max-width": "100%" } }, [e("label", [t._v("ORCID Identifier (e.g., 0000-0001-2345-6789)")]), e("md-input", { attrs: { required: "" }, on: { change: function(i) {
    return t.lookupOrcid();
  } }, model: { value: t.cpID, callback: function(i) {
    t.cpID = i;
  }, expression: "cpID" } }), e("span", { staticClass: "md-error" }, [t._v("ORCID iD required")])], 1)], 1), e("div", { staticClass: "md-layout-item md-size-20" }, [e("md-field", { class: { "md-invalid": t.isInvalidForm && t.dataset.contactpoint.cpfirstname === "" } }, [e("label", [t._v("First name")]), e("md-input", { attrs: { required: "" }, model: { value: t.dataset.contactpoint.cpfirstname, callback: function(i) {
    t.$set(t.dataset.contactpoint, "cpfirstname", i);
  }, expression: "dataset.contactpoint.cpfirstname" } }), e("span", { staticClass: "md-error" }, [t._v("Contact point required")])], 1)], 1), e("div", { staticClass: "md-layout-item md-size-20" }, [e("md-field", { class: { "md-invalid": t.isInvalidForm && t.dataset.contactpoint.cplastname === "" } }, [e("label", [t._v("Last name")]), e("md-input", { attrs: { required: "" }, model: { value: t.dataset.contactpoint.cplastname, callback: function(i) {
    t.$set(t.dataset.contactpoint, "cplastname", i);
  }, expression: "dataset.contactpoint.cplastname" } }), e("span", { staticClass: "md-error" }, [t._v("Contact point required")])], 1)], 1), e("div", { staticClass: "md-layout-item md-size-25" }, [e("md-field", { class: { "md-invalid": t.isInvalidForm && t.dataset.contactpoint.cpemail === "" }, staticStyle: { "max-width": "100%" } }, [e("label", [t._v("Email")]), e("md-input", { attrs: { required: "" }, model: { value: t.dataset.contactpoint.cpemail, callback: function(i) {
    t.$set(t.dataset.contactpoint, "cpemail", i);
  }, expression: "dataset.contactpoint.cpemail" } }), e("span", { staticClass: "md-error" }, [t._v("Valid email required")])], 1)], 1)]), t.cpIDError ? e("div", { staticStyle: { color: "red", "margin-bottom": "20px", "text-align": "center" } }, [t._v(" No results found for " + t._s(t.cpID) + " ")]) : t._e(), e("div", { staticStyle: { "margin-bottom": "40px", "text-align": "center" } }, [t._v(" Don't have an ORCID iD? "), e("a", { attrs: { href: "https://orcid.org/", target: "_blank" } }, [t._v("Create one here")])]), e("md-field", { class: { "md-invalid": t.isInvalidForm && t.dataset.description === "" }, staticStyle: { "max-width": "100%" } }, [e("label", [t._v("Text Description")]), e("md-textarea", { attrs: { required: "" }, model: { value: t.dataset.description, callback: function(i) {
    t.$set(t.dataset, "description", i);
  }, expression: "dataset.description" } }), e("span", { staticClass: "md-error" }, [t._v("Description required")])], 1)], 1), e("md-divider", { staticStyle: { "border-style": "solid" }, attrs: { width: "100%" } }), e("md-content", { staticStyle: { width: "100%", margin: "20px" } }, [e("div", { staticClass: "md-headline", staticStyle: { "margin-top": "10px", "margin-bottom": "10px" } }, [t._v(" Contributors ")]), e("div", [e("md-autocomplete", { staticStyle: { "min-width": "100%" }, attrs: { "md-options": t.autocomplete.availableAuthors, "md-open-on-focus": !1 }, on: { "md-changed": t.resolveEntityAuthor, "md-selected": t.selectedAuthorChange, "md-opened": t.setListStyle, "md-closed": function(i) {
    return t.setListStyle(!0);
  } }, scopedSlots: t._u([{ key: "md-autocomplete-item", fn: function({ item: i, term: s }) {
    return [e("label", { staticStyle: { "white-space": "pre-wrap" }, attrs: { "md-term": "term", "md-fuzzy-search": "true" } }, [t._v(t._s(i.label))])];
  } }, { key: "md-autocomplete-empty", fn: function({ term: i }) {
    return [e("p", [t._v('No authors matching "' + t._s(i) + '" were found.')]), e("a", { staticStyle: { cursor: "pointer" }, on: { click: t.showNewAuthor } }, [t._v("Create new")])];
  } }]), model: { value: t.selectedAuthor, callback: function(i) {
    t.selectedAuthor = i;
  }, expression: "selectedAuthor" } }, [e("label", [t._v("Search for Author")])]), e("table", { staticClass: "table", staticStyle: { "border-collapse": "collapse" }, attrs: { width: "100%" } }, [e("tbody", [e("tr", [e("td", { staticStyle: { width: "100%" } }, t._l(t.contributors, function(i, s) {
    return e("tr", { key: s + "contr", staticStyle: { "border-top": "0.5pt lightgray solid" } }, [e("td", { staticStyle: { width: "50%" } }, [t._v(" " + t._s(t.contributors[s].name) + " ")]), t.editableOrgs ? e("td", { staticStyle: { width: "40%" } }, [e("md-autocomplete", { staticStyle: { "max-width": "90%" }, attrs: { "md-options": t.autocomplete.availableInstitutions, "md-open-on-focus": !1 }, on: { "md-changed": t.resolveEntityInstitution, "md-selected": function(n) {
      return t.selectedOrgChange(s, n);
    } }, scopedSlots: t._u([{ key: "md-autocomplete-item", fn: function({ item: n, term: o }) {
      return [e("md-highlight-text", { attrs: { "md-term": o } }, [t._v(t._s(n.label))])];
    } }, { key: "md-autocomplete-empty", fn: function({ term: n }) {
      return [e("p", [t._v('No organizations matching "' + t._s(n) + '" were found.')]), e("a", { staticStyle: { cursor: "pointer" }, on: { click: t.showNewInstitution } }, [t._v("Create new")])];
    } }], null, !0), model: { value: i.onbehalfof.name, callback: function(n) {
      t.$set(i.onbehalfof, "name", n);
    }, expression: "row['onbehalfof']['name']" } }, [e("label", [t._v("Organization")])])], 1) : e("td", { staticStyle: { width: "30%" } }), e("td", [e("a", { staticStyle: { cursor: "pointer" }, on: { click: function(n) {
      return t.removeElement(s);
    } } }, [t._v("Remove")])])]);
  }), 0)])])])], 1)]), e("md-divider", { staticStyle: { "border-style": "solid" }, attrs: { width: "100%" } }), e("md-content", { staticStyle: { width: "100%", margin: "20px" } }, [e("div", { staticClass: "md-headline", staticStyle: { "margin-top": "10px", "margin-bottom": "10px" } }, [t._v(" Publication Information ")]), e("div", { staticStyle: { width: "100%" } }, [e("div", { staticClass: "md-layout md-gutter" }, [e("div", { staticClass: "md-layout-item md-size-50" }, [e("label", [t._v("Date Published")]), e("md-field", [e("md-input", { attrs: { type: "date", formatter: t.dateFormat }, model: { value: t.dataset.datepub["@value"], callback: function(i) {
    t.$set(t.dataset.datepub, "@value", i);
  }, expression: "dataset.datepub['@value']" } })], 1)], 1), e("div", { staticClass: "md-layout-item md-size-50" }, [e("label", [t._v("Date Last Modified")]), e("md-field", [e("md-input", { attrs: { type: "date", formatter: t.dateFormat }, model: { value: t.dataset.datemod["@value"], callback: function(i) {
    t.$set(t.dataset.datemod, "@value", i);
  }, expression: "dataset.datemod['@value']" } })], 1)], 1)])])]), e("md-button", { staticClass: "md-raised md-primary", on: { click: t.checkSecondPage } }, [t._v("Next")]), t.isInvalidForm ? e("span", { staticClass: "md-error", staticStyle: { color: "red" } }, [t._v("Check for errors in required fields")]) : t._e()], 1)]), e("md-step", { attrs: { id: "third", "md-label": "Confirm and Submit", "md-done": t.third }, on: { "update:mdDone": function(i) {
    t.third = i;
  }, "update:md-done": function(i) {
    t.third = i;
  } } }, [e("div", { staticClass: "md-headline", staticStyle: { margin: "10px" } }, [t._v(" Form Results ")]), e("md-content", { staticStyle: { width: "100%", margin: "20px" } }, [e("span", [t._v("Title: " + t._s(t.dataset.title))]), e("p", [t._v(" Contact Point: " + t._s(t.dataset.contactpoint.cpfirstname) + " " + t._s(t.dataset.contactpoint.cplastname) + " - " + t._s(t.dataset.contactpoint.cpemail) + " ")]), e("p", [t._v("Text Description: " + t._s(t.dataset.description))]), e("span", [t._v("Contributors")]), t._l(t.contributors, function(i, s) {
    return e("div", { key: s + "resContr", staticStyle: { "margin-left": "20px" } }, [e("span", [t._v(t._s(i.name))]), i.onbehalfof !== null && i.onbehalfof.name !== void 0 ? [t._v(" - " + t._s(i.onbehalfof.name))] : t._e()], 2);
  }), e("p", [t._v("Date Published: " + t._s(t.dataset.datepub["@value"]))]), e("p", [t._v("Date Last Modified: " + t._s(t.dataset.datemod["@value"]))]), e("p", [t._v(" Related publication: ")]), e("div", { staticStyle: { "margin-left": "20px" } }, [t._v(" " + t._s(t.dataset.refby) + " ")]), e("p", { staticStyle: { "margin-top": "10px" } }, [t._v("Distribution(s):")]), t._l(t.uploadedFiles, function(i, s) {
    return e("div", { key: s + "confirm", staticStyle: { "margin-left": "20px" } }, [t._v(" " + t._s(i.name) + " ")]);
  }), e("p", [t._v("Representative Image: " + t._s(t.rep_image))])], 2), e("md-card-actions", [e("md-button", { staticClass: "md-primary", on: { click: t.submitForm } }, [t._v("Submit")])], 1)], 1)], 1)], 1)])], 1) : e("div", [e("div", [t._v("Error: user must be logged in to access this page.")])])])]], 2);
}, Ut = [], Ft = /* @__PURE__ */ Q(
  At,
  kt,
  Ut,
  !1,
  null,
  null
);
const zt = Ft.exports;
export {
  zt as default
};
