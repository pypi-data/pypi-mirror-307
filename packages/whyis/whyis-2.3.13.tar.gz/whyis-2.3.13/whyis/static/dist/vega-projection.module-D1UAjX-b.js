function uc(n) {
  return n;
}
function ac(n) {
  if (n == null) return uc;
  var e, t, r = n.scale[0], i = n.scale[1], u = n.translate[0], a = n.translate[1];
  return function(o, c) {
    c || (e = t = 0);
    var f = 2, l = o.length, s = new Array(l);
    for (s[0] = (e += o[0]) * r + u, s[1] = (t += o[1]) * i + a; f < l; ) s[f] = o[f], ++f;
    return s;
  };
}
function oc(n, e) {
  for (var t, r = n.length, i = r - e; i < --r; ) t = n[i], n[i++] = n[r], n[r] = t;
}
function Ng(n, e) {
  return typeof e == "string" && (e = n.objects[e]), e.type === "GeometryCollection" ? { type: "FeatureCollection", features: e.geometries.map(function(t) {
    return $u(n, t);
  }) } : $u(n, e);
}
function $u(n, e) {
  var t = e.id, r = e.bbox, i = e.properties == null ? {} : e.properties, u = La(n, e);
  return t == null && r == null ? { type: "Feature", properties: i, geometry: u } : r == null ? { type: "Feature", id: t, properties: i, geometry: u } : { type: "Feature", id: t, bbox: r, properties: i, geometry: u };
}
function La(n, e) {
  var t = ac(n.transform), r = n.arcs;
  function i(l, s) {
    s.length && s.pop();
    for (var h = r[l < 0 ? ~l : l], g = 0, d = h.length; g < d; ++g)
      s.push(t(h[g], g));
    l < 0 && oc(s, d);
  }
  function u(l) {
    return t(l);
  }
  function a(l) {
    for (var s = [], h = 0, g = l.length; h < g; ++h) i(l[h], s);
    return s.length < 2 && s.push(s[0]), s;
  }
  function o(l) {
    for (var s = a(l); s.length < 4; ) s.push(s[0]);
    return s;
  }
  function c(l) {
    return l.map(o);
  }
  function f(l) {
    var s = l.type, h;
    switch (s) {
      case "GeometryCollection":
        return { type: s, geometries: l.geometries.map(f) };
      case "Point":
        h = u(l.coordinates);
        break;
      case "MultiPoint":
        h = l.coordinates.map(u);
        break;
      case "LineString":
        h = a(l.arcs);
        break;
      case "MultiLineString":
        h = l.arcs.map(a);
        break;
      case "Polygon":
        h = c(l.arcs);
        break;
      case "MultiPolygon":
        h = l.arcs.map(c);
        break;
      default:
        return null;
    }
    return { type: s, coordinates: h };
  }
  return f(e);
}
function fc(n, e) {
  var t = {}, r = {}, i = {}, u = [], a = -1;
  e.forEach(function(f, l) {
    var s = n.arcs[f < 0 ? ~f : f], h;
    s.length < 3 && !s[1][0] && !s[1][1] && (h = e[++a], e[a] = f, e[l] = h);
  }), e.forEach(function(f) {
    var l = o(f), s = l[0], h = l[1], g, d;
    if (g = i[s])
      if (delete i[g.end], g.push(f), g.end = h, d = r[h]) {
        delete r[d.start];
        var p = d === g ? g : g.concat(d);
        r[p.start = g.start] = i[p.end = d.end] = p;
      } else
        r[g.start] = i[g.end] = g;
    else if (g = r[h])
      if (delete r[g.start], g.unshift(f), g.start = s, d = i[s]) {
        delete i[d.end];
        var m = d === g ? g : d.concat(g);
        r[m.start = d.start] = i[m.end = g.end] = m;
      } else
        r[g.start] = i[g.end] = g;
    else
      g = [f], r[g.start = s] = i[g.end = h] = g;
  });
  function o(f) {
    var l = n.arcs[f < 0 ? ~f : f], s = l[0], h;
    return n.transform ? (h = [0, 0], l.forEach(function(g) {
      h[0] += g[0], h[1] += g[1];
    })) : h = l[l.length - 1], f < 0 ? [h, s] : [s, h];
  }
  function c(f, l) {
    for (var s in f) {
      var h = f[s];
      delete l[h.start], delete h.start, delete h.end, h.forEach(function(g) {
        t[g < 0 ? ~g : g] = 1;
      }), u.push(h);
    }
  }
  return c(i, r), c(r, i), e.forEach(function(f) {
    t[f < 0 ? ~f : f] || u.push([f]);
  }), u;
}
function Dg(n) {
  return La(n, cc.apply(this, arguments));
}
function cc(n, e, t) {
  var r, i, u;
  if (arguments.length > 1) r = lc(n, e, t);
  else for (i = 0, r = new Array(u = n.arcs.length); i < u; ++i) r[i] = i;
  return { type: "MultiLineString", arcs: fc(n, r) };
}
function lc(n, e, t) {
  var r = [], i = [], u;
  function a(s) {
    var h = s < 0 ? ~s : s;
    (i[h] || (i[h] = [])).push({ i: s, g: u });
  }
  function o(s) {
    s.forEach(a);
  }
  function c(s) {
    s.forEach(o);
  }
  function f(s) {
    s.forEach(c);
  }
  function l(s) {
    switch (u = s, s.type) {
      case "GeometryCollection":
        s.geometries.forEach(l);
        break;
      case "LineString":
        o(s.arcs);
        break;
      case "MultiLineString":
      case "Polygon":
        c(s.arcs);
        break;
      case "MultiPolygon":
        f(s.arcs);
        break;
    }
  }
  return l(e), i.forEach(t == null ? function(s) {
    r.push(s[0].i);
  } : function(s) {
    t(s[0].g, s[s.length - 1].g) && r.push(s[0].i);
  }), r;
}
function Ln(n, e) {
  return n == null || e == null ? NaN : n < e ? -1 : n > e ? 1 : n >= e ? 0 : NaN;
}
function sc(n, e) {
  return n == null || e == null ? NaN : e < n ? -1 : e > n ? 1 : e >= n ? 0 : NaN;
}
function dr(n) {
  let e, t, r;
  n.length !== 2 ? (e = Ln, t = (o, c) => Ln(n(o), c), r = (o, c) => n(o) - c) : (e = n === Ln || n === sc ? n : hc, t = n, r = n);
  function i(o, c, f = 0, l = o.length) {
    if (f < l) {
      if (e(c, c) !== 0) return l;
      do {
        const s = f + l >>> 1;
        t(o[s], c) < 0 ? f = s + 1 : l = s;
      } while (f < l);
    }
    return f;
  }
  function u(o, c, f = 0, l = o.length) {
    if (f < l) {
      if (e(c, c) !== 0) return l;
      do {
        const s = f + l >>> 1;
        t(o[s], c) <= 0 ? f = s + 1 : l = s;
      } while (f < l);
    }
    return f;
  }
  function a(o, c, f = 0, l = o.length) {
    const s = i(o, c, f, l - 1);
    return s > f && r(o[s - 1], c) > -r(o[s], c) ? s - 1 : s;
  }
  return { left: i, center: a, right: u };
}
function hc() {
  return 0;
}
function Oa(n) {
  return n === null ? NaN : +n;
}
function* gc(n, e) {
  if (e === void 0)
    for (let t of n)
      t != null && (t = +t) >= t && (yield t);
  else {
    let t = -1;
    for (let r of n)
      (r = e(r, ++t, n)) != null && (r = +r) >= r && (yield r);
  }
}
const za = dr(Ln), ce = za.right, Ug = za.left;
dr(Oa).center;
function dc(n, e) {
  let t = 0, r, i = 0, u = 0;
  if (e === void 0)
    for (let a of n)
      a != null && (a = +a) >= a && (r = a - i, i += r / ++t, u += r * (a - i));
  else {
    let a = -1;
    for (let o of n)
      (o = e(o, ++a, n)) != null && (o = +o) >= o && (r = o - i, i += r / ++t, u += r * (o - i));
  }
  if (t > 1) return u / (t - 1);
}
function pc(n, e) {
  const t = dc(n, e);
  return t && Math.sqrt(t);
}
class le {
  constructor() {
    this._partials = new Float64Array(32), this._n = 0;
  }
  add(e) {
    const t = this._partials;
    let r = 0;
    for (let i = 0; i < this._n && i < 32; i++) {
      const u = t[i], a = e + u, o = Math.abs(e) < Math.abs(u) ? e - (a - u) : u - (a - e);
      o && (t[r++] = o), e = a;
    }
    return t[r] = e, this._n = r + 1, this;
  }
  valueOf() {
    const e = this._partials;
    let t = this._n, r, i, u, a = 0;
    if (t > 0) {
      for (a = e[--t]; t > 0 && (r = a, i = e[--t], a = r + i, u = i - (a - r), !u); )
        ;
      t > 0 && (u < 0 && e[t - 1] < 0 || u > 0 && e[t - 1] > 0) && (i = u * 2, r = a + i, i == r - a && (a = r));
    }
    return a;
  }
}
class Cu extends Map {
  constructor(e, t = Ba) {
    if (super(), Object.defineProperties(this, { _intern: { value: /* @__PURE__ */ new Map() }, _key: { value: t } }), e != null) for (const [r, i] of e) this.set(r, i);
  }
  get(e) {
    return super.get(Qr(this, e));
  }
  has(e) {
    return super.has(Qr(this, e));
  }
  set(e, t) {
    return super.set(Wa(this, e), t);
  }
  delete(e) {
    return super.delete(Xa(this, e));
  }
}
class Eg extends Set {
  constructor(e, t = Ba) {
    if (super(), Object.defineProperties(this, { _intern: { value: /* @__PURE__ */ new Map() }, _key: { value: t } }), e != null) for (const r of e) this.add(r);
  }
  has(e) {
    return super.has(Qr(this, e));
  }
  add(e) {
    return super.add(Wa(this, e));
  }
  delete(e) {
    return super.delete(Xa(this, e));
  }
}
function Qr({ _intern: n, _key: e }, t) {
  const r = e(t);
  return n.has(r) ? n.get(r) : t;
}
function Wa({ _intern: n, _key: e }, t) {
  const r = e(t);
  return n.has(r) ? n.get(r) : (n.set(r, t), t);
}
function Xa({ _intern: n, _key: e }, t) {
  const r = e(t);
  return n.has(r) && (t = n.get(r), n.delete(r)), t;
}
function Ba(n) {
  return n !== null && typeof n == "object" ? n.valueOf() : n;
}
function mc(n = Ln) {
  if (n === Ln) return ja;
  if (typeof n != "function") throw new TypeError("compare is not a function");
  return (e, t) => {
    const r = n(e, t);
    return r || r === 0 ? r : (n(t, t) === 0) - (n(e, e) === 0);
  };
}
function ja(n, e) {
  return (n == null || !(n >= n)) - (e == null || !(e >= e)) || (n < e ? -1 : n > e ? 1 : 0);
}
const bc = Math.sqrt(50), yc = Math.sqrt(10), Mc = Math.sqrt(2);
function Bt(n, e, t) {
  const r = (e - n) / Math.max(0, t), i = Math.floor(Math.log10(r)), u = r / Math.pow(10, i), a = u >= bc ? 10 : u >= yc ? 5 : u >= Mc ? 2 : 1;
  let o, c, f;
  return i < 0 ? (f = Math.pow(10, -i) / a, o = Math.round(n * f), c = Math.round(e * f), o / f < n && ++o, c / f > e && --c, f = -f) : (f = Math.pow(10, i) * a, o = Math.round(n / f), c = Math.round(e / f), o * f < n && ++o, c * f > e && --c), c < o && 0.5 <= t && t < 2 ? Bt(n, e, t * 2) : [o, c, f];
}
function Vr(n, e, t) {
  if (e = +e, n = +n, t = +t, !(t > 0)) return [];
  if (n === e) return [n];
  const r = e < n, [i, u, a] = r ? Bt(e, n, t) : Bt(n, e, t);
  if (!(u >= i)) return [];
  const o = u - i + 1, c = new Array(o);
  if (r)
    if (a < 0) for (let f = 0; f < o; ++f) c[f] = (u - f) / -a;
    else for (let f = 0; f < o; ++f) c[f] = (u - f) * a;
  else if (a < 0) for (let f = 0; f < o; ++f) c[f] = (i + f) / -a;
  else for (let f = 0; f < o; ++f) c[f] = (i + f) * a;
  return c;
}
function Jr(n, e, t) {
  return e = +e, n = +n, t = +t, Bt(n, e, t)[2];
}
function ht(n, e, t) {
  e = +e, n = +n, t = +t;
  const r = e < n, i = r ? Jr(e, n, t) : Jr(n, e, t);
  return (r ? -1 : 1) * (i < 0 ? 1 / -i : i);
}
function Nu(n, e) {
  let t;
  if (e === void 0)
    for (const r of n)
      r != null && (t < r || t === void 0 && r >= r) && (t = r);
  else {
    let r = -1;
    for (let i of n)
      (i = e(i, ++r, n)) != null && (t < i || t === void 0 && i >= i) && (t = i);
  }
  return t;
}
function Du(n, e) {
  let t;
  if (e === void 0)
    for (const r of n)
      r != null && (t > r || t === void 0 && r >= r) && (t = r);
  else {
    let r = -1;
    for (let i of n)
      (i = e(i, ++r, n)) != null && (t > i || t === void 0 && i >= i) && (t = i);
  }
  return t;
}
function Ga(n, e, t = 0, r = 1 / 0, i) {
  if (e = Math.floor(e), t = Math.floor(Math.max(0, t)), r = Math.floor(Math.min(n.length - 1, r)), !(t <= e && e <= r)) return n;
  for (i = i === void 0 ? ja : mc(i); r > t; ) {
    if (r - t > 600) {
      const c = r - t + 1, f = e - t + 1, l = Math.log(c), s = 0.5 * Math.exp(2 * l / 3), h = 0.5 * Math.sqrt(l * s * (c - s) / c) * (f - c / 2 < 0 ? -1 : 1), g = Math.max(t, Math.floor(e - f * s / c + h)), d = Math.min(r, Math.floor(e + (c - f) * s / c + h));
      Ga(n, e, g, d, i);
    }
    const u = n[e];
    let a = t, o = r;
    for (ze(n, t, e), i(n[r], u) > 0 && ze(n, t, r); a < o; ) {
      for (ze(n, a, o), ++a, --o; i(n[a], u) < 0; ) ++a;
      for (; i(n[o], u) > 0; ) --o;
    }
    i(n[t], u) === 0 ? ze(n, t, o) : (++o, ze(n, o, r)), o <= e && (t = o + 1), e <= o && (r = o - 1);
  }
  return n;
}
function ze(n, e, t) {
  const r = n[e];
  n[e] = n[t], n[t] = r;
}
function _r(n, e, t) {
  if (n = Float64Array.from(gc(n, t)), !(!(r = n.length) || isNaN(e = +e))) {
    if (e <= 0 || r < 2) return Du(n);
    if (e >= 1) return Nu(n);
    var r, i = (r - 1) * e, u = Math.floor(i), a = Nu(Ga(n, u).subarray(0, u + 1)), o = Du(n.subarray(u + 1));
    return a + (o - a) * (i - u);
  }
}
function Za(n, e, t = Oa) {
  if (!(!(r = n.length) || isNaN(e = +e))) {
    if (e <= 0 || r < 2) return +t(n[0], 0, n);
    if (e >= 1) return +t(n[r - 1], r - 1, n);
    var r, i = (r - 1) * e, u = Math.floor(i), a = +t(n[u], u, n), o = +t(n[u + 1], u + 1, n);
    return a + (o - a) * (i - u);
  }
}
function vc(n, e) {
  return _r(n, 0.5, e);
}
function* wc(n) {
  for (const e of n)
    yield* e;
}
function Qa(n) {
  return Array.from(wc(n));
}
function xc(n, e, t) {
  n = +n, e = +e, t = (i = arguments.length) < 2 ? (e = n, n = 0, 1) : i < 3 ? 1 : +t;
  for (var r = -1, i = Math.max(0, Math.ceil((e - n) / t)) | 0, u = new Array(i); ++r < i; )
    u[r] = n + r * t;
  return u;
}
function* Va(n, e) {
  if (e == null)
    for (let t of n)
      t != null && t !== "" && (t = +t) >= t && (yield t);
  else {
    let t = -1;
    for (let r of n)
      r = e(r, ++t, n), r != null && r !== "" && (r = +r) >= r && (yield r);
  }
}
function Tc(n, e, t) {
  const r = Float64Array.from(Va(n, t));
  return r.sort(Ln), e.map((i) => Za(r, i));
}
function Sc(n, e) {
  return Tc(n, [0.25, 0.5, 0.75], e);
}
function $c(n, e) {
  const t = n.length, r = pc(n, e), i = Sc(n, e), u = (i[2] - i[0]) / 1.34;
  return 1.06 * (Math.min(r, u) || r || Math.abs(i[0]) || 1) * Math.pow(t, -0.2);
}
function Fg(n) {
  const e = n.maxbins || 20, t = n.base || 10, r = Math.log(t), i = n.divide || [5, 2];
  let u = n.extent[0], a = n.extent[1], o, c, f, l, s, h;
  const g = n.span || a - u || Math.abs(u) || 1;
  if (n.step)
    o = n.step;
  else if (n.steps) {
    for (l = g / e, s = 0, h = n.steps.length; s < h && n.steps[s] < l; ++s) ;
    o = n.steps[Math.max(0, s - 1)];
  } else {
    for (c = Math.ceil(Math.log(e) / r), f = n.minstep || 0, o = Math.max(f, Math.pow(t, Math.round(Math.log(g) / r) - c)); Math.ceil(g / o) > e; )
      o *= t;
    for (s = 0, h = i.length; s < h; ++s)
      l = o / i[s], l >= f && g / l <= e && (o = l);
  }
  l = Math.log(o);
  const d = l >= 0 ? 0 : ~~(-l / r) + 1, p = Math.pow(t, -d - 1);
  return (n.nice || n.nice === void 0) && (l = Math.floor(u / o + p) * o, u = u < l ? l - o : l, a = Math.ceil(a / o) * o), {
    start: u,
    stop: a === u ? u + o : a,
    step: o
  };
}
var Qn = Math.random;
function Ag(n) {
  Qn = n;
}
function kg(n, e, t, r) {
  if (!n.length) return [void 0, void 0];
  const i = Float64Array.from(Va(n, r)), u = i.length, a = e;
  let o, c, f, l;
  for (f = 0, l = Array(a); f < a; ++f) {
    for (o = 0, c = 0; c < u; ++c)
      o += i[~~(Qn() * u)];
    l[f] = o / u;
  }
  return l.sort(Ln), [_r(l, t / 2), _r(l, 1 - t / 2)];
}
function Yg(n, e, t, r) {
  r = r || ((h) => h);
  const i = n.length, u = new Float64Array(i);
  let a = 0, o = 1, c = r(n[0]), f = c, l = c + e, s;
  for (; o < i; ++o) {
    if (s = r(n[o]), s >= l) {
      for (f = (c + f) / 2; a < o; ++a) u[a] = f;
      l = s + e, c = s;
    }
    f = s;
  }
  for (f = (c + f) / 2; a < o; ++a) u[a] = f;
  return t ? Cc(u, e + e / 4) : u;
}
function Cc(n, e) {
  const t = n.length;
  let r = 0, i = 1, u, a;
  for (; n[r] === n[i]; ) ++i;
  for (; i < t; ) {
    for (u = i + 1; n[i] === n[u]; ) ++u;
    if (n[i] - n[i - 1] < e) {
      for (a = i + (r + u - i - i >> 1); a < i; ) n[a++] = n[i];
      for (; a > i; ) n[a--] = n[r];
    }
    r = i, i = u;
  }
  return n;
}
function Rg(n) {
  return function() {
    return n = (1103515245 * n + 12345) % 2147483647, n / 2147483647;
  };
}
function qg(n, e) {
  e == null && (e = n, n = 0);
  let t, r, i;
  const u = {
    min(a) {
      return arguments.length ? (t = a || 0, i = r - t, u) : t;
    },
    max(a) {
      return arguments.length ? (r = a || 0, i = r - t, u) : r;
    },
    sample() {
      return t + Math.floor(i * Qn());
    },
    pdf(a) {
      return a === Math.floor(a) && a >= t && a < r ? 1 / i : 0;
    },
    cdf(a) {
      const o = Math.floor(a);
      return o < t ? 0 : o >= r ? 1 : (o - t + 1) / i;
    },
    icdf(a) {
      return a >= 0 && a <= 1 ? t - 1 + Math.floor(a * i) : NaN;
    }
  };
  return u.min(n).max(e);
}
const Ja = Math.sqrt(2 * Math.PI), Nc = Math.SQRT2;
let We = NaN;
function _a(n, e) {
  n = n || 0, e = e ?? 1;
  let t = 0, r = 0, i, u;
  if (We === We)
    t = We, We = NaN;
  else {
    do
      t = Qn() * 2 - 1, r = Qn() * 2 - 1, i = t * t + r * r;
    while (i === 0 || i > 1);
    u = Math.sqrt(-2 * Math.log(i) / i), t *= u, We = r * u;
  }
  return n + t * e;
}
function Dc(n, e, t) {
  t = t ?? 1;
  const r = (n - (e || 0)) / t;
  return Math.exp(-0.5 * r * r) / (t * Ja);
}
function Ka(n, e, t) {
  e = e || 0, t = t ?? 1;
  const r = (n - e) / t, i = Math.abs(r);
  let u;
  if (i > 37)
    u = 0;
  else {
    const a = Math.exp(-i * i / 2);
    let o;
    i < 7.07106781186547 ? (o = 0.0352624965998911 * i + 0.700383064443688, o = o * i + 6.37396220353165, o = o * i + 33.912866078383, o = o * i + 112.079291497871, o = o * i + 221.213596169931, o = o * i + 220.206867912376, u = a * o, o = 0.0883883476483184 * i + 1.75566716318264, o = o * i + 16.064177579207, o = o * i + 86.7807322029461, o = o * i + 296.564248779674, o = o * i + 637.333633378831, o = o * i + 793.826512519948, o = o * i + 440.413735824752, u = u / o) : (o = i + 0.65, o = i + 4 / o, o = i + 3 / o, o = i + 2 / o, o = i + 1 / o, u = a / o / 2.506628274631);
  }
  return r > 0 ? 1 - u : u;
}
function no(n, e, t) {
  return n < 0 || n > 1 ? NaN : (e || 0) + (t ?? 1) * Nc * Uc(2 * n - 1);
}
function Uc(n) {
  let e = -Math.log((1 - n) * (1 + n)), t;
  return e < 6.25 ? (e -= 3.125, t = -364441206401782e-35, t = -16850591381820166e-35 + t * e, t = 128584807152564e-32 + t * e, t = 11157877678025181e-33 + t * e, t = -1333171662854621e-31 + t * e, t = 20972767875968562e-33 + t * e, t = 6637638134358324e-30 + t * e, t = -4054566272975207e-29 + t * e, t = -8151934197605472e-29 + t * e, t = 26335093153082323e-28 + t * e, t = -12975133253453532e-27 + t * e, t = -5415412054294628e-26 + t * e, t = 10512122733215323e-25 + t * e, t = -4112633980346984e-24 + t * e, t = -29070369957882005e-24 + t * e, t = 42347877827932404e-23 + t * e, t = -13654692000834679e-22 + t * e, t = -13882523362786469e-21 + t * e, t = 18673420803405714e-20 + t * e, t = -740702534166267e-18 + t * e, t = -0.006033670871430149 + t * e, t = 0.24015818242558962 + t * e, t = 1.6536545626831027 + t * e) : e < 16 ? (e = Math.sqrt(e) - 3.25, t = 22137376921775787e-25, t = 9075656193888539e-23 + t * e, t = -27517406297064545e-23 + t * e, t = 18239629214389228e-24 + t * e, t = 15027403968909828e-22 + t * e, t = -4013867526981546e-21 + t * e, t = 29234449089955446e-22 + t * e, t = 12475304481671779e-21 + t * e, t = -47318229009055734e-21 + t * e, t = 6828485145957318e-20 + t * e, t = 24031110387097894e-21 + t * e, t = -3550375203628475e-19 + t * e, t = 9532893797373805e-19 + t * e, t = -0.0016882755560235047 + t * e, t = 0.002491442096107851 + t * e, t = -0.003751208507569241 + t * e, t = 0.005370914553590064 + t * e, t = 1.0052589676941592 + t * e, t = 3.0838856104922208 + t * e) : Number.isFinite(e) ? (e = Math.sqrt(e) - 5, t = -27109920616438573e-27, t = -2555641816996525e-25 + t * e, t = 15076572693500548e-25 + t * e, t = -3789465440126737e-24 + t * e, t = 761570120807834e-23 + t * e, t = -1496002662714924e-23 + t * e, t = 2914795345090108e-23 + t * e, t = -6771199775845234e-23 + t * e, t = 22900482228026655e-23 + t * e, t = -99298272942317e-20 + t * e, t = 4526062597223154e-21 + t * e, t = -1968177810553167e-20 + t * e, t = 7599527703001776e-20 + t * e, t = -21503011930044477e-20 + t * e, t = -13871931833623122e-20 + t * e, t = 1.0103004648645344 + t * e, t = 4.849906401408584 + t * e) : t = 1 / 0, t * n;
}
function Ec(n, e) {
  let t, r;
  const i = {
    mean(u) {
      return arguments.length ? (t = u || 0, i) : t;
    },
    stdev(u) {
      return arguments.length ? (r = u ?? 1, i) : r;
    },
    sample: () => _a(t, r),
    pdf: (u) => Dc(u, t, r),
    cdf: (u) => Ka(u, t, r),
    icdf: (u) => no(u, t, r)
  };
  return i.mean(n).stdev(e);
}
function Pg(n, e) {
  const t = Ec();
  let r = 0;
  const i = {
    data(u) {
      return arguments.length ? (n = u, r = u ? u.length : 0, i.bandwidth(e)) : n;
    },
    bandwidth(u) {
      return arguments.length ? (e = u, !e && n && (e = $c(n)), i) : e;
    },
    sample() {
      return n[~~(Qn() * r)] + e * t.sample();
    },
    pdf(u) {
      let a = 0, o = 0;
      for (; o < r; ++o)
        a += t.pdf((u - n[o]) / e);
      return a / e / r;
    },
    cdf(u) {
      let a = 0, o = 0;
      for (; o < r; ++o)
        a += t.cdf((u - n[o]) / e);
      return a / r;
    },
    icdf() {
      throw Error("KDE icdf not supported.");
    }
  };
  return i.data(n);
}
function Fc(n, e) {
  return n = n || 0, e = e ?? 1, Math.exp(n + _a() * e);
}
function Ac(n, e, t) {
  if (n <= 0) return 0;
  e = e || 0, t = t ?? 1;
  const r = (Math.log(n) - e) / t;
  return Math.exp(-0.5 * r * r) / (t * Ja * n);
}
function kc(n, e, t) {
  return Ka(Math.log(n), e, t);
}
function Yc(n, e, t) {
  return Math.exp(no(n, e, t));
}
function Ig(n, e) {
  let t, r;
  const i = {
    mean(u) {
      return arguments.length ? (t = u || 0, i) : t;
    },
    stdev(u) {
      return arguments.length ? (r = u ?? 1, i) : r;
    },
    sample: () => Fc(t, r),
    pdf: (u) => Ac(u, t, r),
    cdf: (u) => kc(u, t, r),
    icdf: (u) => Yc(u, t, r)
  };
  return i.mean(n).stdev(e);
}
function Hg(n, e) {
  let t = 0, r;
  function i(a) {
    const o = [];
    let c = 0, f;
    for (f = 0; f < t; ++f)
      c += o[f] = a[f] == null ? 1 : +a[f];
    for (f = 0; f < t; ++f)
      o[f] /= c;
    return o;
  }
  const u = {
    weights(a) {
      return arguments.length ? (r = i(e = a || []), u) : e;
    },
    distributions(a) {
      return arguments.length ? (a ? (t = a.length, n = a) : (t = 0, n = []), u.weights(e)) : n;
    },
    sample() {
      const a = Qn();
      let o = n[t - 1], c = r[0], f = 0;
      for (; f < t - 1; c += r[++f])
        if (a < c) {
          o = n[f];
          break;
        }
      return o.sample();
    },
    pdf(a) {
      let o = 0, c = 0;
      for (; c < t; ++c)
        o += r[c] * n[c].pdf(a);
      return o;
    },
    cdf(a) {
      let o = 0, c = 0;
      for (; c < t; ++c)
        o += r[c] * n[c].cdf(a);
      return o;
    },
    icdf() {
      throw Error("Mixture icdf not supported.");
    }
  };
  return u.distributions(n).weights(e);
}
function Rc(n, e) {
  return e == null && (e = n ?? 1, n = 0), n + (e - n) * Qn();
}
function qc(n, e, t) {
  return t == null && (t = e ?? 1, e = 0), n >= e && n <= t ? 1 / (t - e) : 0;
}
function Pc(n, e, t) {
  return t == null && (t = e ?? 1, e = 0), n < e ? 0 : n > t ? 1 : (n - e) / (t - e);
}
function Ic(n, e, t) {
  return t == null && (t = e ?? 1, e = 0), n >= 0 && n <= 1 ? e + n * (t - e) : NaN;
}
function Lg(n, e) {
  let t, r;
  const i = {
    min(u) {
      return arguments.length ? (t = u || 0, i) : t;
    },
    max(u) {
      return arguments.length ? (r = u ?? 1, i) : r;
    },
    sample: () => Rc(t, r),
    pdf: (u) => qc(u, t, r),
    cdf: (u) => Pc(u, t, r),
    icdf: (u) => Ic(u, t, r)
  };
  return e == null && (e = n ?? 1, n = 0), i.min(n).max(e);
}
function Hc(n, e, t) {
  let r = 0, i = 0;
  for (const u of n) {
    const a = t(u);
    e(u) == null || a == null || isNaN(a) || (r += (a - r) / ++i);
  }
  return {
    coef: [r],
    predict: () => r,
    rSquared: 0
  };
}
function $t(n, e, t, r) {
  const i = r - n * n, u = Math.abs(i) < 1e-24 ? 0 : (t - n * e) / i;
  return [e - u * n, u];
}
function pr(n, e, t, r) {
  n = n.filter((g) => {
    let d = e(g), p = t(g);
    return d != null && (d = +d) >= d && p != null && (p = +p) >= p;
  }), r && n.sort((g, d) => e(g) - e(d));
  const i = n.length, u = new Float64Array(i), a = new Float64Array(i);
  let o = 0, c = 0, f = 0, l, s, h;
  for (h of n)
    u[o] = l = +e(h), a[o] = s = +t(h), ++o, c += (l - c) / o, f += (s - f) / o;
  for (o = 0; o < i; ++o)
    u[o] -= c, a[o] -= f;
  return [u, a, c, f];
}
function Ct(n, e, t, r) {
  let i = -1, u, a;
  for (const o of n)
    u = e(o), a = t(o), u != null && (u = +u) >= u && a != null && (a = +a) >= a && r(u, a, ++i);
}
function qe(n, e, t, r, i) {
  let u = 0, a = 0;
  return Ct(n, e, t, (o, c) => {
    const f = c - i(o), l = c - r;
    u += f * f, a += l * l;
  }), 1 - u / a;
}
function Lc(n, e, t) {
  let r = 0, i = 0, u = 0, a = 0, o = 0;
  Ct(n, e, t, (l, s) => {
    ++o, r += (l - r) / o, i += (s - i) / o, u += (l * s - u) / o, a += (l * l - a) / o;
  });
  const c = $t(r, i, u, a), f = (l) => c[0] + c[1] * l;
  return {
    coef: c,
    predict: f,
    rSquared: qe(n, e, t, i, f)
  };
}
function Og(n, e, t) {
  let r = 0, i = 0, u = 0, a = 0, o = 0;
  Ct(n, e, t, (l, s) => {
    ++o, l = Math.log(l), r += (l - r) / o, i += (s - i) / o, u += (l * s - u) / o, a += (l * l - a) / o;
  });
  const c = $t(r, i, u, a), f = (l) => c[0] + c[1] * Math.log(l);
  return {
    coef: c,
    predict: f,
    rSquared: qe(n, e, t, i, f)
  };
}
function zg(n, e, t) {
  const [r, i, u, a] = pr(n, e, t);
  let o = 0, c = 0, f = 0, l = 0, s = 0, h, g, d;
  Ct(n, e, t, (x, b) => {
    h = r[s++], g = Math.log(b), d = h * b, o += (b * g - o) / s, c += (d - c) / s, f += (d * g - f) / s, l += (h * d - l) / s;
  });
  const [p, m] = $t(c / a, o / a, f / a, l / a), M = (x) => Math.exp(p + m * (x - u));
  return {
    coef: [Math.exp(p - m * u), m],
    predict: M,
    rSquared: qe(n, e, t, a, M)
  };
}
function Wg(n, e, t) {
  let r = 0, i = 0, u = 0, a = 0, o = 0, c = 0;
  Ct(n, e, t, (s, h) => {
    const g = Math.log(s), d = Math.log(h);
    ++c, r += (g - r) / c, i += (d - i) / c, u += (g * d - u) / c, a += (g * g - a) / c, o += (h - o) / c;
  });
  const f = $t(r, i, u, a), l = (s) => f[0] * Math.pow(s, f[1]);
  return f[0] = Math.exp(f[0]), {
    coef: f,
    predict: l,
    rSquared: qe(n, e, t, o, l)
  };
}
function Oc(n, e, t) {
  const [r, i, u, a] = pr(n, e, t), o = r.length;
  let c = 0, f = 0, l = 0, s = 0, h = 0, g, d, p, m;
  for (g = 0; g < o; )
    d = r[g], p = i[g++], m = d * d, c += (m - c) / g, f += (m * d - f) / g, l += (m * m - l) / g, s += (d * p - s) / g, h += (m * p - h) / g;
  const M = l - c * c, x = c * M - f * f, b = (h * c - s * f) / x, y = (s * M - h * f) / x, T = -b * c, v = (C) => (C = C - u, b * C * C + y * C + T + a);
  return {
    coef: [T - y * u + b * u * u + a, y - 2 * b * u, b],
    predict: v,
    rSquared: qe(n, e, t, a, v)
  };
}
function Xg(n, e, t, r) {
  if (r === 0) return Hc(n, e, t);
  if (r === 1) return Lc(n, e, t);
  if (r === 2) return Oc(n, e, t);
  const [i, u, a, o] = pr(n, e, t), c = i.length, f = [], l = [], s = r + 1;
  let h, g, d, p, m;
  for (h = 0; h < s; ++h) {
    for (d = 0, p = 0; d < c; ++d)
      p += Math.pow(i[d], h) * u[d];
    for (f.push(p), m = new Float64Array(s), g = 0; g < s; ++g) {
      for (d = 0, p = 0; d < c; ++d)
        p += Math.pow(i[d], h + g);
      m[g] = p;
    }
    l.push(m);
  }
  l.push(f);
  const M = Wc(l), x = (b) => {
    b -= a;
    let y = o + M[0] + M[1] * b + M[2] * b * b;
    for (h = 3; h < s; ++h) y += M[h] * Math.pow(b, h);
    return y;
  };
  return {
    coef: zc(s, M, -a, o),
    predict: x,
    rSquared: qe(n, e, t, o, x)
  };
}
function zc(n, e, t, r) {
  const i = Array(n);
  let u, a, o, c;
  for (u = 0; u < n; ++u) i[u] = 0;
  for (u = n - 1; u >= 0; --u)
    for (o = e[u], c = 1, i[u] += o, a = 1; a <= u; ++a)
      c *= (u + 1 - a) / a, i[u - a] += o * Math.pow(t, a) * c;
  return i[0] += r, i;
}
function Wc(n) {
  const e = n.length - 1, t = [];
  let r, i, u, a, o;
  for (r = 0; r < e; ++r) {
    for (a = r, i = r + 1; i < e; ++i)
      Math.abs(n[r][i]) > Math.abs(n[r][a]) && (a = i);
    for (u = r; u < e + 1; ++u)
      o = n[u][r], n[u][r] = n[u][a], n[u][a] = o;
    for (i = r + 1; i < e; ++i)
      for (u = e; u >= r; u--)
        n[u][i] -= n[u][r] * n[r][i] / n[r][r];
  }
  for (i = e - 1; i >= 0; --i) {
    for (o = 0, u = i + 1; u < e; ++u)
      o += n[u][i] * t[u];
    t[i] = (n[e][i] - o) / n[i][i];
  }
  return t;
}
const Uu = 2, Eu = 1e-12;
function Bg(n, e, t, r) {
  const [i, u, a, o] = pr(n, e, t, !0), c = i.length, f = Math.max(2, ~~(r * c)), l = new Float64Array(c), s = new Float64Array(c), h = new Float64Array(c).fill(1);
  for (let g = -1; ++g <= Uu; ) {
    const d = [0, f - 1];
    for (let m = 0; m < c; ++m) {
      const M = i[m], x = d[0], b = d[1], y = M - i[x] > i[b] - M ? x : b;
      let T = 0, v = 0, C = 0, U = 0, k = 0;
      const I = 1 / Math.abs(i[y] - M || 1);
      for (let F = x; F <= b; ++F) {
        const Y = i[F], w = u[F], D = Xc(Math.abs(M - Y) * I) * h[F], z = Y * D;
        T += D, v += z, C += w * D, U += w * z, k += Y * z;
      }
      const [$, X] = $t(v / T, C / T, U / T, k / T);
      l[m] = $ + X * M, s[m] = Math.abs(u[m] - l[m]), Bc(i, m + 1, d);
    }
    if (g === Uu)
      break;
    const p = vc(s);
    if (Math.abs(p) < Eu) break;
    for (let m = 0, M, x; m < c; ++m)
      M = s[m] / (6 * p), h[m] = M >= 1 ? Eu : (x = 1 - M * M) * x;
  }
  return jc(i, l, a, o);
}
function Xc(n) {
  return (n = 1 - n * n * n) * n * n;
}
function Bc(n, e, t) {
  const r = n[e];
  let i = t[0], u = t[1] + 1;
  if (!(u >= n.length))
    for (; e > i && n[u] - r <= r - n[i]; )
      t[0] = ++i, t[1] = u, ++u;
}
function jc(n, e, t, r) {
  const i = n.length, u = [];
  let a = 0, o = 0, c = [], f;
  for (; a < i; ++a)
    f = n[a] + t, c[0] === f ? c[1] += (e[a] - c[1]) / ++o : (o = 0, c[1] += r, c = [f, e[a]], u.push(c));
  return c[1] += r, u;
}
const Gc = 0.5 * Math.PI / 180;
function jg(n, e, t, r) {
  t = t || 25, r = Math.max(t, r || 200);
  const i = (p) => [p, n(p)], u = e[0], a = e[1], o = a - u, c = o / r, f = [i(u)], l = [];
  if (t === r) {
    for (let p = 1; p < r; ++p)
      f.push(i(u + p / t * o));
    return f.push(i(a)), f;
  } else {
    l.push(i(a));
    for (let p = t; --p > 0; )
      l.push(i(u + p / t * o));
  }
  let s = f[0], h = l[l.length - 1];
  const g = 1 / o, d = Zc(s[1], l);
  for (; h; ) {
    const p = i((s[0] + h[0]) / 2);
    p[0] - s[0] >= c && Qc(s, p, h, g, d) > Gc ? l.push(p) : (s = h, f.push(h), l.pop()), h = l[l.length - 1];
  }
  return f;
}
function Zc(n, e) {
  let t = n, r = n;
  const i = e.length;
  for (let u = 0; u < i; ++u) {
    const a = e[u][1];
    a < t && (t = a), a > r && (r = a);
  }
  return 1 / (r - t);
}
function Qc(n, e, t, r, i) {
  const u = Math.atan2(i * (t[1] - n[1]), r * (t[0] - n[0])), a = Math.atan2(i * (e[1] - n[1]), r * (e[0] - n[0]));
  return Math.abs(u - a);
}
function Gg(n, e) {
  if (typeof document < "u" && document.createElement) {
    const t = document.createElement("canvas");
    if (t && t.getContext)
      return t.width = n, t.height = e, t;
  }
  return null;
}
const Zg = () => typeof Image < "u" ? Image : null;
var A = 1e-6, eo = 1e-12, q = Math.PI, Z = q / 2, Fu = q / 4, gn = q * 2, tn = 180 / q, G = q / 180, O = Math.abs, Pe = Math.atan, On = Math.atan2, R = Math.cos, Qg = Math.ceil, to = Math.exp, Vg = Math.hypot, jt = Math.log, Er = Math.pow, E = Math.sin, pn = Math.sign || function(n) {
  return n > 0 ? 1 : n < 0 ? -1 : 0;
}, cn = Math.sqrt, Ai = Math.tan;
function ro(n) {
  return n > 1 ? 0 : n < -1 ? q : Math.acos(n);
}
function yn(n) {
  return n > 1 ? Z : n < -1 ? -Z : Math.asin(n);
}
function mn() {
}
function Gt(n, e) {
  n && ku.hasOwnProperty(n.type) && ku[n.type](n, e);
}
var Au = {
  Feature: function(n, e) {
    Gt(n.geometry, e);
  },
  FeatureCollection: function(n, e) {
    for (var t = n.features, r = -1, i = t.length; ++r < i; ) Gt(t[r].geometry, e);
  }
}, ku = {
  Sphere: function(n, e) {
    e.sphere();
  },
  Point: function(n, e) {
    n = n.coordinates, e.point(n[0], n[1], n[2]);
  },
  MultiPoint: function(n, e) {
    for (var t = n.coordinates, r = -1, i = t.length; ++r < i; ) n = t[r], e.point(n[0], n[1], n[2]);
  },
  LineString: function(n, e) {
    Kr(n.coordinates, e, 0);
  },
  MultiLineString: function(n, e) {
    for (var t = n.coordinates, r = -1, i = t.length; ++r < i; ) Kr(t[r], e, 0);
  },
  Polygon: function(n, e) {
    Yu(n.coordinates, e);
  },
  MultiPolygon: function(n, e) {
    for (var t = n.coordinates, r = -1, i = t.length; ++r < i; ) Yu(t[r], e);
  },
  GeometryCollection: function(n, e) {
    for (var t = n.geometries, r = -1, i = t.length; ++r < i; ) Gt(t[r], e);
  }
};
function Kr(n, e, t) {
  var r = -1, i = n.length - t, u;
  for (e.lineStart(); ++r < i; ) u = n[r], e.point(u[0], u[1], u[2]);
  e.lineEnd();
}
function Yu(n, e) {
  var t = -1, r = n.length;
  for (e.polygonStart(); ++t < r; ) Kr(n[t], e, 1);
  e.polygonEnd();
}
function xe(n, e) {
  n && Au.hasOwnProperty(n.type) ? Au[n.type](n, e) : Gt(n, e);
}
function ni(n) {
  return [On(n[1], n[0]), yn(n[2])];
}
function Ne(n) {
  var e = n[0], t = n[1], r = R(t);
  return [r * R(e), r * E(e), E(t)];
}
function Yt(n, e) {
  return n[0] * e[0] + n[1] * e[1] + n[2] * e[2];
}
function Zt(n, e) {
  return [n[1] * e[2] - n[2] * e[1], n[2] * e[0] - n[0] * e[2], n[0] * e[1] - n[1] * e[0]];
}
function Fr(n, e) {
  n[0] += e[0], n[1] += e[1], n[2] += e[2];
}
function Rt(n, e) {
  return [n[0] * e, n[1] * e, n[2] * e];
}
function ei(n) {
  var e = cn(n[0] * n[0] + n[1] * n[1] + n[2] * n[2]);
  n[0] /= e, n[1] /= e, n[2] /= e;
}
function ti(n, e) {
  function t(r, i) {
    return r = n(r, i), e(r[0], r[1]);
  }
  return n.invert && e.invert && (t.invert = function(r, i) {
    return r = e.invert(r, i), r && n.invert(r[0], r[1]);
  }), t;
}
function ri(n, e) {
  return O(n) > q && (n -= Math.round(n / gn) * gn), [n, e];
}
ri.invert = ri;
function io(n, e, t) {
  return (n %= gn) ? e || t ? ti(qu(n), Pu(e, t)) : qu(n) : e || t ? Pu(e, t) : ri;
}
function Ru(n) {
  return function(e, t) {
    return e += n, O(e) > q && (e -= Math.round(e / gn) * gn), [e, t];
  };
}
function qu(n) {
  var e = Ru(n);
  return e.invert = Ru(-n), e;
}
function Pu(n, e) {
  var t = R(n), r = E(n), i = R(e), u = E(e);
  function a(o, c) {
    var f = R(c), l = R(o) * f, s = E(o) * f, h = E(c), g = h * t + l * r;
    return [
      On(s * i - g * u, l * t - h * r),
      yn(g * i + s * u)
    ];
  }
  return a.invert = function(o, c) {
    var f = R(c), l = R(o) * f, s = E(o) * f, h = E(c), g = h * i - s * u;
    return [
      On(s * i + h * u, l * t + g * r),
      yn(g * t - l * r)
    ];
  }, a;
}
function Vc(n) {
  n = io(n[0] * G, n[1] * G, n.length > 2 ? n[2] * G : 0);
  function e(t) {
    return t = n(t[0] * G, t[1] * G), t[0] *= tn, t[1] *= tn, t;
  }
  return e.invert = function(t) {
    return t = n.invert(t[0] * G, t[1] * G), t[0] *= tn, t[1] *= tn, t;
  }, e;
}
function Jc(n, e, t, r, i, u) {
  if (t) {
    var a = R(e), o = E(e), c = r * t;
    i == null ? (i = e + r * gn, u = e - c / 2) : (i = Iu(a, i), u = Iu(a, u), (r > 0 ? i < u : i > u) && (i += r * gn));
    for (var f, l = i; r > 0 ? l > u : l < u; l -= c)
      f = ni([a, -o * R(l), -o * E(l)]), n.point(f[0], f[1]);
  }
}
function Iu(n, e) {
  e = Ne(e), e[0] -= n, ei(e);
  var t = ro(-e[1]);
  return ((-e[2] < 0 ? -t : t) + gn - A) % gn;
}
function uo() {
  var n = [], e;
  return {
    point: function(t, r, i) {
      e.push([t, r, i]);
    },
    lineStart: function() {
      n.push(e = []);
    },
    lineEnd: mn,
    rejoin: function() {
      n.length > 1 && n.push(n.pop().concat(n.shift()));
    },
    result: function() {
      var t = n;
      return n = [], e = null, t;
    }
  };
}
function Wt(n, e) {
  return O(n[0] - e[0]) < A && O(n[1] - e[1]) < A;
}
function qt(n, e, t, r) {
  this.x = n, this.z = e, this.o = t, this.e = r, this.v = !1, this.n = this.p = null;
}
function ao(n, e, t, r, i) {
  var u = [], a = [], o, c;
  if (n.forEach(function(d) {
    if (!((p = d.length - 1) <= 0)) {
      var p, m = d[0], M = d[p], x;
      if (Wt(m, M)) {
        if (!m[2] && !M[2]) {
          for (i.lineStart(), o = 0; o < p; ++o) i.point((m = d[o])[0], m[1]);
          i.lineEnd();
          return;
        }
        M[0] += 2 * A;
      }
      u.push(x = new qt(m, d, null, !0)), a.push(x.o = new qt(m, null, x, !1)), u.push(x = new qt(M, d, null, !1)), a.push(x.o = new qt(M, null, x, !0));
    }
  }), !!u.length) {
    for (a.sort(e), Hu(u), Hu(a), o = 0, c = a.length; o < c; ++o)
      a[o].e = t = !t;
    for (var f = u[0], l, s; ; ) {
      for (var h = f, g = !0; h.v; ) if ((h = h.n) === f) return;
      l = h.z, i.lineStart();
      do {
        if (h.v = h.o.v = !0, h.e) {
          if (g)
            for (o = 0, c = l.length; o < c; ++o) i.point((s = l[o])[0], s[1]);
          else
            r(h.x, h.n.x, 1, i);
          h = h.n;
        } else {
          if (g)
            for (l = h.p.z, o = l.length - 1; o >= 0; --o) i.point((s = l[o])[0], s[1]);
          else
            r(h.x, h.p.x, -1, i);
          h = h.p;
        }
        h = h.o, l = h.z, g = !g;
      } while (!h.v);
      i.lineEnd();
    }
  }
}
function Hu(n) {
  if (e = n.length) {
    for (var e, t = 0, r = n[0], i; ++t < e; )
      r.n = i = n[t], i.p = r, r = i;
    r.n = i = n[0], i.p = r;
  }
}
function Ar(n) {
  return O(n[0]) <= q ? n[0] : pn(n[0]) * ((O(n[0]) + q) % gn - q);
}
function _c(n, e) {
  var t = Ar(e), r = e[1], i = E(r), u = [E(t), -R(t), 0], a = 0, o = 0, c = new le();
  i === 1 ? r = Z + A : i === -1 && (r = -Z - A);
  for (var f = 0, l = n.length; f < l; ++f)
    if (h = (s = n[f]).length)
      for (var s, h, g = s[h - 1], d = Ar(g), p = g[1] / 2 + Fu, m = E(p), M = R(p), x = 0; x < h; ++x, d = y, m = v, M = C, g = b) {
        var b = s[x], y = Ar(b), T = b[1] / 2 + Fu, v = E(T), C = R(T), U = y - d, k = U >= 0 ? 1 : -1, I = k * U, $ = I > q, X = m * v;
        if (c.add(On(X * k * E(I), M * C + X * R(I))), a += $ ? U + k * gn : U, $ ^ d >= t ^ y >= t) {
          var F = Zt(Ne(g), Ne(b));
          ei(F);
          var Y = Zt(u, F);
          ei(Y);
          var w = ($ ^ U >= 0 ? -1 : 1) * yn(Y[2]);
          (r > w || r === w && (F[0] || F[1])) && (o += $ ^ U >= 0 ? 1 : -1);
        }
      }
  return (a < -A || a < A && c < -eo) ^ o & 1;
}
function oo(n, e, t, r) {
  return function(i) {
    var u = e(i), a = uo(), o = e(a), c = !1, f, l, s, h = {
      point: g,
      lineStart: p,
      lineEnd: m,
      polygonStart: function() {
        h.point = M, h.lineStart = x, h.lineEnd = b, l = [], f = [];
      },
      polygonEnd: function() {
        h.point = g, h.lineStart = p, h.lineEnd = m, l = Qa(l);
        var y = _c(f, r);
        l.length ? (c || (i.polygonStart(), c = !0), ao(l, nl, y, t, i)) : y && (c || (i.polygonStart(), c = !0), i.lineStart(), t(null, null, 1, i), i.lineEnd()), c && (i.polygonEnd(), c = !1), l = f = null;
      },
      sphere: function() {
        i.polygonStart(), i.lineStart(), t(null, null, 1, i), i.lineEnd(), i.polygonEnd();
      }
    };
    function g(y, T) {
      n(y, T) && i.point(y, T);
    }
    function d(y, T) {
      u.point(y, T);
    }
    function p() {
      h.point = d, u.lineStart();
    }
    function m() {
      h.point = g, u.lineEnd();
    }
    function M(y, T) {
      s.push([y, T]), o.point(y, T);
    }
    function x() {
      o.lineStart(), s = [];
    }
    function b() {
      M(s[0][0], s[0][1]), o.lineEnd();
      var y = o.clean(), T = a.result(), v, C = T.length, U, k, I;
      if (s.pop(), f.push(s), s = null, !!C) {
        if (y & 1) {
          if (k = T[0], (U = k.length - 1) > 0) {
            for (c || (i.polygonStart(), c = !0), i.lineStart(), v = 0; v < U; ++v) i.point((I = k[v])[0], I[1]);
            i.lineEnd();
          }
          return;
        }
        C > 1 && y & 2 && T.push(T.pop().concat(T.shift())), l.push(T.filter(Kc));
      }
    }
    return h;
  };
}
function Kc(n) {
  return n.length > 1;
}
function nl(n, e) {
  return ((n = n.x)[0] < 0 ? n[1] - Z - A : Z - n[1]) - ((e = e.x)[0] < 0 ? e[1] - Z - A : Z - e[1]);
}
const Lu = oo(
  function() {
    return !0;
  },
  el,
  rl,
  [-q, -Z]
);
function el(n) {
  var e = NaN, t = NaN, r = NaN, i;
  return {
    lineStart: function() {
      n.lineStart(), i = 1;
    },
    point: function(u, a) {
      var o = u > 0 ? q : -q, c = O(u - e);
      O(c - q) < A ? (n.point(e, t = (t + a) / 2 > 0 ? Z : -Z), n.point(r, t), n.lineEnd(), n.lineStart(), n.point(o, t), n.point(u, t), i = 0) : r !== o && c >= q && (O(e - r) < A && (e -= r * A), O(u - o) < A && (u -= o * A), t = tl(e, t, u, a), n.point(r, t), n.lineEnd(), n.lineStart(), n.point(o, t), i = 0), n.point(e = u, t = a), r = o;
    },
    lineEnd: function() {
      n.lineEnd(), e = t = NaN;
    },
    clean: function() {
      return 2 - i;
    }
  };
}
function tl(n, e, t, r) {
  var i, u, a = E(n - t);
  return O(a) > A ? Pe((E(e) * (u = R(r)) * E(t) - E(r) * (i = R(e)) * E(n)) / (i * u * a)) : (e + r) / 2;
}
function rl(n, e, t, r) {
  var i;
  if (n == null)
    i = t * Z, r.point(-q, i), r.point(0, i), r.point(q, i), r.point(q, 0), r.point(q, -i), r.point(0, -i), r.point(-q, -i), r.point(-q, 0), r.point(-q, i);
  else if (O(n[0] - e[0]) > A) {
    var u = n[0] < e[0] ? q : -q;
    i = t * u / 2, r.point(-u, i), r.point(0, i), r.point(u, i);
  } else
    r.point(e[0], e[1]);
}
function il(n) {
  var e = R(n), t = 2 * G, r = e > 0, i = O(e) > A;
  function u(l, s, h, g) {
    Jc(g, n, t, h, l, s);
  }
  function a(l, s) {
    return R(l) * R(s) > e;
  }
  function o(l) {
    var s, h, g, d, p;
    return {
      lineStart: function() {
        d = g = !1, p = 1;
      },
      point: function(m, M) {
        var x = [m, M], b, y = a(m, M), T = r ? y ? 0 : f(m, M) : y ? f(m + (m < 0 ? q : -q), M) : 0;
        if (!s && (d = g = y) && l.lineStart(), y !== g && (b = c(s, x), (!b || Wt(s, b) || Wt(x, b)) && (x[2] = 1)), y !== g)
          p = 0, y ? (l.lineStart(), b = c(x, s), l.point(b[0], b[1])) : (b = c(s, x), l.point(b[0], b[1], 2), l.lineEnd()), s = b;
        else if (i && s && r ^ y) {
          var v;
          !(T & h) && (v = c(x, s, !0)) && (p = 0, r ? (l.lineStart(), l.point(v[0][0], v[0][1]), l.point(v[1][0], v[1][1]), l.lineEnd()) : (l.point(v[1][0], v[1][1]), l.lineEnd(), l.lineStart(), l.point(v[0][0], v[0][1], 3)));
        }
        y && (!s || !Wt(s, x)) && l.point(x[0], x[1]), s = x, g = y, h = T;
      },
      lineEnd: function() {
        g && l.lineEnd(), s = null;
      },
      // Rejoin first and last segments if there were intersections and the first
      // and last points were visible.
      clean: function() {
        return p | (d && g) << 1;
      }
    };
  }
  function c(l, s, h) {
    var g = Ne(l), d = Ne(s), p = [1, 0, 0], m = Zt(g, d), M = Yt(m, m), x = m[0], b = M - x * x;
    if (!b) return !h && l;
    var y = e * M / b, T = -e * x / b, v = Zt(p, m), C = Rt(p, y), U = Rt(m, T);
    Fr(C, U);
    var k = v, I = Yt(C, k), $ = Yt(k, k), X = I * I - $ * (Yt(C, C) - 1);
    if (!(X < 0)) {
      var F = cn(X), Y = Rt(k, (-I - F) / $);
      if (Fr(Y, C), Y = ni(Y), !h) return Y;
      var w = l[0], D = s[0], z = l[1], Q = s[1], j;
      D < w && (j = w, w = D, D = j);
      var te = D - w, vn = O(te - q) < A, Rn = vn || te < A;
      if (!vn && Q < z && (j = z, z = Q, Q = j), Rn ? vn ? z + Q > 0 ^ Y[1] < (O(Y[0] - w) < A ? z : Q) : z <= Y[1] && Y[1] <= Q : te > q ^ (w <= Y[0] && Y[0] <= D)) {
        var wn = Rt(k, (-I + F) / $);
        return Fr(wn, C), [Y, ni(wn)];
      }
    }
  }
  function f(l, s) {
    var h = r ? n : q - n, g = 0;
    return l < -h ? g |= 1 : l > h && (g |= 2), s < -h ? g |= 4 : s > h && (g |= 8), g;
  }
  return oo(a, o, u, r ? [0, -n] : [-q, n - q]);
}
function ul(n, e, t, r, i, u) {
  var a = n[0], o = n[1], c = e[0], f = e[1], l = 0, s = 1, h = c - a, g = f - o, d;
  if (d = t - a, !(!h && d > 0)) {
    if (d /= h, h < 0) {
      if (d < l) return;
      d < s && (s = d);
    } else if (h > 0) {
      if (d > s) return;
      d > l && (l = d);
    }
    if (d = i - a, !(!h && d < 0)) {
      if (d /= h, h < 0) {
        if (d > s) return;
        d > l && (l = d);
      } else if (h > 0) {
        if (d < l) return;
        d < s && (s = d);
      }
      if (d = r - o, !(!g && d > 0)) {
        if (d /= g, g < 0) {
          if (d < l) return;
          d < s && (s = d);
        } else if (g > 0) {
          if (d > s) return;
          d > l && (l = d);
        }
        if (d = u - o, !(!g && d < 0)) {
          if (d /= g, g < 0) {
            if (d > s) return;
            d > l && (l = d);
          } else if (g > 0) {
            if (d < l) return;
            d < s && (s = d);
          }
          return l > 0 && (n[0] = a + l * h, n[1] = o + l * g), s < 1 && (e[0] = a + s * h, e[1] = o + s * g), !0;
        }
      }
    }
  }
}
var Qe = 1e9, Pt = -Qe;
function fo(n, e, t, r) {
  function i(f, l) {
    return n <= f && f <= t && e <= l && l <= r;
  }
  function u(f, l, s, h) {
    var g = 0, d = 0;
    if (f == null || (g = a(f, s)) !== (d = a(l, s)) || c(f, l) < 0 ^ s > 0)
      do
        h.point(g === 0 || g === 3 ? n : t, g > 1 ? r : e);
      while ((g = (g + s + 4) % 4) !== d);
    else
      h.point(l[0], l[1]);
  }
  function a(f, l) {
    return O(f[0] - n) < A ? l > 0 ? 0 : 3 : O(f[0] - t) < A ? l > 0 ? 2 : 1 : O(f[1] - e) < A ? l > 0 ? 1 : 0 : l > 0 ? 3 : 2;
  }
  function o(f, l) {
    return c(f.x, l.x);
  }
  function c(f, l) {
    var s = a(f, 1), h = a(l, 1);
    return s !== h ? s - h : s === 0 ? l[1] - f[1] : s === 1 ? f[0] - l[0] : s === 2 ? f[1] - l[1] : l[0] - f[0];
  }
  return function(f) {
    var l = f, s = uo(), h, g, d, p, m, M, x, b, y, T, v, C = {
      point: U,
      lineStart: X,
      lineEnd: F,
      polygonStart: I,
      polygonEnd: $
    };
    function U(w, D) {
      i(w, D) && l.point(w, D);
    }
    function k() {
      for (var w = 0, D = 0, z = g.length; D < z; ++D)
        for (var Q = g[D], j = 1, te = Q.length, vn = Q[0], Rn, wn, ve = vn[0], Zn = vn[1]; j < te; ++j)
          Rn = ve, wn = Zn, vn = Q[j], ve = vn[0], Zn = vn[1], wn <= r ? Zn > r && (ve - Rn) * (r - wn) > (Zn - wn) * (n - Rn) && ++w : Zn <= r && (ve - Rn) * (r - wn) < (Zn - wn) * (n - Rn) && --w;
      return w;
    }
    function I() {
      l = s, h = [], g = [], v = !0;
    }
    function $() {
      var w = k(), D = v && w, z = (h = Qa(h)).length;
      (D || z) && (f.polygonStart(), D && (f.lineStart(), u(null, null, 1, f), f.lineEnd()), z && ao(h, o, w, u, f), f.polygonEnd()), l = f, h = g = d = null;
    }
    function X() {
      C.point = Y, g && g.push(d = []), T = !0, y = !1, x = b = NaN;
    }
    function F() {
      h && (Y(p, m), M && y && s.rejoin(), h.push(s.result())), C.point = U, y && l.lineEnd();
    }
    function Y(w, D) {
      var z = i(w, D);
      if (g && d.push([w, D]), T)
        p = w, m = D, M = z, T = !1, z && (l.lineStart(), l.point(w, D));
      else if (z && y) l.point(w, D);
      else {
        var Q = [x = Math.max(Pt, Math.min(Qe, x)), b = Math.max(Pt, Math.min(Qe, b))], j = [w = Math.max(Pt, Math.min(Qe, w)), D = Math.max(Pt, Math.min(Qe, D))];
        ul(Q, j, n, e, t, r) ? (y || (l.lineStart(), l.point(Q[0], Q[1])), l.point(j[0], j[1]), z || l.lineEnd(), v = !1) : z && (l.lineStart(), l.point(w, D), v = !1);
      }
      x = w, b = D, y = z;
    }
    return C;
  };
}
const gt = (n) => n;
var kr = new le(), ii = new le(), co, lo, ui, ai, qn = {
  point: mn,
  lineStart: mn,
  lineEnd: mn,
  polygonStart: function() {
    qn.lineStart = al, qn.lineEnd = fl;
  },
  polygonEnd: function() {
    qn.lineStart = qn.lineEnd = qn.point = mn, kr.add(O(ii)), ii = new le();
  },
  result: function() {
    var n = kr / 2;
    return kr = new le(), n;
  }
};
function al() {
  qn.point = ol;
}
function ol(n, e) {
  qn.point = so, co = ui = n, lo = ai = e;
}
function so(n, e) {
  ii.add(ai * n - ui * e), ui = n, ai = e;
}
function fl() {
  so(co, lo);
}
var De = 1 / 0, Qt = De, dt = -De, Vt = dt, Jt = {
  point: cl,
  lineStart: mn,
  lineEnd: mn,
  polygonStart: mn,
  polygonEnd: mn,
  result: function() {
    var n = [[De, Qt], [dt, Vt]];
    return dt = Vt = -(Qt = De = 1 / 0), n;
  }
};
function cl(n, e) {
  n < De && (De = n), n > dt && (dt = n), e < Qt && (Qt = e), e > Vt && (Vt = e);
}
var oi = 0, fi = 0, Ve = 0, _t = 0, Kt = 0, Te = 0, ci = 0, li = 0, Je = 0, ho, go, Cn, Nn, dn = {
  point: se,
  lineStart: Ou,
  lineEnd: zu,
  polygonStart: function() {
    dn.lineStart = hl, dn.lineEnd = gl;
  },
  polygonEnd: function() {
    dn.point = se, dn.lineStart = Ou, dn.lineEnd = zu;
  },
  result: function() {
    var n = Je ? [ci / Je, li / Je] : Te ? [_t / Te, Kt / Te] : Ve ? [oi / Ve, fi / Ve] : [NaN, NaN];
    return oi = fi = Ve = _t = Kt = Te = ci = li = Je = 0, n;
  }
};
function se(n, e) {
  oi += n, fi += e, ++Ve;
}
function Ou() {
  dn.point = ll;
}
function ll(n, e) {
  dn.point = sl, se(Cn = n, Nn = e);
}
function sl(n, e) {
  var t = n - Cn, r = e - Nn, i = cn(t * t + r * r);
  _t += i * (Cn + n) / 2, Kt += i * (Nn + e) / 2, Te += i, se(Cn = n, Nn = e);
}
function zu() {
  dn.point = se;
}
function hl() {
  dn.point = dl;
}
function gl() {
  po(ho, go);
}
function dl(n, e) {
  dn.point = po, se(ho = Cn = n, go = Nn = e);
}
function po(n, e) {
  var t = n - Cn, r = e - Nn, i = cn(t * t + r * r);
  _t += i * (Cn + n) / 2, Kt += i * (Nn + e) / 2, Te += i, i = Nn * n - Cn * e, ci += i * (Cn + n), li += i * (Nn + e), Je += i * 3, se(Cn = n, Nn = e);
}
function mo(n) {
  this._context = n;
}
mo.prototype = {
  _radius: 4.5,
  pointRadius: function(n) {
    return this._radius = n, this;
  },
  polygonStart: function() {
    this._line = 0;
  },
  polygonEnd: function() {
    this._line = NaN;
  },
  lineStart: function() {
    this._point = 0;
  },
  lineEnd: function() {
    this._line === 0 && this._context.closePath(), this._point = NaN;
  },
  point: function(n, e) {
    switch (this._point) {
      case 0: {
        this._context.moveTo(n, e), this._point = 1;
        break;
      }
      case 1: {
        this._context.lineTo(n, e);
        break;
      }
      default: {
        this._context.moveTo(n + this._radius, e), this._context.arc(n, e, this._radius, 0, gn);
        break;
      }
    }
  },
  result: mn
};
var si = new le(), Yr, bo, yo, _e, Ke, pt = {
  point: mn,
  lineStart: function() {
    pt.point = pl;
  },
  lineEnd: function() {
    Yr && Mo(bo, yo), pt.point = mn;
  },
  polygonStart: function() {
    Yr = !0;
  },
  polygonEnd: function() {
    Yr = null;
  },
  result: function() {
    var n = +si;
    return si = new le(), n;
  }
};
function pl(n, e) {
  pt.point = Mo, bo = _e = n, yo = Ke = e;
}
function Mo(n, e) {
  _e -= n, Ke -= e, si.add(cn(_e * _e + Ke * Ke)), _e = n, Ke = e;
}
let Wu, nr, Xu, Bu;
class ju {
  constructor(e) {
    this._append = e == null ? vo : ml(e), this._radius = 4.5, this._ = "";
  }
  pointRadius(e) {
    return this._radius = +e, this;
  }
  polygonStart() {
    this._line = 0;
  }
  polygonEnd() {
    this._line = NaN;
  }
  lineStart() {
    this._point = 0;
  }
  lineEnd() {
    this._line === 0 && (this._ += "Z"), this._point = NaN;
  }
  point(e, t) {
    switch (this._point) {
      case 0: {
        this._append`M${e},${t}`, this._point = 1;
        break;
      }
      case 1: {
        this._append`L${e},${t}`;
        break;
      }
      default: {
        if (this._append`M${e},${t}`, this._radius !== Xu || this._append !== nr) {
          const r = this._radius, i = this._;
          this._ = "", this._append`m0,${r}a${r},${r} 0 1,1 0,${-2 * r}a${r},${r} 0 1,1 0,${2 * r}z`, Xu = r, nr = this._append, Bu = this._, this._ = i;
        }
        this._ += Bu;
        break;
      }
    }
  }
  result() {
    const e = this._;
    return this._ = "", e.length ? e : null;
  }
}
function vo(n) {
  let e = 1;
  this._ += n[0];
  for (const t = n.length; e < t; ++e)
    this._ += arguments[e] + n[e];
}
function ml(n) {
  const e = Math.floor(n);
  if (!(e >= 0)) throw new RangeError(`invalid digits: ${n}`);
  if (e > 15) return vo;
  if (e !== Wu) {
    const t = 10 ** e;
    Wu = e, nr = function(i) {
      let u = 1;
      this._ += i[0];
      for (const a = i.length; u < a; ++u)
        this._ += Math.round(arguments[u] * t) / t + i[u];
    };
  }
  return nr;
}
function wo(n, e) {
  let t = 3, r = 4.5, i, u;
  function a(o) {
    return o && (typeof r == "function" && u.pointRadius(+r.apply(this, arguments)), xe(o, i(u))), u.result();
  }
  return a.area = function(o) {
    return xe(o, i(qn)), qn.result();
  }, a.measure = function(o) {
    return xe(o, i(pt)), pt.result();
  }, a.bounds = function(o) {
    return xe(o, i(Jt)), Jt.result();
  }, a.centroid = function(o) {
    return xe(o, i(dn)), dn.result();
  }, a.projection = function(o) {
    return arguments.length ? (i = o == null ? (n = null, gt) : (n = o).stream, a) : n;
  }, a.context = function(o) {
    return arguments.length ? (u = o == null ? (e = null, new ju(t)) : new mo(e = o), typeof r != "function" && u.pointRadius(r), a) : e;
  }, a.pointRadius = function(o) {
    return arguments.length ? (r = typeof o == "function" ? o : (u.pointRadius(+o), +o), a) : r;
  }, a.digits = function(o) {
    if (!arguments.length) return t;
    if (o == null) t = null;
    else {
      const c = Math.floor(o);
      if (!(c >= 0)) throw new RangeError(`invalid digits: ${o}`);
      t = c;
    }
    return e === null && (u = new ju(t)), a;
  }, a.projection(n).digits(t).context(e);
}
function mr(n) {
  return function(e) {
    var t = new hi();
    for (var r in n) t[r] = n[r];
    return t.stream = e, t;
  };
}
function hi() {
}
hi.prototype = {
  constructor: hi,
  point: function(n, e) {
    this.stream.point(n, e);
  },
  sphere: function() {
    this.stream.sphere();
  },
  lineStart: function() {
    this.stream.lineStart();
  },
  lineEnd: function() {
    this.stream.lineEnd();
  },
  polygonStart: function() {
    this.stream.polygonStart();
  },
  polygonEnd: function() {
    this.stream.polygonEnd();
  }
};
function ki(n, e, t) {
  var r = n.clipExtent && n.clipExtent();
  return n.scale(150).translate([0, 0]), r != null && n.clipExtent(null), xe(t, n.stream(Jt)), e(Jt.result()), r != null && n.clipExtent(r), n;
}
function br(n, e, t) {
  return ki(n, function(r) {
    var i = e[1][0] - e[0][0], u = e[1][1] - e[0][1], a = Math.min(i / (r[1][0] - r[0][0]), u / (r[1][1] - r[0][1])), o = +e[0][0] + (i - a * (r[1][0] + r[0][0])) / 2, c = +e[0][1] + (u - a * (r[1][1] + r[0][1])) / 2;
    n.scale(150 * a).translate([o, c]);
  }, t);
}
function Yi(n, e, t) {
  return br(n, [[0, 0], e], t);
}
function Ri(n, e, t) {
  return ki(n, function(r) {
    var i = +e, u = i / (r[1][0] - r[0][0]), a = (i - u * (r[1][0] + r[0][0])) / 2, o = -u * r[0][1];
    n.scale(150 * u).translate([a, o]);
  }, t);
}
function qi(n, e, t) {
  return ki(n, function(r) {
    var i = +e, u = i / (r[1][1] - r[0][1]), a = -u * r[0][0], o = (i - u * (r[1][1] + r[0][1])) / 2;
    n.scale(150 * u).translate([a, o]);
  }, t);
}
var Gu = 16, bl = R(30 * G);
function Zu(n, e) {
  return +e ? Ml(n, e) : yl(n);
}
function yl(n) {
  return mr({
    point: function(e, t) {
      e = n(e, t), this.stream.point(e[0], e[1]);
    }
  });
}
function Ml(n, e) {
  function t(r, i, u, a, o, c, f, l, s, h, g, d, p, m) {
    var M = f - r, x = l - i, b = M * M + x * x;
    if (b > 4 * e && p--) {
      var y = a + h, T = o + g, v = c + d, C = cn(y * y + T * T + v * v), U = yn(v /= C), k = O(O(v) - 1) < A || O(u - s) < A ? (u + s) / 2 : On(T, y), I = n(k, U), $ = I[0], X = I[1], F = $ - r, Y = X - i, w = x * F - M * Y;
      (w * w / b > e || O((M * F + x * Y) / b - 0.5) > 0.3 || a * h + o * g + c * d < bl) && (t(r, i, u, a, o, c, $, X, k, y /= C, T /= C, v, p, m), m.point($, X), t($, X, k, y, T, v, f, l, s, h, g, d, p, m));
    }
  }
  return function(r) {
    var i, u, a, o, c, f, l, s, h, g, d, p, m = {
      point: M,
      lineStart: x,
      lineEnd: y,
      polygonStart: function() {
        r.polygonStart(), m.lineStart = T;
      },
      polygonEnd: function() {
        r.polygonEnd(), m.lineStart = x;
      }
    };
    function M(U, k) {
      U = n(U, k), r.point(U[0], U[1]);
    }
    function x() {
      s = NaN, m.point = b, r.lineStart();
    }
    function b(U, k) {
      var I = Ne([U, k]), $ = n(U, k);
      t(s, h, l, g, d, p, s = $[0], h = $[1], l = U, g = I[0], d = I[1], p = I[2], Gu, r), r.point(s, h);
    }
    function y() {
      m.point = M, r.lineEnd();
    }
    function T() {
      x(), m.point = v, m.lineEnd = C;
    }
    function v(U, k) {
      b(i = U, k), u = s, a = h, o = g, c = d, f = p, m.point = b;
    }
    function C() {
      t(s, h, l, g, d, p, u, a, i, o, c, f, Gu, r), m.lineEnd = y, y();
    }
    return m;
  };
}
var vl = mr({
  point: function(n, e) {
    this.stream.point(n * G, e * G);
  }
});
function wl(n) {
  return mr({
    point: function(e, t) {
      var r = n(e, t);
      return this.stream.point(r[0], r[1]);
    }
  });
}
function xl(n, e, t, r, i) {
  function u(a, o) {
    return a *= r, o *= i, [e + n * a, t - n * o];
  }
  return u.invert = function(a, o) {
    return [(a - e) / n * r, (t - o) / n * i];
  }, u;
}
function Qu(n, e, t, r, i, u) {
  if (!u) return xl(n, e, t, r, i);
  var a = R(u), o = E(u), c = a * n, f = o * n, l = a / n, s = o / n, h = (o * t - a * e) / n, g = (o * e + a * t) / n;
  function d(p, m) {
    return p *= r, m *= i, [c * p - f * m + e, t - f * p - c * m];
  }
  return d.invert = function(p, m) {
    return [r * (l * p - s * m + h), i * (g - s * p - l * m)];
  }, d;
}
function An(n) {
  return xo(function() {
    return n;
  })();
}
function xo(n) {
  var e, t = 150, r = 480, i = 250, u = 0, a = 0, o = 0, c = 0, f = 0, l, s = 0, h = 1, g = 1, d = null, p = Lu, m = null, M, x, b, y = gt, T = 0.5, v, C, U, k, I;
  function $(w) {
    return U(w[0] * G, w[1] * G);
  }
  function X(w) {
    return w = U.invert(w[0], w[1]), w && [w[0] * tn, w[1] * tn];
  }
  $.stream = function(w) {
    return k && I === w ? k : k = vl(wl(l)(p(v(y(I = w)))));
  }, $.preclip = function(w) {
    return arguments.length ? (p = w, d = void 0, Y()) : p;
  }, $.postclip = function(w) {
    return arguments.length ? (y = w, m = M = x = b = null, Y()) : y;
  }, $.clipAngle = function(w) {
    return arguments.length ? (p = +w ? il(d = w * G) : (d = null, Lu), Y()) : d * tn;
  }, $.clipExtent = function(w) {
    return arguments.length ? (y = w == null ? (m = M = x = b = null, gt) : fo(m = +w[0][0], M = +w[0][1], x = +w[1][0], b = +w[1][1]), Y()) : m == null ? null : [[m, M], [x, b]];
  }, $.scale = function(w) {
    return arguments.length ? (t = +w, F()) : t;
  }, $.translate = function(w) {
    return arguments.length ? (r = +w[0], i = +w[1], F()) : [r, i];
  }, $.center = function(w) {
    return arguments.length ? (u = w[0] % 360 * G, a = w[1] % 360 * G, F()) : [u * tn, a * tn];
  }, $.rotate = function(w) {
    return arguments.length ? (o = w[0] % 360 * G, c = w[1] % 360 * G, f = w.length > 2 ? w[2] % 360 * G : 0, F()) : [o * tn, c * tn, f * tn];
  }, $.angle = function(w) {
    return arguments.length ? (s = w % 360 * G, F()) : s * tn;
  }, $.reflectX = function(w) {
    return arguments.length ? (h = w ? -1 : 1, F()) : h < 0;
  }, $.reflectY = function(w) {
    return arguments.length ? (g = w ? -1 : 1, F()) : g < 0;
  }, $.precision = function(w) {
    return arguments.length ? (v = Zu(C, T = w * w), Y()) : cn(T);
  }, $.fitExtent = function(w, D) {
    return br($, w, D);
  }, $.fitSize = function(w, D) {
    return Yi($, w, D);
  }, $.fitWidth = function(w, D) {
    return Ri($, w, D);
  }, $.fitHeight = function(w, D) {
    return qi($, w, D);
  };
  function F() {
    var w = Qu(t, 0, 0, h, g, s).apply(null, e(u, a)), D = Qu(t, r - w[0], i - w[1], h, g, s);
    return l = io(o, c, f), C = ti(e, D), U = ti(l, C), v = Zu(C, T), Y();
  }
  function Y() {
    return k = I = null, $;
  }
  return function() {
    return e = n.apply(this, arguments), $.invert = e.invert && X, F();
  };
}
function Pi(n) {
  var e = 0, t = q / 3, r = xo(n), i = r(e, t);
  return i.parallels = function(u) {
    return arguments.length ? r(e = u[0] * G, t = u[1] * G) : [e * tn, t * tn];
  }, i;
}
function Tl(n) {
  var e = R(n);
  function t(r, i) {
    return [r * e, E(i) / e];
  }
  return t.invert = function(r, i) {
    return [r / e, yn(i * e)];
  }, t;
}
function Sl(n, e) {
  var t = E(n), r = (t + E(e)) / 2;
  if (O(r) < A) return Tl(n);
  var i = 1 + t * (2 * r - t), u = cn(i) / r;
  function a(o, c) {
    var f = cn(i - 2 * r * E(c)) / r;
    return [f * E(o *= r), u - f * R(o)];
  }
  return a.invert = function(o, c) {
    var f = u - c, l = On(o, O(f)) * pn(f);
    return f * r < 0 && (l -= q * pn(o) * pn(f)), [l / r, yn((i - (o * o + f * f) * r * r) / (2 * r))];
  }, a;
}
function er() {
  return Pi(Sl).scale(155.424).center([0, 33.6442]);
}
function To() {
  return er().parallels([29.5, 45.5]).scale(1070).translate([480, 250]).rotate([96, 0]).center([-0.6, 38.7]);
}
function $l(n) {
  var e = n.length;
  return {
    point: function(t, r) {
      for (var i = -1; ++i < e; ) n[i].point(t, r);
    },
    sphere: function() {
      for (var t = -1; ++t < e; ) n[t].sphere();
    },
    lineStart: function() {
      for (var t = -1; ++t < e; ) n[t].lineStart();
    },
    lineEnd: function() {
      for (var t = -1; ++t < e; ) n[t].lineEnd();
    },
    polygonStart: function() {
      for (var t = -1; ++t < e; ) n[t].polygonStart();
    },
    polygonEnd: function() {
      for (var t = -1; ++t < e; ) n[t].polygonEnd();
    }
  };
}
function Cl() {
  var n, e, t = To(), r, i = er().rotate([154, 0]).center([-2, 58.5]).parallels([55, 65]), u, a = er().rotate([157, 0]).center([-3, 19.9]).parallels([8, 18]), o, c, f = { point: function(h, g) {
    c = [h, g];
  } };
  function l(h) {
    var g = h[0], d = h[1];
    return c = null, r.point(g, d), c || (u.point(g, d), c) || (o.point(g, d), c);
  }
  l.invert = function(h) {
    var g = t.scale(), d = t.translate(), p = (h[0] - d[0]) / g, m = (h[1] - d[1]) / g;
    return (m >= 0.12 && m < 0.234 && p >= -0.425 && p < -0.214 ? i : m >= 0.166 && m < 0.234 && p >= -0.214 && p < -0.115 ? a : t).invert(h);
  }, l.stream = function(h) {
    return n && e === h ? n : n = $l([t.stream(e = h), i.stream(h), a.stream(h)]);
  }, l.precision = function(h) {
    return arguments.length ? (t.precision(h), i.precision(h), a.precision(h), s()) : t.precision();
  }, l.scale = function(h) {
    return arguments.length ? (t.scale(h), i.scale(h * 0.35), a.scale(h), l.translate(t.translate())) : t.scale();
  }, l.translate = function(h) {
    if (!arguments.length) return t.translate();
    var g = t.scale(), d = +h[0], p = +h[1];
    return r = t.translate(h).clipExtent([[d - 0.455 * g, p - 0.238 * g], [d + 0.455 * g, p + 0.238 * g]]).stream(f), u = i.translate([d - 0.307 * g, p + 0.201 * g]).clipExtent([[d - 0.425 * g + A, p + 0.12 * g + A], [d - 0.214 * g - A, p + 0.234 * g - A]]).stream(f), o = a.translate([d - 0.205 * g, p + 0.212 * g]).clipExtent([[d - 0.214 * g + A, p + 0.166 * g + A], [d - 0.115 * g - A, p + 0.234 * g - A]]).stream(f), s();
  }, l.fitExtent = function(h, g) {
    return br(l, h, g);
  }, l.fitSize = function(h, g) {
    return Yi(l, h, g);
  }, l.fitWidth = function(h, g) {
    return Ri(l, h, g);
  }, l.fitHeight = function(h, g) {
    return qi(l, h, g);
  };
  function s() {
    return n = e = null, l;
  }
  return l.scale(1070);
}
function So(n) {
  return function(e, t) {
    var r = R(e), i = R(t), u = n(r * i);
    return u === 1 / 0 ? [2, 0] : [
      u * i * E(e),
      u * E(t)
    ];
  };
}
function Nt(n) {
  return function(e, t) {
    var r = cn(e * e + t * t), i = n(r), u = E(i), a = R(i);
    return [
      On(e * u, r * a),
      yn(r && t * u / r)
    ];
  };
}
var $o = So(function(n) {
  return cn(2 / (1 + n));
});
$o.invert = Nt(function(n) {
  return 2 * yn(n / 2);
});
function Nl() {
  return An($o).scale(124.75).clipAngle(180 - 1e-3);
}
var Co = So(function(n) {
  return (n = ro(n)) && n / E(n);
});
Co.invert = Nt(function(n) {
  return n;
});
function Dl() {
  return An(Co).scale(79.4188).clipAngle(180 - 1e-3);
}
function yr(n, e) {
  return [n, jt(Ai((Z + e) / 2))];
}
yr.invert = function(n, e) {
  return [n, 2 * Pe(to(e)) - Z];
};
function Ul() {
  return No(yr).scale(961 / gn);
}
function No(n) {
  var e = An(n), t = e.center, r = e.scale, i = e.translate, u = e.clipExtent, a = null, o, c, f;
  e.scale = function(s) {
    return arguments.length ? (r(s), l()) : r();
  }, e.translate = function(s) {
    return arguments.length ? (i(s), l()) : i();
  }, e.center = function(s) {
    return arguments.length ? (t(s), l()) : t();
  }, e.clipExtent = function(s) {
    return arguments.length ? (s == null ? a = o = c = f = null : (a = +s[0][0], o = +s[0][1], c = +s[1][0], f = +s[1][1]), l()) : a == null ? null : [[a, o], [c, f]];
  };
  function l() {
    var s = q * r(), h = e(Vc(e.rotate()).invert([0, 0]));
    return u(a == null ? [[h[0] - s, h[1] - s], [h[0] + s, h[1] + s]] : n === yr ? [[Math.max(h[0] - s, a), o], [Math.min(h[0] + s, c), f]] : [[a, Math.max(h[1] - s, o)], [c, Math.min(h[1] + s, f)]]);
  }
  return l();
}
function It(n) {
  return Ai((Z + n) / 2);
}
function El(n, e) {
  var t = R(n), r = n === e ? E(n) : jt(t / R(e)) / jt(It(e) / It(n)), i = t * Er(It(n), r) / r;
  if (!r) return yr;
  function u(a, o) {
    i > 0 ? o < -Z + A && (o = -Z + A) : o > Z - A && (o = Z - A);
    var c = i / Er(It(o), r);
    return [c * E(r * a), i - c * R(r * a)];
  }
  return u.invert = function(a, o) {
    var c = i - o, f = pn(r) * cn(a * a + c * c), l = On(a, O(c)) * pn(c);
    return c * r < 0 && (l -= q * pn(a) * pn(c)), [l / r, 2 * Pe(Er(i / f, 1 / r)) - Z];
  }, u;
}
function Fl() {
  return Pi(El).scale(109.5).parallels([30, 30]);
}
function tr(n, e) {
  return [n, e];
}
tr.invert = tr;
function Al() {
  return An(tr).scale(152.63);
}
function kl(n, e) {
  var t = R(n), r = n === e ? E(n) : (t - R(e)) / (e - n), i = t / r + n;
  if (O(r) < A) return tr;
  function u(a, o) {
    var c = i - o, f = r * a;
    return [c * E(f), i - c * R(f)];
  }
  return u.invert = function(a, o) {
    var c = i - o, f = On(a, O(c)) * pn(c);
    return c * r < 0 && (f -= q * pn(a) * pn(c)), [f / r, i - pn(r) * cn(a * a + c * c)];
  }, u;
}
function Yl() {
  return Pi(kl).scale(131.154).center([0, 13.9389]);
}
var at = 1.340264, ot = -0.081106, ft = 893e-6, ct = 3796e-6, rr = cn(3) / 2, Rl = 12;
function Do(n, e) {
  var t = yn(rr * E(e)), r = t * t, i = r * r * r;
  return [
    n * R(t) / (rr * (at + 3 * ot * r + i * (7 * ft + 9 * ct * r))),
    t * (at + ot * r + i * (ft + ct * r))
  ];
}
Do.invert = function(n, e) {
  for (var t = e, r = t * t, i = r * r * r, u = 0, a, o, c; u < Rl && (o = t * (at + ot * r + i * (ft + ct * r)) - e, c = at + 3 * ot * r + i * (7 * ft + 9 * ct * r), t -= a = o / c, r = t * t, i = r * r * r, !(O(a) < eo)); ++u)
    ;
  return [
    rr * n * (at + 3 * ot * r + i * (7 * ft + 9 * ct * r)) / R(t),
    yn(E(t) / rr)
  ];
};
function ql() {
  return An(Do).scale(177.158);
}
function Uo(n, e) {
  var t = R(e), r = R(n) * t;
  return [t * E(n) / r, E(e) / r];
}
Uo.invert = Nt(Pe);
function Pl() {
  return An(Uo).scale(144.049).clipAngle(60);
}
function Il() {
  var n = 1, e = 0, t = 0, r = 1, i = 1, u = 0, a, o, c = null, f, l, s, h = 1, g = 1, d = mr({
    point: function(y, T) {
      var v = b([y, T]);
      this.stream.point(v[0], v[1]);
    }
  }), p = gt, m, M;
  function x() {
    return h = n * r, g = n * i, m = M = null, b;
  }
  function b(y) {
    var T = y[0] * h, v = y[1] * g;
    if (u) {
      var C = v * a - T * o;
      T = T * a + v * o, v = C;
    }
    return [T + e, v + t];
  }
  return b.invert = function(y) {
    var T = y[0] - e, v = y[1] - t;
    if (u) {
      var C = v * a + T * o;
      T = T * a - v * o, v = C;
    }
    return [T / h, v / g];
  }, b.stream = function(y) {
    return m && M === y ? m : m = d(p(M = y));
  }, b.postclip = function(y) {
    return arguments.length ? (p = y, c = f = l = s = null, x()) : p;
  }, b.clipExtent = function(y) {
    return arguments.length ? (p = y == null ? (c = f = l = s = null, gt) : fo(c = +y[0][0], f = +y[0][1], l = +y[1][0], s = +y[1][1]), x()) : c == null ? null : [[c, f], [l, s]];
  }, b.scale = function(y) {
    return arguments.length ? (n = +y, x()) : n;
  }, b.translate = function(y) {
    return arguments.length ? (e = +y[0], t = +y[1], x()) : [e, t];
  }, b.angle = function(y) {
    return arguments.length ? (u = y % 360 * G, o = E(u), a = R(u), x()) : u * tn;
  }, b.reflectX = function(y) {
    return arguments.length ? (r = y ? -1 : 1, x()) : r < 0;
  }, b.reflectY = function(y) {
    return arguments.length ? (i = y ? -1 : 1, x()) : i < 0;
  }, b.fitExtent = function(y, T) {
    return br(b, y, T);
  }, b.fitSize = function(y, T) {
    return Yi(b, y, T);
  }, b.fitWidth = function(y, T) {
    return Ri(b, y, T);
  }, b.fitHeight = function(y, T) {
    return qi(b, y, T);
  }, b;
}
function Eo(n, e) {
  var t = e * e, r = t * t;
  return [
    n * (0.8707 - 0.131979 * t + r * (-0.013791 + r * (3971e-6 * t - 1529e-6 * r))),
    e * (1.007226 + t * (0.015085 + r * (-0.044475 + 0.028874 * t - 5916e-6 * r)))
  ];
}
Eo.invert = function(n, e) {
  var t = e, r = 25, i;
  do {
    var u = t * t, a = u * u;
    t -= i = (t * (1.007226 + u * (0.015085 + a * (-0.044475 + 0.028874 * u - 5916e-6 * a))) - e) / (1.007226 + u * (0.015085 * 3 + a * (-0.044475 * 7 + 0.028874 * 9 * u - 5916e-6 * 11 * a)));
  } while (O(i) > A && --r > 0);
  return [
    n / (0.8707 + (u = t * t) * (-0.131979 + u * (-0.013791 + u * u * u * (3971e-6 - 1529e-6 * u)))),
    t
  ];
};
function Hl() {
  return An(Eo).scale(175.295);
}
function Fo(n, e) {
  return [R(e) * E(n), E(e)];
}
Fo.invert = Nt(yn);
function Ll() {
  return An(Fo).scale(249.5).clipAngle(90 + A);
}
function Ao(n, e) {
  var t = R(e), r = 1 + R(n) * t;
  return [t * E(n) / r, E(e) / r];
}
Ao.invert = Nt(function(n) {
  return 2 * Pe(n);
});
function Ol() {
  return An(Ao).scale(250).clipAngle(142);
}
function ko(n, e) {
  return [jt(Ai((Z + e) / 2)), -n];
}
ko.invert = function(n, e) {
  return [-e, 2 * Pe(to(n)) - Z];
};
function zl() {
  var n = No(ko), e = n.center, t = n.rotate;
  return n.center = function(r) {
    return arguments.length ? e([-r[1], r[0]]) : (r = e(), [r[1], -r[0]]);
  }, n.rotate = function(r) {
    return arguments.length ? t([r[0], r[1], r.length > 2 ? r[2] + 90 : 90]) : (r = t(), [r[0], r[1], r[2] - 90]);
  }, t([0, 0, 90]).scale(159.155);
}
var Wl = Math.abs, gi = Math.cos, ir = Math.sin, Xl = 1e-6, Yo = Math.PI, di = Yo / 2, Vu = Bl(2);
function Ju(n) {
  return n > 1 ? di : n < -1 ? -di : Math.asin(n);
}
function Bl(n) {
  return n > 0 ? Math.sqrt(n) : 0;
}
function jl(n, e) {
  var t = n * ir(e), r = 30, i;
  do
    e -= i = (e + ir(e) - t) / (1 + gi(e));
  while (Wl(i) > Xl && --r > 0);
  return e / 2;
}
function Gl(n, e, t) {
  function r(i, u) {
    return [n * i * gi(u = jl(t, u)), e * ir(u)];
  }
  return r.invert = function(i, u) {
    return u = Ju(u / e), [i / (n * gi(u)), Ju((2 * u + ir(2 * u)) / t)];
  }, r;
}
var Zl = Gl(Vu / di, Vu, Yo);
function Ql() {
  return An(Zl).scale(169.529);
}
function Ie(n, e, t) {
  return n.fields = e || [], n.fname = t, n;
}
function Vl(n) {
  return n.length === 1 ? Jl(n[0]) : _l(n);
}
const Jl = (n) => function(e) {
  return e[n];
}, _l = (n) => {
  const e = n.length;
  return function(t) {
    for (let r = 0; r < e; ++r)
      t = t[n[r]];
    return t;
  };
};
function Xt(n) {
  throw Error(n);
}
function Kl(n) {
  const e = [], t = n.length;
  let r = null, i = 0, u = "", a, o, c;
  n = n + "";
  function f() {
    e.push(u + n.substring(a, o)), u = "", a = o + 1;
  }
  for (a = o = 0; o < t; ++o)
    if (c = n[o], c === "\\")
      u += n.substring(a, o++), a = o;
    else if (c === r)
      f(), r = null, i = -1;
    else {
      if (r)
        continue;
      a === i && c === '"' || a === i && c === "'" ? (a = o + 1, r = c) : c === "." && !i ? o > a ? f() : a = o + 1 : c === "[" ? (o > a && f(), i = a = o + 1) : c === "]" && (i || Xt("Access path missing open bracket: " + n), i > 0 && f(), i = 0, a = o + 1);
    }
  return i && Xt("Access path missing closing bracket: " + n), r && Xt("Access path missing closing quote: " + n), o > a && (o++, f()), e;
}
function n0(n, e, t) {
  const r = Kl(n);
  return n = r.length === 1 ? r[0] : n, Ie(Vl(r), [n], n);
}
n0("id");
Ie((n) => n, [], "identity");
Ie(() => 0, [], "zero");
Ie(() => 1, [], "one");
Ie(() => !0, [], "true");
Ie(() => !1, [], "false");
var Ii = Array.isArray;
function e0(n) {
  return n === Object(n);
}
function Vn(n) {
  return n[n.length - 1];
}
function t0(n) {
  return n == null || n === "" ? null : +n;
}
function r0(n) {
  return n != null ? Ii(n) ? n : [n] : [];
}
function i0(n) {
  return typeof n == "function";
}
function u0(n) {
  return i0(n) ? n : () => n;
}
function a0(n) {
  return typeof n == "number";
}
function Ro(n) {
  return typeof n == "string";
}
function o0(n) {
  return n && Vn(n) - n[0] || 0;
}
function f0(n) {
  const e = {}, t = n.length;
  for (let r = 0; r < t; ++r) e[n[r]] = !0;
  return e;
}
function kn(n, e) {
  switch (arguments.length) {
    case 0:
      break;
    case 1:
      this.range(n);
      break;
    default:
      this.range(e).domain(n);
      break;
  }
  return this;
}
function Kn(n, e) {
  switch (arguments.length) {
    case 0:
      break;
    case 1: {
      typeof n == "function" ? this.interpolator(n) : this.range(n);
      break;
    }
    default: {
      this.domain(n), typeof e == "function" ? this.interpolator(e) : this.range(e);
      break;
    }
  }
  return this;
}
const _u = Symbol("implicit");
function Hi() {
  var n = new Cu(), e = [], t = [], r = _u;
  function i(u) {
    let a = n.get(u);
    if (a === void 0) {
      if (r !== _u) return r;
      n.set(u, a = e.push(u) - 1);
    }
    return t[a % t.length];
  }
  return i.domain = function(u) {
    if (!arguments.length) return e.slice();
    e = [], n = new Cu();
    for (const a of u)
      n.has(a) || n.set(a, e.push(a) - 1);
    return i;
  }, i.range = function(u) {
    return arguments.length ? (t = Array.from(u), i) : t.slice();
  }, i.unknown = function(u) {
    return arguments.length ? (r = u, i) : r;
  }, i.copy = function() {
    return Hi(e, t).unknown(r);
  }, kn.apply(i, arguments), i;
}
function He(n, e, t) {
  n.prototype = e.prototype = t, t.constructor = n;
}
function Dt(n, e) {
  var t = Object.create(n.prototype);
  for (var r in e) t[r] = e[r];
  return t;
}
function ne() {
}
var he = 0.7, Ue = 1 / he, Se = "\\s*([+-]?\\d+)\\s*", mt = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)\\s*", Dn = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)%\\s*", c0 = /^#([0-9a-f]{3,8})$/, l0 = new RegExp(`^rgb\\(${Se},${Se},${Se}\\)$`), s0 = new RegExp(`^rgb\\(${Dn},${Dn},${Dn}\\)$`), h0 = new RegExp(`^rgba\\(${Se},${Se},${Se},${mt}\\)$`), g0 = new RegExp(`^rgba\\(${Dn},${Dn},${Dn},${mt}\\)$`), d0 = new RegExp(`^hsl\\(${mt},${Dn},${Dn}\\)$`), p0 = new RegExp(`^hsla\\(${mt},${Dn},${Dn},${mt}\\)$`), Ku = {
  aliceblue: 15792383,
  antiquewhite: 16444375,
  aqua: 65535,
  aquamarine: 8388564,
  azure: 15794175,
  beige: 16119260,
  bisque: 16770244,
  black: 0,
  blanchedalmond: 16772045,
  blue: 255,
  blueviolet: 9055202,
  brown: 10824234,
  burlywood: 14596231,
  cadetblue: 6266528,
  chartreuse: 8388352,
  chocolate: 13789470,
  coral: 16744272,
  cornflowerblue: 6591981,
  cornsilk: 16775388,
  crimson: 14423100,
  cyan: 65535,
  darkblue: 139,
  darkcyan: 35723,
  darkgoldenrod: 12092939,
  darkgray: 11119017,
  darkgreen: 25600,
  darkgrey: 11119017,
  darkkhaki: 12433259,
  darkmagenta: 9109643,
  darkolivegreen: 5597999,
  darkorange: 16747520,
  darkorchid: 10040012,
  darkred: 9109504,
  darksalmon: 15308410,
  darkseagreen: 9419919,
  darkslateblue: 4734347,
  darkslategray: 3100495,
  darkslategrey: 3100495,
  darkturquoise: 52945,
  darkviolet: 9699539,
  deeppink: 16716947,
  deepskyblue: 49151,
  dimgray: 6908265,
  dimgrey: 6908265,
  dodgerblue: 2003199,
  firebrick: 11674146,
  floralwhite: 16775920,
  forestgreen: 2263842,
  fuchsia: 16711935,
  gainsboro: 14474460,
  ghostwhite: 16316671,
  gold: 16766720,
  goldenrod: 14329120,
  gray: 8421504,
  green: 32768,
  greenyellow: 11403055,
  grey: 8421504,
  honeydew: 15794160,
  hotpink: 16738740,
  indianred: 13458524,
  indigo: 4915330,
  ivory: 16777200,
  khaki: 15787660,
  lavender: 15132410,
  lavenderblush: 16773365,
  lawngreen: 8190976,
  lemonchiffon: 16775885,
  lightblue: 11393254,
  lightcoral: 15761536,
  lightcyan: 14745599,
  lightgoldenrodyellow: 16448210,
  lightgray: 13882323,
  lightgreen: 9498256,
  lightgrey: 13882323,
  lightpink: 16758465,
  lightsalmon: 16752762,
  lightseagreen: 2142890,
  lightskyblue: 8900346,
  lightslategray: 7833753,
  lightslategrey: 7833753,
  lightsteelblue: 11584734,
  lightyellow: 16777184,
  lime: 65280,
  limegreen: 3329330,
  linen: 16445670,
  magenta: 16711935,
  maroon: 8388608,
  mediumaquamarine: 6737322,
  mediumblue: 205,
  mediumorchid: 12211667,
  mediumpurple: 9662683,
  mediumseagreen: 3978097,
  mediumslateblue: 8087790,
  mediumspringgreen: 64154,
  mediumturquoise: 4772300,
  mediumvioletred: 13047173,
  midnightblue: 1644912,
  mintcream: 16121850,
  mistyrose: 16770273,
  moccasin: 16770229,
  navajowhite: 16768685,
  navy: 128,
  oldlace: 16643558,
  olive: 8421376,
  olivedrab: 7048739,
  orange: 16753920,
  orangered: 16729344,
  orchid: 14315734,
  palegoldenrod: 15657130,
  palegreen: 10025880,
  paleturquoise: 11529966,
  palevioletred: 14381203,
  papayawhip: 16773077,
  peachpuff: 16767673,
  peru: 13468991,
  pink: 16761035,
  plum: 14524637,
  powderblue: 11591910,
  purple: 8388736,
  rebeccapurple: 6697881,
  red: 16711680,
  rosybrown: 12357519,
  royalblue: 4286945,
  saddlebrown: 9127187,
  salmon: 16416882,
  sandybrown: 16032864,
  seagreen: 3050327,
  seashell: 16774638,
  sienna: 10506797,
  silver: 12632256,
  skyblue: 8900331,
  slateblue: 6970061,
  slategray: 7372944,
  slategrey: 7372944,
  snow: 16775930,
  springgreen: 65407,
  steelblue: 4620980,
  tan: 13808780,
  teal: 32896,
  thistle: 14204888,
  tomato: 16737095,
  turquoise: 4251856,
  violet: 15631086,
  wheat: 16113331,
  white: 16777215,
  whitesmoke: 16119285,
  yellow: 16776960,
  yellowgreen: 10145074
};
He(ne, bt, {
  copy(n) {
    return Object.assign(new this.constructor(), this, n);
  },
  displayable() {
    return this.rgb().displayable();
  },
  hex: na,
  // Deprecated! Use color.formatHex.
  formatHex: na,
  formatHex8: m0,
  formatHsl: b0,
  formatRgb: ea,
  toString: ea
});
function na() {
  return this.rgb().formatHex();
}
function m0() {
  return this.rgb().formatHex8();
}
function b0() {
  return qo(this).formatHsl();
}
function ea() {
  return this.rgb().formatRgb();
}
function bt(n) {
  var e, t;
  return n = (n + "").trim().toLowerCase(), (e = c0.exec(n)) ? (t = e[1].length, e = parseInt(e[1], 16), t === 6 ? ta(e) : t === 3 ? new K(e >> 8 & 15 | e >> 4 & 240, e >> 4 & 15 | e & 240, (e & 15) << 4 | e & 15, 1) : t === 8 ? Ht(e >> 24 & 255, e >> 16 & 255, e >> 8 & 255, (e & 255) / 255) : t === 4 ? Ht(e >> 12 & 15 | e >> 8 & 240, e >> 8 & 15 | e >> 4 & 240, e >> 4 & 15 | e & 240, ((e & 15) << 4 | e & 15) / 255) : null) : (e = l0.exec(n)) ? new K(e[1], e[2], e[3], 1) : (e = s0.exec(n)) ? new K(e[1] * 255 / 100, e[2] * 255 / 100, e[3] * 255 / 100, 1) : (e = h0.exec(n)) ? Ht(e[1], e[2], e[3], e[4]) : (e = g0.exec(n)) ? Ht(e[1] * 255 / 100, e[2] * 255 / 100, e[3] * 255 / 100, e[4]) : (e = d0.exec(n)) ? ua(e[1], e[2] / 100, e[3] / 100, 1) : (e = p0.exec(n)) ? ua(e[1], e[2] / 100, e[3] / 100, e[4]) : Ku.hasOwnProperty(n) ? ta(Ku[n]) : n === "transparent" ? new K(NaN, NaN, NaN, 0) : null;
}
function ta(n) {
  return new K(n >> 16 & 255, n >> 8 & 255, n & 255, 1);
}
function Ht(n, e, t, r) {
  return r <= 0 && (n = e = t = NaN), new K(n, e, t, r);
}
function Li(n) {
  return n instanceof ne || (n = bt(n)), n ? (n = n.rgb(), new K(n.r, n.g, n.b, n.opacity)) : new K();
}
function ur(n, e, t, r) {
  return arguments.length === 1 ? Li(n) : new K(n, e, t, r ?? 1);
}
function K(n, e, t, r) {
  this.r = +n, this.g = +e, this.b = +t, this.opacity = +r;
}
He(K, ur, Dt(ne, {
  brighter(n) {
    return n = n == null ? Ue : Math.pow(Ue, n), new K(this.r * n, this.g * n, this.b * n, this.opacity);
  },
  darker(n) {
    return n = n == null ? he : Math.pow(he, n), new K(this.r * n, this.g * n, this.b * n, this.opacity);
  },
  rgb() {
    return this;
  },
  clamp() {
    return new K(oe(this.r), oe(this.g), oe(this.b), ar(this.opacity));
  },
  displayable() {
    return -0.5 <= this.r && this.r < 255.5 && -0.5 <= this.g && this.g < 255.5 && -0.5 <= this.b && this.b < 255.5 && 0 <= this.opacity && this.opacity <= 1;
  },
  hex: ra,
  // Deprecated! Use color.formatHex.
  formatHex: ra,
  formatHex8: y0,
  formatRgb: ia,
  toString: ia
}));
function ra() {
  return `#${ue(this.r)}${ue(this.g)}${ue(this.b)}`;
}
function y0() {
  return `#${ue(this.r)}${ue(this.g)}${ue(this.b)}${ue((isNaN(this.opacity) ? 1 : this.opacity) * 255)}`;
}
function ia() {
  const n = ar(this.opacity);
  return `${n === 1 ? "rgb(" : "rgba("}${oe(this.r)}, ${oe(this.g)}, ${oe(this.b)}${n === 1 ? ")" : `, ${n})`}`;
}
function ar(n) {
  return isNaN(n) ? 1 : Math.max(0, Math.min(1, n));
}
function oe(n) {
  return Math.max(0, Math.min(255, Math.round(n) || 0));
}
function ue(n) {
  return n = oe(n), (n < 16 ? "0" : "") + n.toString(16);
}
function ua(n, e, t, r) {
  return r <= 0 ? n = e = t = NaN : t <= 0 || t >= 1 ? n = e = NaN : e <= 0 && (n = NaN), new Tn(n, e, t, r);
}
function qo(n) {
  if (n instanceof Tn) return new Tn(n.h, n.s, n.l, n.opacity);
  if (n instanceof ne || (n = bt(n)), !n) return new Tn();
  if (n instanceof Tn) return n;
  n = n.rgb();
  var e = n.r / 255, t = n.g / 255, r = n.b / 255, i = Math.min(e, t, r), u = Math.max(e, t, r), a = NaN, o = u - i, c = (u + i) / 2;
  return o ? (e === u ? a = (t - r) / o + (t < r) * 6 : t === u ? a = (r - e) / o + 2 : a = (e - t) / o + 4, o /= c < 0.5 ? u + i : 2 - u - i, a *= 60) : o = c > 0 && c < 1 ? 0 : a, new Tn(a, o, c, n.opacity);
}
function pi(n, e, t, r) {
  return arguments.length === 1 ? qo(n) : new Tn(n, e, t, r ?? 1);
}
function Tn(n, e, t, r) {
  this.h = +n, this.s = +e, this.l = +t, this.opacity = +r;
}
He(Tn, pi, Dt(ne, {
  brighter(n) {
    return n = n == null ? Ue : Math.pow(Ue, n), new Tn(this.h, this.s, this.l * n, this.opacity);
  },
  darker(n) {
    return n = n == null ? he : Math.pow(he, n), new Tn(this.h, this.s, this.l * n, this.opacity);
  },
  rgb() {
    var n = this.h % 360 + (this.h < 0) * 360, e = isNaN(n) || isNaN(this.s) ? 0 : this.s, t = this.l, r = t + (t < 0.5 ? t : 1 - t) * e, i = 2 * t - r;
    return new K(
      Rr(n >= 240 ? n - 240 : n + 120, i, r),
      Rr(n, i, r),
      Rr(n < 120 ? n + 240 : n - 120, i, r),
      this.opacity
    );
  },
  clamp() {
    return new Tn(aa(this.h), Lt(this.s), Lt(this.l), ar(this.opacity));
  },
  displayable() {
    return (0 <= this.s && this.s <= 1 || isNaN(this.s)) && 0 <= this.l && this.l <= 1 && 0 <= this.opacity && this.opacity <= 1;
  },
  formatHsl() {
    const n = ar(this.opacity);
    return `${n === 1 ? "hsl(" : "hsla("}${aa(this.h)}, ${Lt(this.s) * 100}%, ${Lt(this.l) * 100}%${n === 1 ? ")" : `, ${n})`}`;
  }
}));
function aa(n) {
  return n = (n || 0) % 360, n < 0 ? n + 360 : n;
}
function Lt(n) {
  return Math.max(0, Math.min(1, n || 0));
}
function Rr(n, e, t) {
  return (n < 60 ? e + (t - e) * n / 60 : n < 180 ? t : n < 240 ? e + (t - e) * (240 - n) / 60 : e) * 255;
}
const Po = Math.PI / 180, Io = 180 / Math.PI, or = 18, Ho = 0.96422, Lo = 1, Oo = 0.82521, zo = 4 / 29, $e = 6 / 29, Wo = 3 * $e * $e, M0 = $e * $e * $e;
function Xo(n) {
  if (n instanceof Un) return new Un(n.l, n.a, n.b, n.opacity);
  if (n instanceof Pn) return Bo(n);
  n instanceof K || (n = Li(n));
  var e = Hr(n.r), t = Hr(n.g), r = Hr(n.b), i = qr((0.2225045 * e + 0.7168786 * t + 0.0606169 * r) / Lo), u, a;
  return e === t && t === r ? u = a = i : (u = qr((0.4360747 * e + 0.3850649 * t + 0.1430804 * r) / Ho), a = qr((0.0139322 * e + 0.0971045 * t + 0.7141733 * r) / Oo)), new Un(116 * i - 16, 500 * (u - i), 200 * (i - a), n.opacity);
}
function mi(n, e, t, r) {
  return arguments.length === 1 ? Xo(n) : new Un(n, e, t, r ?? 1);
}
function Un(n, e, t, r) {
  this.l = +n, this.a = +e, this.b = +t, this.opacity = +r;
}
He(Un, mi, Dt(ne, {
  brighter(n) {
    return new Un(this.l + or * (n ?? 1), this.a, this.b, this.opacity);
  },
  darker(n) {
    return new Un(this.l - or * (n ?? 1), this.a, this.b, this.opacity);
  },
  rgb() {
    var n = (this.l + 16) / 116, e = isNaN(this.a) ? n : n + this.a / 500, t = isNaN(this.b) ? n : n - this.b / 200;
    return e = Ho * Pr(e), n = Lo * Pr(n), t = Oo * Pr(t), new K(
      Ir(3.1338561 * e - 1.6168667 * n - 0.4906146 * t),
      Ir(-0.9787684 * e + 1.9161415 * n + 0.033454 * t),
      Ir(0.0719453 * e - 0.2289914 * n + 1.4052427 * t),
      this.opacity
    );
  }
}));
function qr(n) {
  return n > M0 ? Math.pow(n, 1 / 3) : n / Wo + zo;
}
function Pr(n) {
  return n > $e ? n * n * n : Wo * (n - zo);
}
function Ir(n) {
  return 255 * (n <= 31308e-7 ? 12.92 * n : 1.055 * Math.pow(n, 1 / 2.4) - 0.055);
}
function Hr(n) {
  return (n /= 255) <= 0.04045 ? n / 12.92 : Math.pow((n + 0.055) / 1.055, 2.4);
}
function v0(n) {
  if (n instanceof Pn) return new Pn(n.h, n.c, n.l, n.opacity);
  if (n instanceof Un || (n = Xo(n)), n.a === 0 && n.b === 0) return new Pn(NaN, 0 < n.l && n.l < 100 ? 0 : NaN, n.l, n.opacity);
  var e = Math.atan2(n.b, n.a) * Io;
  return new Pn(e < 0 ? e + 360 : e, Math.sqrt(n.a * n.a + n.b * n.b), n.l, n.opacity);
}
function bi(n, e, t, r) {
  return arguments.length === 1 ? v0(n) : new Pn(n, e, t, r ?? 1);
}
function Pn(n, e, t, r) {
  this.h = +n, this.c = +e, this.l = +t, this.opacity = +r;
}
function Bo(n) {
  if (isNaN(n.h)) return new Un(n.l, 0, 0, n.opacity);
  var e = n.h * Po;
  return new Un(n.l, Math.cos(e) * n.c, Math.sin(e) * n.c, n.opacity);
}
He(Pn, bi, Dt(ne, {
  brighter(n) {
    return new Pn(this.h, this.c, this.l + or * (n ?? 1), this.opacity);
  },
  darker(n) {
    return new Pn(this.h, this.c, this.l - or * (n ?? 1), this.opacity);
  },
  rgb() {
    return Bo(this).rgb();
  }
}));
var jo = -0.14861, Oi = 1.78277, zi = -0.29227, Mr = -0.90649, yt = 1.97294, oa = yt * Mr, fa = yt * Oi, ca = Oi * zi - Mr * jo;
function w0(n) {
  if (n instanceof fe) return new fe(n.h, n.s, n.l, n.opacity);
  n instanceof K || (n = Li(n));
  var e = n.r / 255, t = n.g / 255, r = n.b / 255, i = (ca * r + oa * e - fa * t) / (ca + oa - fa), u = r - i, a = (yt * (t - i) - zi * u) / Mr, o = Math.sqrt(a * a + u * u) / (yt * i * (1 - i)), c = o ? Math.atan2(a, u) * Io - 120 : NaN;
  return new fe(c < 0 ? c + 360 : c, o, i, n.opacity);
}
function yi(n, e, t, r) {
  return arguments.length === 1 ? w0(n) : new fe(n, e, t, r ?? 1);
}
function fe(n, e, t, r) {
  this.h = +n, this.s = +e, this.l = +t, this.opacity = +r;
}
He(fe, yi, Dt(ne, {
  brighter(n) {
    return n = n == null ? Ue : Math.pow(Ue, n), new fe(this.h, this.s, this.l * n, this.opacity);
  },
  darker(n) {
    return n = n == null ? he : Math.pow(he, n), new fe(this.h, this.s, this.l * n, this.opacity);
  },
  rgb() {
    var n = isNaN(this.h) ? 0 : (this.h + 120) * Po, e = +this.l, t = isNaN(this.s) ? 0 : this.s * e * (1 - e), r = Math.cos(n), i = Math.sin(n);
    return new K(
      255 * (e + t * (jo * r + Oi * i)),
      255 * (e + t * (zi * r + Mr * i)),
      255 * (e + t * (yt * r)),
      this.opacity
    );
  }
}));
function Go(n, e, t, r, i) {
  var u = n * n, a = u * n;
  return ((1 - 3 * n + 3 * u - a) * e + (4 - 6 * u + 3 * a) * t + (1 + 3 * n + 3 * u - 3 * a) * r + a * i) / 6;
}
function Zo(n) {
  var e = n.length - 1;
  return function(t) {
    var r = t <= 0 ? t = 0 : t >= 1 ? (t = 1, e - 1) : Math.floor(t * e), i = n[r], u = n[r + 1], a = r > 0 ? n[r - 1] : 2 * i - u, o = r < e - 1 ? n[r + 2] : 2 * u - i;
    return Go((t - r / e) * e, a, i, u, o);
  };
}
function Qo(n) {
  var e = n.length;
  return function(t) {
    var r = Math.floor(((t %= 1) < 0 ? ++t : t) * e), i = n[(r + e - 1) % e], u = n[r % e], a = n[(r + 1) % e], o = n[(r + 2) % e];
    return Go((t - r / e) * e, i, u, a, o);
  };
}
const vr = (n) => () => n;
function Vo(n, e) {
  return function(t) {
    return n + t * e;
  };
}
function x0(n, e, t) {
  return n = Math.pow(n, t), e = Math.pow(e, t) - n, t = 1 / t, function(r) {
    return Math.pow(n + r * e, t);
  };
}
function wr(n, e) {
  var t = e - n;
  return t ? Vo(n, t > 180 || t < -180 ? t - 360 * Math.round(t / 360) : t) : vr(isNaN(n) ? e : n);
}
function T0(n) {
  return (n = +n) == 1 ? nn : function(e, t) {
    return t - e ? x0(e, t, n) : vr(isNaN(e) ? t : e);
  };
}
function nn(n, e) {
  var t = e - n;
  return t ? Vo(n, t) : vr(isNaN(n) ? e : n);
}
const Mi = function n(e) {
  var t = T0(e);
  function r(i, u) {
    var a = t((i = ur(i)).r, (u = ur(u)).r), o = t(i.g, u.g), c = t(i.b, u.b), f = nn(i.opacity, u.opacity);
    return function(l) {
      return i.r = a(l), i.g = o(l), i.b = c(l), i.opacity = f(l), i + "";
    };
  }
  return r.gamma = n, r;
}(1);
function Jo(n) {
  return function(e) {
    var t = e.length, r = new Array(t), i = new Array(t), u = new Array(t), a, o;
    for (a = 0; a < t; ++a)
      o = ur(e[a]), r[a] = o.r || 0, i[a] = o.g || 0, u[a] = o.b || 0;
    return r = n(r), i = n(i), u = n(u), o.opacity = 1, function(c) {
      return o.r = r(c), o.g = i(c), o.b = u(c), o + "";
    };
  };
}
var S0 = Jo(Zo), $0 = Jo(Qo);
function Wi(n, e) {
  e || (e = []);
  var t = n ? Math.min(e.length, n.length) : 0, r = e.slice(), i;
  return function(u) {
    for (i = 0; i < t; ++i) r[i] = n[i] * (1 - u) + e[i] * u;
    return r;
  };
}
function _o(n) {
  return ArrayBuffer.isView(n) && !(n instanceof DataView);
}
function C0(n, e) {
  return (_o(e) ? Wi : Ko)(n, e);
}
function Ko(n, e) {
  var t = e ? e.length : 0, r = n ? Math.min(t, n.length) : 0, i = new Array(r), u = new Array(t), a;
  for (a = 0; a < r; ++a) i[a] = ge(n[a], e[a]);
  for (; a < t; ++a) u[a] = e[a];
  return function(o) {
    for (a = 0; a < r; ++a) u[a] = i[a](o);
    return u;
  };
}
function nf(n, e) {
  var t = /* @__PURE__ */ new Date();
  return n = +n, e = +e, function(r) {
    return t.setTime(n * (1 - r) + e * r), t;
  };
}
function xn(n, e) {
  return n = +n, e = +e, function(t) {
    return n * (1 - t) + e * t;
  };
}
function ef(n, e) {
  var t = {}, r = {}, i;
  (n === null || typeof n != "object") && (n = {}), (e === null || typeof e != "object") && (e = {});
  for (i in e)
    i in n ? t[i] = ge(n[i], e[i]) : r[i] = e[i];
  return function(u) {
    for (i in t) r[i] = t[i](u);
    return r;
  };
}
var vi = /[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?/g, Lr = new RegExp(vi.source, "g");
function N0(n) {
  return function() {
    return n;
  };
}
function D0(n) {
  return function(e) {
    return n(e) + "";
  };
}
function tf(n, e) {
  var t = vi.lastIndex = Lr.lastIndex = 0, r, i, u, a = -1, o = [], c = [];
  for (n = n + "", e = e + ""; (r = vi.exec(n)) && (i = Lr.exec(e)); )
    (u = i.index) > t && (u = e.slice(t, u), o[a] ? o[a] += u : o[++a] = u), (r = r[0]) === (i = i[0]) ? o[a] ? o[a] += i : o[++a] = i : (o[++a] = null, c.push({ i: a, x: xn(r, i) })), t = Lr.lastIndex;
  return t < e.length && (u = e.slice(t), o[a] ? o[a] += u : o[++a] = u), o.length < 2 ? c[0] ? D0(c[0].x) : N0(e) : (e = c.length, function(f) {
    for (var l = 0, s; l < e; ++l) o[(s = c[l]).i] = s.x(f);
    return o.join("");
  });
}
function ge(n, e) {
  var t = typeof e, r;
  return e == null || t === "boolean" ? vr(e) : (t === "number" ? xn : t === "string" ? (r = bt(e)) ? (e = r, Mi) : tf : e instanceof bt ? Mi : e instanceof Date ? nf : _o(e) ? Wi : Array.isArray(e) ? Ko : typeof e.valueOf != "function" && typeof e.toString != "function" || isNaN(e) ? ef : xn)(n, e);
}
function U0(n) {
  var e = n.length;
  return function(t) {
    return n[Math.max(0, Math.min(e - 1, Math.floor(t * e)))];
  };
}
function E0(n, e) {
  var t = wr(+n, +e);
  return function(r) {
    var i = t(r);
    return i - 360 * Math.floor(i / 360);
  };
}
function xr(n, e) {
  return n = +n, e = +e, function(t) {
    return Math.round(n * (1 - t) + e * t);
  };
}
var la = 180 / Math.PI, wi = {
  translateX: 0,
  translateY: 0,
  rotate: 0,
  skewX: 0,
  scaleX: 1,
  scaleY: 1
};
function rf(n, e, t, r, i, u) {
  var a, o, c;
  return (a = Math.sqrt(n * n + e * e)) && (n /= a, e /= a), (c = n * t + e * r) && (t -= n * c, r -= e * c), (o = Math.sqrt(t * t + r * r)) && (t /= o, r /= o, c /= o), n * r < e * t && (n = -n, e = -e, c = -c, a = -a), {
    translateX: i,
    translateY: u,
    rotate: Math.atan2(e, n) * la,
    skewX: Math.atan(c) * la,
    scaleX: a,
    scaleY: o
  };
}
var Ot;
function F0(n) {
  const e = new (typeof DOMMatrix == "function" ? DOMMatrix : WebKitCSSMatrix)(n + "");
  return e.isIdentity ? wi : rf(e.a, e.b, e.c, e.d, e.e, e.f);
}
function A0(n) {
  return n == null || (Ot || (Ot = document.createElementNS("http://www.w3.org/2000/svg", "g")), Ot.setAttribute("transform", n), !(n = Ot.transform.baseVal.consolidate())) ? wi : (n = n.matrix, rf(n.a, n.b, n.c, n.d, n.e, n.f));
}
function uf(n, e, t, r) {
  function i(f) {
    return f.length ? f.pop() + " " : "";
  }
  function u(f, l, s, h, g, d) {
    if (f !== s || l !== h) {
      var p = g.push("translate(", null, e, null, t);
      d.push({ i: p - 4, x: xn(f, s) }, { i: p - 2, x: xn(l, h) });
    } else (s || h) && g.push("translate(" + s + e + h + t);
  }
  function a(f, l, s, h) {
    f !== l ? (f - l > 180 ? l += 360 : l - f > 180 && (f += 360), h.push({ i: s.push(i(s) + "rotate(", null, r) - 2, x: xn(f, l) })) : l && s.push(i(s) + "rotate(" + l + r);
  }
  function o(f, l, s, h) {
    f !== l ? h.push({ i: s.push(i(s) + "skewX(", null, r) - 2, x: xn(f, l) }) : l && s.push(i(s) + "skewX(" + l + r);
  }
  function c(f, l, s, h, g, d) {
    if (f !== s || l !== h) {
      var p = g.push(i(g) + "scale(", null, ",", null, ")");
      d.push({ i: p - 4, x: xn(f, s) }, { i: p - 2, x: xn(l, h) });
    } else (s !== 1 || h !== 1) && g.push(i(g) + "scale(" + s + "," + h + ")");
  }
  return function(f, l) {
    var s = [], h = [];
    return f = n(f), l = n(l), u(f.translateX, f.translateY, l.translateX, l.translateY, s, h), a(f.rotate, l.rotate, s, h), o(f.skewX, l.skewX, s, h), c(f.scaleX, f.scaleY, l.scaleX, l.scaleY, s, h), f = l = null, function(g) {
      for (var d = -1, p = h.length, m; ++d < p; ) s[(m = h[d]).i] = m.x(g);
      return s.join("");
    };
  };
}
var k0 = uf(F0, "px, ", "px)", "deg)"), Y0 = uf(A0, ", ", ")", ")"), R0 = 1e-12;
function sa(n) {
  return ((n = Math.exp(n)) + 1 / n) / 2;
}
function q0(n) {
  return ((n = Math.exp(n)) - 1 / n) / 2;
}
function P0(n) {
  return ((n = Math.exp(2 * n)) - 1) / (n + 1);
}
const I0 = function n(e, t, r) {
  function i(u, a) {
    var o = u[0], c = u[1], f = u[2], l = a[0], s = a[1], h = a[2], g = l - o, d = s - c, p = g * g + d * d, m, M;
    if (p < R0)
      M = Math.log(h / f) / e, m = function(C) {
        return [
          o + C * g,
          c + C * d,
          f * Math.exp(e * C * M)
        ];
      };
    else {
      var x = Math.sqrt(p), b = (h * h - f * f + r * p) / (2 * f * t * x), y = (h * h - f * f - r * p) / (2 * h * t * x), T = Math.log(Math.sqrt(b * b + 1) - b), v = Math.log(Math.sqrt(y * y + 1) - y);
      M = (v - T) / e, m = function(C) {
        var U = C * M, k = sa(T), I = f / (t * x) * (k * P0(e * U + T) - q0(T));
        return [
          o + I * g,
          c + I * d,
          f * k / sa(e * U + T)
        ];
      };
    }
    return m.duration = M * 1e3 * e / Math.SQRT2, m;
  }
  return i.rho = function(u) {
    var a = Math.max(1e-3, +u), o = a * a, c = o * o;
    return n(a, o, c);
  }, i;
}(Math.SQRT2, 2, 4);
function af(n) {
  return function(e, t) {
    var r = n((e = pi(e)).h, (t = pi(t)).h), i = nn(e.s, t.s), u = nn(e.l, t.l), a = nn(e.opacity, t.opacity);
    return function(o) {
      return e.h = r(o), e.s = i(o), e.l = u(o), e.opacity = a(o), e + "";
    };
  };
}
const H0 = af(wr);
var L0 = af(nn);
function O0(n, e) {
  var t = nn((n = mi(n)).l, (e = mi(e)).l), r = nn(n.a, e.a), i = nn(n.b, e.b), u = nn(n.opacity, e.opacity);
  return function(a) {
    return n.l = t(a), n.a = r(a), n.b = i(a), n.opacity = u(a), n + "";
  };
}
function of(n) {
  return function(e, t) {
    var r = n((e = bi(e)).h, (t = bi(t)).h), i = nn(e.c, t.c), u = nn(e.l, t.l), a = nn(e.opacity, t.opacity);
    return function(o) {
      return e.h = r(o), e.c = i(o), e.l = u(o), e.opacity = a(o), e + "";
    };
  };
}
const z0 = of(wr);
var W0 = of(nn);
function ff(n) {
  return function e(t) {
    t = +t;
    function r(i, u) {
      var a = n((i = yi(i)).h, (u = yi(u)).h), o = nn(i.s, u.s), c = nn(i.l, u.l), f = nn(i.opacity, u.opacity);
      return function(l) {
        return i.h = a(l), i.s = o(l), i.l = c(Math.pow(l, t)), i.opacity = f(l), i + "";
      };
    }
    return r.gamma = e, r;
  }(1);
}
const X0 = ff(wr);
var B0 = ff(nn);
function Xi(n, e) {
  e === void 0 && (e = n, n = ge);
  for (var t = 0, r = e.length - 1, i = e[0], u = new Array(r < 0 ? 0 : r); t < r; ) u[t] = n(i, i = e[++t]);
  return function(a) {
    var o = Math.max(0, Math.min(r - 1, Math.floor(a *= r)));
    return u[o](a - o);
  };
}
function j0(n, e) {
  for (var t = new Array(e), r = 0; r < e; ++r) t[r] = n(r / (e - 1));
  return t;
}
const G0 = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  interpolate: ge,
  interpolateArray: C0,
  interpolateBasis: Zo,
  interpolateBasisClosed: Qo,
  interpolateCubehelix: X0,
  interpolateCubehelixLong: B0,
  interpolateDate: nf,
  interpolateDiscrete: U0,
  interpolateHcl: z0,
  interpolateHclLong: W0,
  interpolateHsl: H0,
  interpolateHslLong: L0,
  interpolateHue: E0,
  interpolateLab: O0,
  interpolateNumber: xn,
  interpolateNumberArray: Wi,
  interpolateObject: ef,
  interpolateRgb: Mi,
  interpolateRgbBasis: S0,
  interpolateRgbBasisClosed: $0,
  interpolateRound: xr,
  interpolateString: tf,
  interpolateTransformCss: k0,
  interpolateTransformSvg: Y0,
  interpolateZoom: I0,
  piecewise: Xi,
  quantize: j0
}, Symbol.toStringTag, { value: "Module" }));
function Z0(n) {
  return function() {
    return n;
  };
}
function xi(n) {
  return +n;
}
var ha = [0, 1];
function on(n) {
  return n;
}
function Ti(n, e) {
  return (e -= n = +n) ? function(t) {
    return (t - n) / e;
  } : Z0(isNaN(e) ? NaN : 0.5);
}
function Q0(n, e) {
  var t;
  return n > e && (t = n, n = e, e = t), function(r) {
    return Math.max(n, Math.min(e, r));
  };
}
function V0(n, e, t) {
  var r = n[0], i = n[1], u = e[0], a = e[1];
  return i < r ? (r = Ti(i, r), u = t(a, u)) : (r = Ti(r, i), u = t(u, a)), function(o) {
    return u(r(o));
  };
}
function J0(n, e, t) {
  var r = Math.min(n.length, e.length) - 1, i = new Array(r), u = new Array(r), a = -1;
  for (n[r] < n[0] && (n = n.slice().reverse(), e = e.slice().reverse()); ++a < r; )
    i[a] = Ti(n[a], n[a + 1]), u[a] = t(e[a], e[a + 1]);
  return function(o) {
    var c = ce(n, o, 1, r) - 1;
    return u[c](i[c](o));
  };
}
function Ut(n, e) {
  return e.domain(n.domain()).range(n.range()).interpolate(n.interpolate()).clamp(n.clamp()).unknown(n.unknown());
}
function Tr() {
  var n = ha, e = ha, t = ge, r, i, u, a = on, o, c, f;
  function l() {
    var h = Math.min(n.length, e.length);
    return a !== on && (a = Q0(n[0], n[h - 1])), o = h > 2 ? J0 : V0, c = f = null, s;
  }
  function s(h) {
    return h == null || isNaN(h = +h) ? u : (c || (c = o(n.map(r), e, t)))(r(a(h)));
  }
  return s.invert = function(h) {
    return a(i((f || (f = o(e, n.map(r), xn)))(h)));
  }, s.domain = function(h) {
    return arguments.length ? (n = Array.from(h, xi), l()) : n.slice();
  }, s.range = function(h) {
    return arguments.length ? (e = Array.from(h), l()) : e.slice();
  }, s.rangeRound = function(h) {
    return e = Array.from(h), t = xr, l();
  }, s.clamp = function(h) {
    return arguments.length ? (a = h ? !0 : on, l()) : a !== on;
  }, s.interpolate = function(h) {
    return arguments.length ? (t = h, l()) : t;
  }, s.unknown = function(h) {
    return arguments.length ? (u = h, s) : u;
  }, function(h, g) {
    return r = h, i = g, l();
  };
}
function cf() {
  return Tr()(on, on);
}
function _0(n) {
  return Math.abs(n = Math.round(n)) >= 1e21 ? n.toLocaleString("en").replace(/,/g, "") : n.toString(10);
}
function fr(n, e) {
  if ((t = (n = e ? n.toExponential(e - 1) : n.toExponential()).indexOf("e")) < 0) return null;
  var t, r = n.slice(0, t);
  return [
    r.length > 1 ? r[0] + r.slice(2) : r,
    +n.slice(t + 1)
  ];
}
function Ee(n) {
  return n = fr(Math.abs(n)), n ? n[1] : NaN;
}
function K0(n, e) {
  return function(t, r) {
    for (var i = t.length, u = [], a = 0, o = n[0], c = 0; i > 0 && o > 0 && (c + o + 1 > r && (o = Math.max(1, r - c)), u.push(t.substring(i -= o, i + o)), !((c += o + 1) > r)); )
      o = n[a = (a + 1) % n.length];
    return u.reverse().join(e);
  };
}
function ns(n) {
  return function(e) {
    return e.replace(/[0-9]/g, function(t) {
      return n[+t];
    });
  };
}
var es = /^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$/i;
function Mt(n) {
  if (!(e = es.exec(n))) throw new Error("invalid format: " + n);
  var e;
  return new Bi({
    fill: e[1],
    align: e[2],
    sign: e[3],
    symbol: e[4],
    zero: e[5],
    width: e[6],
    comma: e[7],
    precision: e[8] && e[8].slice(1),
    trim: e[9],
    type: e[10]
  });
}
Mt.prototype = Bi.prototype;
function Bi(n) {
  this.fill = n.fill === void 0 ? " " : n.fill + "", this.align = n.align === void 0 ? ">" : n.align + "", this.sign = n.sign === void 0 ? "-" : n.sign + "", this.symbol = n.symbol === void 0 ? "" : n.symbol + "", this.zero = !!n.zero, this.width = n.width === void 0 ? void 0 : +n.width, this.comma = !!n.comma, this.precision = n.precision === void 0 ? void 0 : +n.precision, this.trim = !!n.trim, this.type = n.type === void 0 ? "" : n.type + "";
}
Bi.prototype.toString = function() {
  return this.fill + this.align + this.sign + this.symbol + (this.zero ? "0" : "") + (this.width === void 0 ? "" : Math.max(1, this.width | 0)) + (this.comma ? "," : "") + (this.precision === void 0 ? "" : "." + Math.max(0, this.precision | 0)) + (this.trim ? "~" : "") + this.type;
};
function ts(n) {
  n: for (var e = n.length, t = 1, r = -1, i; t < e; ++t)
    switch (n[t]) {
      case ".":
        r = i = t;
        break;
      case "0":
        r === 0 && (r = t), i = t;
        break;
      default:
        if (!+n[t]) break n;
        r > 0 && (r = 0);
        break;
    }
  return r > 0 ? n.slice(0, r) + n.slice(i + 1) : n;
}
var lf;
function rs(n, e) {
  var t = fr(n, e);
  if (!t) return n + "";
  var r = t[0], i = t[1], u = i - (lf = Math.max(-8, Math.min(8, Math.floor(i / 3))) * 3) + 1, a = r.length;
  return u === a ? r : u > a ? r + new Array(u - a + 1).join("0") : u > 0 ? r.slice(0, u) + "." + r.slice(u) : "0." + new Array(1 - u).join("0") + fr(n, Math.max(0, e + u - 1))[0];
}
function ga(n, e) {
  var t = fr(n, e);
  if (!t) return n + "";
  var r = t[0], i = t[1];
  return i < 0 ? "0." + new Array(-i).join("0") + r : r.length > i + 1 ? r.slice(0, i + 1) + "." + r.slice(i + 1) : r + new Array(i - r.length + 2).join("0");
}
const da = {
  "%": (n, e) => (n * 100).toFixed(e),
  b: (n) => Math.round(n).toString(2),
  c: (n) => n + "",
  d: _0,
  e: (n, e) => n.toExponential(e),
  f: (n, e) => n.toFixed(e),
  g: (n, e) => n.toPrecision(e),
  o: (n) => Math.round(n).toString(8),
  p: (n, e) => ga(n * 100, e),
  r: ga,
  s: rs,
  X: (n) => Math.round(n).toString(16).toUpperCase(),
  x: (n) => Math.round(n).toString(16)
};
function pa(n) {
  return n;
}
var ma = Array.prototype.map, ba = ["y", "z", "a", "f", "p", "n", "µ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y"];
function is(n) {
  var e = n.grouping === void 0 || n.thousands === void 0 ? pa : K0(ma.call(n.grouping, Number), n.thousands + ""), t = n.currency === void 0 ? "" : n.currency[0] + "", r = n.currency === void 0 ? "" : n.currency[1] + "", i = n.decimal === void 0 ? "." : n.decimal + "", u = n.numerals === void 0 ? pa : ns(ma.call(n.numerals, String)), a = n.percent === void 0 ? "%" : n.percent + "", o = n.minus === void 0 ? "−" : n.minus + "", c = n.nan === void 0 ? "NaN" : n.nan + "";
  function f(s) {
    s = Mt(s);
    var h = s.fill, g = s.align, d = s.sign, p = s.symbol, m = s.zero, M = s.width, x = s.comma, b = s.precision, y = s.trim, T = s.type;
    T === "n" ? (x = !0, T = "g") : da[T] || (b === void 0 && (b = 12), y = !0, T = "g"), (m || h === "0" && g === "=") && (m = !0, h = "0", g = "=");
    var v = p === "$" ? t : p === "#" && /[boxX]/.test(T) ? "0" + T.toLowerCase() : "", C = p === "$" ? r : /[%p]/.test(T) ? a : "", U = da[T], k = /[defgprs%]/.test(T);
    b = b === void 0 ? 6 : /[gprs]/.test(T) ? Math.max(1, Math.min(21, b)) : Math.max(0, Math.min(20, b));
    function I($) {
      var X = v, F = C, Y, w, D;
      if (T === "c")
        F = U($) + F, $ = "";
      else {
        $ = +$;
        var z = $ < 0 || 1 / $ < 0;
        if ($ = isNaN($) ? c : U(Math.abs($), b), y && ($ = ts($)), z && +$ == 0 && d !== "+" && (z = !1), X = (z ? d === "(" ? d : o : d === "-" || d === "(" ? "" : d) + X, F = (T === "s" ? ba[8 + lf / 3] : "") + F + (z && d === "(" ? ")" : ""), k) {
          for (Y = -1, w = $.length; ++Y < w; )
            if (D = $.charCodeAt(Y), 48 > D || D > 57) {
              F = (D === 46 ? i + $.slice(Y + 1) : $.slice(Y)) + F, $ = $.slice(0, Y);
              break;
            }
        }
      }
      x && !m && ($ = e($, 1 / 0));
      var Q = X.length + $.length + F.length, j = Q < M ? new Array(M - Q + 1).join(h) : "";
      switch (x && m && ($ = e(j + $, j.length ? M - F.length : 1 / 0), j = ""), g) {
        case "<":
          $ = X + $ + F + j;
          break;
        case "=":
          $ = X + j + $ + F;
          break;
        case "^":
          $ = j.slice(0, Q = j.length >> 1) + X + $ + F + j.slice(Q);
          break;
        default:
          $ = j + X + $ + F;
          break;
      }
      return u($);
    }
    return I.toString = function() {
      return s + "";
    }, I;
  }
  function l(s, h) {
    var g = f((s = Mt(s), s.type = "f", s)), d = Math.max(-8, Math.min(8, Math.floor(Ee(h) / 3))) * 3, p = Math.pow(10, -d), m = ba[8 + d / 3];
    return function(M) {
      return g(p * M) + m;
    };
  }
  return {
    format: f,
    formatPrefix: l
  };
}
var zt, ji, sf;
us({
  thousands: ",",
  grouping: [3],
  currency: ["$", ""]
});
function us(n) {
  return zt = is(n), ji = zt.format, sf = zt.formatPrefix, zt;
}
function as(n) {
  return Math.max(0, -Ee(Math.abs(n)));
}
function os(n, e) {
  return Math.max(0, Math.max(-8, Math.min(8, Math.floor(Ee(e) / 3))) * 3 - Ee(Math.abs(n)));
}
function fs(n, e) {
  return n = Math.abs(n), e = Math.abs(e) - n, Math.max(0, Ee(e) - Ee(n)) + 1;
}
function hf(n, e, t, r) {
  var i = ht(n, e, t), u;
  switch (r = Mt(r ?? ",f"), r.type) {
    case "s": {
      var a = Math.max(Math.abs(n), Math.abs(e));
      return r.precision == null && !isNaN(u = os(i, a)) && (r.precision = u), sf(r, a);
    }
    case "":
    case "e":
    case "g":
    case "p":
    case "r": {
      r.precision == null && !isNaN(u = fs(i, Math.max(Math.abs(n), Math.abs(e)))) && (r.precision = u - (r.type === "e"));
      break;
    }
    case "f":
    case "%": {
      r.precision == null && !isNaN(u = as(i)) && (r.precision = u - (r.type === "%") * 2);
      break;
    }
  }
  return ji(r);
}
function de(n) {
  var e = n.domain;
  return n.ticks = function(t) {
    var r = e();
    return Vr(r[0], r[r.length - 1], t ?? 10);
  }, n.tickFormat = function(t, r) {
    var i = e();
    return hf(i[0], i[i.length - 1], t ?? 10, r);
  }, n.nice = function(t) {
    t == null && (t = 10);
    var r = e(), i = 0, u = r.length - 1, a = r[i], o = r[u], c, f, l = 10;
    for (o < a && (f = a, a = o, o = f, f = i, i = u, u = f); l-- > 0; ) {
      if (f = Jr(a, o, t), f === c)
        return r[i] = a, r[u] = o, e(r);
      if (f > 0)
        a = Math.floor(a / f) * f, o = Math.ceil(o / f) * f;
      else if (f < 0)
        a = Math.ceil(a * f) / f, o = Math.floor(o * f) / f;
      else
        break;
      c = f;
    }
    return n;
  }, n;
}
function gf() {
  var n = cf();
  return n.copy = function() {
    return Ut(n, gf());
  }, kn.apply(n, arguments), de(n);
}
function df(n) {
  var e;
  function t(r) {
    return r == null || isNaN(r = +r) ? e : r;
  }
  return t.invert = t, t.domain = t.range = function(r) {
    return arguments.length ? (n = Array.from(r, xi), t) : n.slice();
  }, t.unknown = function(r) {
    return arguments.length ? (e = r, t) : e;
  }, t.copy = function() {
    return df(n).unknown(e);
  }, n = arguments.length ? Array.from(n, xi) : [0, 1], de(t);
}
function pf(n, e) {
  n = n.slice();
  var t = 0, r = n.length - 1, i = n[t], u = n[r], a;
  return u < i && (a = t, t = r, r = a, a = i, i = u, u = a), n[t] = e.floor(i), n[r] = e.ceil(u), n;
}
function ya(n) {
  return Math.log(n);
}
function Ma(n) {
  return Math.exp(n);
}
function cs(n) {
  return -Math.log(-n);
}
function ls(n) {
  return -Math.exp(-n);
}
function ss(n) {
  return isFinite(n) ? +("1e" + n) : n < 0 ? 0 : n;
}
function hs(n) {
  return n === 10 ? ss : n === Math.E ? Math.exp : (e) => Math.pow(n, e);
}
function gs(n) {
  return n === Math.E ? Math.log : n === 10 && Math.log10 || n === 2 && Math.log2 || (n = Math.log(n), (e) => Math.log(e) / n);
}
function va(n) {
  return (e, t) => -n(-e, t);
}
function Gi(n) {
  const e = n(ya, Ma), t = e.domain;
  let r = 10, i, u;
  function a() {
    return i = gs(r), u = hs(r), t()[0] < 0 ? (i = va(i), u = va(u), n(cs, ls)) : n(ya, Ma), e;
  }
  return e.base = function(o) {
    return arguments.length ? (r = +o, a()) : r;
  }, e.domain = function(o) {
    return arguments.length ? (t(o), a()) : t();
  }, e.ticks = (o) => {
    const c = t();
    let f = c[0], l = c[c.length - 1];
    const s = l < f;
    s && ([f, l] = [l, f]);
    let h = i(f), g = i(l), d, p;
    const m = o == null ? 10 : +o;
    let M = [];
    if (!(r % 1) && g - h < m) {
      if (h = Math.floor(h), g = Math.ceil(g), f > 0) {
        for (; h <= g; ++h)
          for (d = 1; d < r; ++d)
            if (p = h < 0 ? d / u(-h) : d * u(h), !(p < f)) {
              if (p > l) break;
              M.push(p);
            }
      } else for (; h <= g; ++h)
        for (d = r - 1; d >= 1; --d)
          if (p = h > 0 ? d / u(-h) : d * u(h), !(p < f)) {
            if (p > l) break;
            M.push(p);
          }
      M.length * 2 < m && (M = Vr(f, l, m));
    } else
      M = Vr(h, g, Math.min(g - h, m)).map(u);
    return s ? M.reverse() : M;
  }, e.tickFormat = (o, c) => {
    if (o == null && (o = 10), c == null && (c = r === 10 ? "s" : ","), typeof c != "function" && (!(r % 1) && (c = Mt(c)).precision == null && (c.trim = !0), c = ji(c)), o === 1 / 0) return c;
    const f = Math.max(1, r * o / e.ticks().length);
    return (l) => {
      let s = l / u(Math.round(i(l)));
      return s * r < r - 0.5 && (s *= r), s <= f ? c(l) : "";
    };
  }, e.nice = () => t(pf(t(), {
    floor: (o) => u(Math.floor(i(o))),
    ceil: (o) => u(Math.ceil(i(o)))
  })), e;
}
function mf() {
  const n = Gi(Tr()).domain([1, 10]);
  return n.copy = () => Ut(n, mf()).base(n.base()), kn.apply(n, arguments), n;
}
function wa(n) {
  return function(e) {
    return Math.sign(e) * Math.log1p(Math.abs(e / n));
  };
}
function xa(n) {
  return function(e) {
    return Math.sign(e) * Math.expm1(Math.abs(e)) * n;
  };
}
function Zi(n) {
  var e = 1, t = n(wa(e), xa(e));
  return t.constant = function(r) {
    return arguments.length ? n(wa(e = +r), xa(e)) : e;
  }, de(t);
}
function bf() {
  var n = Zi(Tr());
  return n.copy = function() {
    return Ut(n, bf()).constant(n.constant());
  }, kn.apply(n, arguments);
}
function Ta(n) {
  return function(e) {
    return e < 0 ? -Math.pow(-e, n) : Math.pow(e, n);
  };
}
function ds(n) {
  return n < 0 ? -Math.sqrt(-n) : Math.sqrt(n);
}
function ps(n) {
  return n < 0 ? -n * n : n * n;
}
function Qi(n) {
  var e = n(on, on), t = 1;
  function r() {
    return t === 1 ? n(on, on) : t === 0.5 ? n(ds, ps) : n(Ta(t), Ta(1 / t));
  }
  return e.exponent = function(i) {
    return arguments.length ? (t = +i, r()) : t;
  }, de(e);
}
function Vi() {
  var n = Qi(Tr());
  return n.copy = function() {
    return Ut(n, Vi()).exponent(n.exponent());
  }, kn.apply(n, arguments), n;
}
function ms() {
  return Vi.apply(null, arguments).exponent(0.5);
}
function yf() {
  var n = [], e = [], t = [], r;
  function i() {
    var a = 0, o = Math.max(1, e.length);
    for (t = new Array(o - 1); ++a < o; ) t[a - 1] = Za(n, a / o);
    return u;
  }
  function u(a) {
    return a == null || isNaN(a = +a) ? r : e[ce(t, a)];
  }
  return u.invertExtent = function(a) {
    var o = e.indexOf(a);
    return o < 0 ? [NaN, NaN] : [
      o > 0 ? t[o - 1] : n[0],
      o < t.length ? t[o] : n[n.length - 1]
    ];
  }, u.domain = function(a) {
    if (!arguments.length) return n.slice();
    n = [];
    for (let o of a) o != null && !isNaN(o = +o) && n.push(o);
    return n.sort(Ln), i();
  }, u.range = function(a) {
    return arguments.length ? (e = Array.from(a), i()) : e.slice();
  }, u.unknown = function(a) {
    return arguments.length ? (r = a, u) : r;
  }, u.quantiles = function() {
    return t.slice();
  }, u.copy = function() {
    return yf().domain(n).range(e).unknown(r);
  }, kn.apply(u, arguments);
}
function Mf() {
  var n = 0, e = 1, t = 1, r = [0.5], i = [0, 1], u;
  function a(c) {
    return c != null && c <= c ? i[ce(r, c, 0, t)] : u;
  }
  function o() {
    var c = -1;
    for (r = new Array(t); ++c < t; ) r[c] = ((c + 1) * e - (c - t) * n) / (t + 1);
    return a;
  }
  return a.domain = function(c) {
    return arguments.length ? ([n, e] = c, n = +n, e = +e, o()) : [n, e];
  }, a.range = function(c) {
    return arguments.length ? (t = (i = Array.from(c)).length - 1, o()) : i.slice();
  }, a.invertExtent = function(c) {
    var f = i.indexOf(c);
    return f < 0 ? [NaN, NaN] : f < 1 ? [n, r[0]] : f >= t ? [r[t - 1], e] : [r[f - 1], r[f]];
  }, a.unknown = function(c) {
    return arguments.length && (u = c), a;
  }, a.thresholds = function() {
    return r.slice();
  }, a.copy = function() {
    return Mf().domain([n, e]).range(i).unknown(u);
  }, kn.apply(de(a), arguments);
}
function vf() {
  var n = [0.5], e = [0, 1], t, r = 1;
  function i(u) {
    return u != null && u <= u ? e[ce(n, u, 0, r)] : t;
  }
  return i.domain = function(u) {
    return arguments.length ? (n = Array.from(u), r = Math.min(n.length, e.length - 1), i) : n.slice();
  }, i.range = function(u) {
    return arguments.length ? (e = Array.from(u), r = Math.min(n.length, e.length - 1), i) : e.slice();
  }, i.invertExtent = function(u) {
    var a = e.indexOf(u);
    return [n[a - 1], n[a]];
  }, i.unknown = function(u) {
    return arguments.length ? (t = u, i) : t;
  }, i.copy = function() {
    return vf().domain(n).range(e).unknown(t);
  }, kn.apply(i, arguments);
}
const Or = /* @__PURE__ */ new Date(), zr = /* @__PURE__ */ new Date();
function V(n, e, t, r) {
  function i(u) {
    return n(u = arguments.length === 0 ? /* @__PURE__ */ new Date() : /* @__PURE__ */ new Date(+u)), u;
  }
  return i.floor = (u) => (n(u = /* @__PURE__ */ new Date(+u)), u), i.ceil = (u) => (n(u = new Date(u - 1)), e(u, 1), n(u), u), i.round = (u) => {
    const a = i(u), o = i.ceil(u);
    return u - a < o - u ? a : o;
  }, i.offset = (u, a) => (e(u = /* @__PURE__ */ new Date(+u), a == null ? 1 : Math.floor(a)), u), i.range = (u, a, o) => {
    const c = [];
    if (u = i.ceil(u), o = o == null ? 1 : Math.floor(o), !(u < a) || !(o > 0)) return c;
    let f;
    do
      c.push(f = /* @__PURE__ */ new Date(+u)), e(u, o), n(u);
    while (f < u && u < a);
    return c;
  }, i.filter = (u) => V((a) => {
    if (a >= a) for (; n(a), !u(a); ) a.setTime(a - 1);
  }, (a, o) => {
    if (a >= a)
      if (o < 0) for (; ++o <= 0; )
        for (; e(a, -1), !u(a); )
          ;
      else for (; --o >= 0; )
        for (; e(a, 1), !u(a); )
          ;
  }), t && (i.count = (u, a) => (Or.setTime(+u), zr.setTime(+a), n(Or), n(zr), Math.floor(t(Or, zr))), i.every = (u) => (u = Math.floor(u), !isFinite(u) || !(u > 0) ? null : u > 1 ? i.filter(r ? (a) => r(a) % u === 0 : (a) => i.count(0, a) % u === 0) : i)), i;
}
const cr = V(() => {
}, (n, e) => {
  n.setTime(+n + e);
}, (n, e) => e - n);
cr.every = (n) => (n = Math.floor(n), !isFinite(n) || !(n > 0) ? null : n > 1 ? V((e) => {
  e.setTime(Math.floor(e / n) * n);
}, (e, t) => {
  e.setTime(+e + t * n);
}, (e, t) => (t - e) / n) : cr);
cr.range;
const In = 1e3, bn = In * 60, Hn = bn * 60, zn = Hn * 24, Ji = zn * 7, Sa = zn * 30, Wr = zn * 365, ae = V((n) => {
  n.setTime(n - n.getMilliseconds());
}, (n, e) => {
  n.setTime(+n + e * In);
}, (n, e) => (e - n) / In, (n) => n.getUTCSeconds());
ae.range;
const _i = V((n) => {
  n.setTime(n - n.getMilliseconds() - n.getSeconds() * In);
}, (n, e) => {
  n.setTime(+n + e * bn);
}, (n, e) => (e - n) / bn, (n) => n.getMinutes());
_i.range;
const Ki = V((n) => {
  n.setUTCSeconds(0, 0);
}, (n, e) => {
  n.setTime(+n + e * bn);
}, (n, e) => (e - n) / bn, (n) => n.getUTCMinutes());
Ki.range;
const nu = V((n) => {
  n.setTime(n - n.getMilliseconds() - n.getSeconds() * In - n.getMinutes() * bn);
}, (n, e) => {
  n.setTime(+n + e * Hn);
}, (n, e) => (e - n) / Hn, (n) => n.getHours());
nu.range;
const eu = V((n) => {
  n.setUTCMinutes(0, 0, 0);
}, (n, e) => {
  n.setTime(+n + e * Hn);
}, (n, e) => (e - n) / Hn, (n) => n.getUTCHours());
eu.range;
const Et = V(
  (n) => n.setHours(0, 0, 0, 0),
  (n, e) => n.setDate(n.getDate() + e),
  (n, e) => (e - n - (e.getTimezoneOffset() - n.getTimezoneOffset()) * bn) / zn,
  (n) => n.getDate() - 1
);
Et.range;
const Sr = V((n) => {
  n.setUTCHours(0, 0, 0, 0);
}, (n, e) => {
  n.setUTCDate(n.getUTCDate() + e);
}, (n, e) => (e - n) / zn, (n) => n.getUTCDate() - 1);
Sr.range;
const wf = V((n) => {
  n.setUTCHours(0, 0, 0, 0);
}, (n, e) => {
  n.setUTCDate(n.getUTCDate() + e);
}, (n, e) => (e - n) / zn, (n) => Math.floor(n / zn));
wf.range;
function pe(n) {
  return V((e) => {
    e.setDate(e.getDate() - (e.getDay() + 7 - n) % 7), e.setHours(0, 0, 0, 0);
  }, (e, t) => {
    e.setDate(e.getDate() + t * 7);
  }, (e, t) => (t - e - (t.getTimezoneOffset() - e.getTimezoneOffset()) * bn) / Ji);
}
const $r = pe(0), lr = pe(1), bs = pe(2), ys = pe(3), Fe = pe(4), Ms = pe(5), vs = pe(6);
$r.range;
lr.range;
bs.range;
ys.range;
Fe.range;
Ms.range;
vs.range;
function me(n) {
  return V((e) => {
    e.setUTCDate(e.getUTCDate() - (e.getUTCDay() + 7 - n) % 7), e.setUTCHours(0, 0, 0, 0);
  }, (e, t) => {
    e.setUTCDate(e.getUTCDate() + t * 7);
  }, (e, t) => (t - e) / Ji);
}
const Cr = me(0), sr = me(1), ws = me(2), xs = me(3), Ae = me(4), Ts = me(5), Ss = me(6);
Cr.range;
sr.range;
ws.range;
xs.range;
Ae.range;
Ts.range;
Ss.range;
const tu = V((n) => {
  n.setDate(1), n.setHours(0, 0, 0, 0);
}, (n, e) => {
  n.setMonth(n.getMonth() + e);
}, (n, e) => e.getMonth() - n.getMonth() + (e.getFullYear() - n.getFullYear()) * 12, (n) => n.getMonth());
tu.range;
const ru = V((n) => {
  n.setUTCDate(1), n.setUTCHours(0, 0, 0, 0);
}, (n, e) => {
  n.setUTCMonth(n.getUTCMonth() + e);
}, (n, e) => e.getUTCMonth() - n.getUTCMonth() + (e.getUTCFullYear() - n.getUTCFullYear()) * 12, (n) => n.getUTCMonth());
ru.range;
const Wn = V((n) => {
  n.setMonth(0, 1), n.setHours(0, 0, 0, 0);
}, (n, e) => {
  n.setFullYear(n.getFullYear() + e);
}, (n, e) => e.getFullYear() - n.getFullYear(), (n) => n.getFullYear());
Wn.every = (n) => !isFinite(n = Math.floor(n)) || !(n > 0) ? null : V((e) => {
  e.setFullYear(Math.floor(e.getFullYear() / n) * n), e.setMonth(0, 1), e.setHours(0, 0, 0, 0);
}, (e, t) => {
  e.setFullYear(e.getFullYear() + t * n);
});
Wn.range;
const Xn = V((n) => {
  n.setUTCMonth(0, 1), n.setUTCHours(0, 0, 0, 0);
}, (n, e) => {
  n.setUTCFullYear(n.getUTCFullYear() + e);
}, (n, e) => e.getUTCFullYear() - n.getUTCFullYear(), (n) => n.getUTCFullYear());
Xn.every = (n) => !isFinite(n = Math.floor(n)) || !(n > 0) ? null : V((e) => {
  e.setUTCFullYear(Math.floor(e.getUTCFullYear() / n) * n), e.setUTCMonth(0, 1), e.setUTCHours(0, 0, 0, 0);
}, (e, t) => {
  e.setUTCFullYear(e.getUTCFullYear() + t * n);
});
Xn.range;
function xf(n, e, t, r, i, u) {
  const a = [
    [ae, 1, In],
    [ae, 5, 5 * In],
    [ae, 15, 15 * In],
    [ae, 30, 30 * In],
    [u, 1, bn],
    [u, 5, 5 * bn],
    [u, 15, 15 * bn],
    [u, 30, 30 * bn],
    [i, 1, Hn],
    [i, 3, 3 * Hn],
    [i, 6, 6 * Hn],
    [i, 12, 12 * Hn],
    [r, 1, zn],
    [r, 2, 2 * zn],
    [t, 1, Ji],
    [e, 1, Sa],
    [e, 3, 3 * Sa],
    [n, 1, Wr]
  ];
  function o(f, l, s) {
    const h = l < f;
    h && ([f, l] = [l, f]);
    const g = s && typeof s.range == "function" ? s : c(f, l, s), d = g ? g.range(f, +l + 1) : [];
    return h ? d.reverse() : d;
  }
  function c(f, l, s) {
    const h = Math.abs(l - f) / s, g = dr(([, , m]) => m).right(a, h);
    if (g === a.length) return n.every(ht(f / Wr, l / Wr, s));
    if (g === 0) return cr.every(Math.max(ht(f, l, s), 1));
    const [d, p] = a[h / a[g - 1][2] < a[g][2] / h ? g - 1 : g];
    return d.every(p);
  }
  return [o, c];
}
const [$s, Cs] = xf(Xn, ru, Cr, wf, eu, Ki), [Ns, Ds] = xf(Wn, tu, $r, Et, nu, _i);
function Xr(n) {
  if (0 <= n.y && n.y < 100) {
    var e = new Date(-1, n.m, n.d, n.H, n.M, n.S, n.L);
    return e.setFullYear(n.y), e;
  }
  return new Date(n.y, n.m, n.d, n.H, n.M, n.S, n.L);
}
function Br(n) {
  if (0 <= n.y && n.y < 100) {
    var e = new Date(Date.UTC(-1, n.m, n.d, n.H, n.M, n.S, n.L));
    return e.setUTCFullYear(n.y), e;
  }
  return new Date(Date.UTC(n.y, n.m, n.d, n.H, n.M, n.S, n.L));
}
function Xe(n, e, t) {
  return { y: n, m: e, d: t, H: 0, M: 0, S: 0, L: 0 };
}
function Us(n) {
  var e = n.dateTime, t = n.date, r = n.time, i = n.periods, u = n.days, a = n.shortDays, o = n.months, c = n.shortMonths, f = Be(i), l = je(i), s = Be(u), h = je(u), g = Be(a), d = je(a), p = Be(o), m = je(o), M = Be(c), x = je(c), b = {
    a: z,
    A: Q,
    b: j,
    B: te,
    c: null,
    d: Ea,
    e: Ea,
    f: _s,
    g: f1,
    G: l1,
    H: Qs,
    I: Vs,
    j: Js,
    L: Tf,
    m: Ks,
    M: n1,
    p: vn,
    q: Rn,
    Q: ka,
    s: Ya,
    S: e1,
    u: t1,
    U: r1,
    V: i1,
    w: u1,
    W: a1,
    x: null,
    X: null,
    y: o1,
    Y: c1,
    Z: s1,
    "%": Aa
  }, y = {
    a: wn,
    A: ve,
    b: Zn,
    B: tc,
    c: null,
    d: Fa,
    e: Fa,
    f: p1,
    g: $1,
    G: N1,
    H: h1,
    I: g1,
    j: d1,
    L: $f,
    m: m1,
    M: b1,
    p: rc,
    q: ic,
    Q: ka,
    s: Ya,
    S: y1,
    u: M1,
    U: v1,
    V: w1,
    w: x1,
    W: T1,
    x: null,
    X: null,
    y: S1,
    Y: C1,
    Z: D1,
    "%": Aa
  }, T = {
    a: I,
    A: $,
    b: X,
    B: F,
    c: Y,
    d: Da,
    e: Da,
    f: Bs,
    g: Na,
    G: Ca,
    H: Ua,
    I: Ua,
    j: Os,
    L: Xs,
    m: Ls,
    M: zs,
    p: k,
    q: Hs,
    Q: Gs,
    s: Zs,
    S: Ws,
    u: Ys,
    U: Rs,
    V: qs,
    w: ks,
    W: Ps,
    x: w,
    X: D,
    y: Na,
    Y: Ca,
    Z: Is,
    "%": js
  };
  b.x = v(t, b), b.X = v(r, b), b.c = v(e, b), y.x = v(t, y), y.X = v(r, y), y.c = v(e, y);
  function v(N, P) {
    return function(H) {
      var S = [], un = -1, B = 0, ln = N.length, sn, re, Su;
      for (H instanceof Date || (H = /* @__PURE__ */ new Date(+H)); ++un < ln; )
        N.charCodeAt(un) === 37 && (S.push(N.slice(B, un)), (re = $a[sn = N.charAt(++un)]) != null ? sn = N.charAt(++un) : re = sn === "e" ? " " : "0", (Su = P[sn]) && (sn = Su(H, re)), S.push(sn), B = un + 1);
      return S.push(N.slice(B, un)), S.join("");
    };
  }
  function C(N, P) {
    return function(H) {
      var S = Xe(1900, void 0, 1), un = U(S, N, H += "", 0), B, ln;
      if (un != H.length) return null;
      if ("Q" in S) return new Date(S.Q);
      if ("s" in S) return new Date(S.s * 1e3 + ("L" in S ? S.L : 0));
      if (P && !("Z" in S) && (S.Z = 0), "p" in S && (S.H = S.H % 12 + S.p * 12), S.m === void 0 && (S.m = "q" in S ? S.q : 0), "V" in S) {
        if (S.V < 1 || S.V > 53) return null;
        "w" in S || (S.w = 1), "Z" in S ? (B = Br(Xe(S.y, 0, 1)), ln = B.getUTCDay(), B = ln > 4 || ln === 0 ? sr.ceil(B) : sr(B), B = Sr.offset(B, (S.V - 1) * 7), S.y = B.getUTCFullYear(), S.m = B.getUTCMonth(), S.d = B.getUTCDate() + (S.w + 6) % 7) : (B = Xr(Xe(S.y, 0, 1)), ln = B.getDay(), B = ln > 4 || ln === 0 ? lr.ceil(B) : lr(B), B = Et.offset(B, (S.V - 1) * 7), S.y = B.getFullYear(), S.m = B.getMonth(), S.d = B.getDate() + (S.w + 6) % 7);
      } else ("W" in S || "U" in S) && ("w" in S || (S.w = "u" in S ? S.u % 7 : "W" in S ? 1 : 0), ln = "Z" in S ? Br(Xe(S.y, 0, 1)).getUTCDay() : Xr(Xe(S.y, 0, 1)).getDay(), S.m = 0, S.d = "W" in S ? (S.w + 6) % 7 + S.W * 7 - (ln + 5) % 7 : S.w + S.U * 7 - (ln + 6) % 7);
      return "Z" in S ? (S.H += S.Z / 100 | 0, S.M += S.Z % 100, Br(S)) : Xr(S);
    };
  }
  function U(N, P, H, S) {
    for (var un = 0, B = P.length, ln = H.length, sn, re; un < B; ) {
      if (S >= ln) return -1;
      if (sn = P.charCodeAt(un++), sn === 37) {
        if (sn = P.charAt(un++), re = T[sn in $a ? P.charAt(un++) : sn], !re || (S = re(N, H, S)) < 0) return -1;
      } else if (sn != H.charCodeAt(S++))
        return -1;
    }
    return S;
  }
  function k(N, P, H) {
    var S = f.exec(P.slice(H));
    return S ? (N.p = l.get(S[0].toLowerCase()), H + S[0].length) : -1;
  }
  function I(N, P, H) {
    var S = g.exec(P.slice(H));
    return S ? (N.w = d.get(S[0].toLowerCase()), H + S[0].length) : -1;
  }
  function $(N, P, H) {
    var S = s.exec(P.slice(H));
    return S ? (N.w = h.get(S[0].toLowerCase()), H + S[0].length) : -1;
  }
  function X(N, P, H) {
    var S = M.exec(P.slice(H));
    return S ? (N.m = x.get(S[0].toLowerCase()), H + S[0].length) : -1;
  }
  function F(N, P, H) {
    var S = p.exec(P.slice(H));
    return S ? (N.m = m.get(S[0].toLowerCase()), H + S[0].length) : -1;
  }
  function Y(N, P, H) {
    return U(N, e, P, H);
  }
  function w(N, P, H) {
    return U(N, t, P, H);
  }
  function D(N, P, H) {
    return U(N, r, P, H);
  }
  function z(N) {
    return a[N.getDay()];
  }
  function Q(N) {
    return u[N.getDay()];
  }
  function j(N) {
    return c[N.getMonth()];
  }
  function te(N) {
    return o[N.getMonth()];
  }
  function vn(N) {
    return i[+(N.getHours() >= 12)];
  }
  function Rn(N) {
    return 1 + ~~(N.getMonth() / 3);
  }
  function wn(N) {
    return a[N.getUTCDay()];
  }
  function ve(N) {
    return u[N.getUTCDay()];
  }
  function Zn(N) {
    return c[N.getUTCMonth()];
  }
  function tc(N) {
    return o[N.getUTCMonth()];
  }
  function rc(N) {
    return i[+(N.getUTCHours() >= 12)];
  }
  function ic(N) {
    return 1 + ~~(N.getUTCMonth() / 3);
  }
  return {
    format: function(N) {
      var P = v(N += "", b);
      return P.toString = function() {
        return N;
      }, P;
    },
    parse: function(N) {
      var P = C(N += "", !1);
      return P.toString = function() {
        return N;
      }, P;
    },
    utcFormat: function(N) {
      var P = v(N += "", y);
      return P.toString = function() {
        return N;
      }, P;
    },
    utcParse: function(N) {
      var P = C(N += "", !0);
      return P.toString = function() {
        return N;
      }, P;
    }
  };
}
var $a = { "-": "", _: " ", 0: "0" }, en = /^\s*\d+/, Es = /^%/, Fs = /[\\^$*+?|[\]().{}]/g;
function L(n, e, t) {
  var r = n < 0 ? "-" : "", i = (r ? -n : n) + "", u = i.length;
  return r + (u < t ? new Array(t - u + 1).join(e) + i : i);
}
function As(n) {
  return n.replace(Fs, "\\$&");
}
function Be(n) {
  return new RegExp("^(?:" + n.map(As).join("|") + ")", "i");
}
function je(n) {
  return new Map(n.map((e, t) => [e.toLowerCase(), t]));
}
function ks(n, e, t) {
  var r = en.exec(e.slice(t, t + 1));
  return r ? (n.w = +r[0], t + r[0].length) : -1;
}
function Ys(n, e, t) {
  var r = en.exec(e.slice(t, t + 1));
  return r ? (n.u = +r[0], t + r[0].length) : -1;
}
function Rs(n, e, t) {
  var r = en.exec(e.slice(t, t + 2));
  return r ? (n.U = +r[0], t + r[0].length) : -1;
}
function qs(n, e, t) {
  var r = en.exec(e.slice(t, t + 2));
  return r ? (n.V = +r[0], t + r[0].length) : -1;
}
function Ps(n, e, t) {
  var r = en.exec(e.slice(t, t + 2));
  return r ? (n.W = +r[0], t + r[0].length) : -1;
}
function Ca(n, e, t) {
  var r = en.exec(e.slice(t, t + 4));
  return r ? (n.y = +r[0], t + r[0].length) : -1;
}
function Na(n, e, t) {
  var r = en.exec(e.slice(t, t + 2));
  return r ? (n.y = +r[0] + (+r[0] > 68 ? 1900 : 2e3), t + r[0].length) : -1;
}
function Is(n, e, t) {
  var r = /^(Z)|([+-]\d\d)(?::?(\d\d))?/.exec(e.slice(t, t + 6));
  return r ? (n.Z = r[1] ? 0 : -(r[2] + (r[3] || "00")), t + r[0].length) : -1;
}
function Hs(n, e, t) {
  var r = en.exec(e.slice(t, t + 1));
  return r ? (n.q = r[0] * 3 - 3, t + r[0].length) : -1;
}
function Ls(n, e, t) {
  var r = en.exec(e.slice(t, t + 2));
  return r ? (n.m = r[0] - 1, t + r[0].length) : -1;
}
function Da(n, e, t) {
  var r = en.exec(e.slice(t, t + 2));
  return r ? (n.d = +r[0], t + r[0].length) : -1;
}
function Os(n, e, t) {
  var r = en.exec(e.slice(t, t + 3));
  return r ? (n.m = 0, n.d = +r[0], t + r[0].length) : -1;
}
function Ua(n, e, t) {
  var r = en.exec(e.slice(t, t + 2));
  return r ? (n.H = +r[0], t + r[0].length) : -1;
}
function zs(n, e, t) {
  var r = en.exec(e.slice(t, t + 2));
  return r ? (n.M = +r[0], t + r[0].length) : -1;
}
function Ws(n, e, t) {
  var r = en.exec(e.slice(t, t + 2));
  return r ? (n.S = +r[0], t + r[0].length) : -1;
}
function Xs(n, e, t) {
  var r = en.exec(e.slice(t, t + 3));
  return r ? (n.L = +r[0], t + r[0].length) : -1;
}
function Bs(n, e, t) {
  var r = en.exec(e.slice(t, t + 6));
  return r ? (n.L = Math.floor(r[0] / 1e3), t + r[0].length) : -1;
}
function js(n, e, t) {
  var r = Es.exec(e.slice(t, t + 1));
  return r ? t + r[0].length : -1;
}
function Gs(n, e, t) {
  var r = en.exec(e.slice(t));
  return r ? (n.Q = +r[0], t + r[0].length) : -1;
}
function Zs(n, e, t) {
  var r = en.exec(e.slice(t));
  return r ? (n.s = +r[0], t + r[0].length) : -1;
}
function Ea(n, e) {
  return L(n.getDate(), e, 2);
}
function Qs(n, e) {
  return L(n.getHours(), e, 2);
}
function Vs(n, e) {
  return L(n.getHours() % 12 || 12, e, 2);
}
function Js(n, e) {
  return L(1 + Et.count(Wn(n), n), e, 3);
}
function Tf(n, e) {
  return L(n.getMilliseconds(), e, 3);
}
function _s(n, e) {
  return Tf(n, e) + "000";
}
function Ks(n, e) {
  return L(n.getMonth() + 1, e, 2);
}
function n1(n, e) {
  return L(n.getMinutes(), e, 2);
}
function e1(n, e) {
  return L(n.getSeconds(), e, 2);
}
function t1(n) {
  var e = n.getDay();
  return e === 0 ? 7 : e;
}
function r1(n, e) {
  return L($r.count(Wn(n) - 1, n), e, 2);
}
function Sf(n) {
  var e = n.getDay();
  return e >= 4 || e === 0 ? Fe(n) : Fe.ceil(n);
}
function i1(n, e) {
  return n = Sf(n), L(Fe.count(Wn(n), n) + (Wn(n).getDay() === 4), e, 2);
}
function u1(n) {
  return n.getDay();
}
function a1(n, e) {
  return L(lr.count(Wn(n) - 1, n), e, 2);
}
function o1(n, e) {
  return L(n.getFullYear() % 100, e, 2);
}
function f1(n, e) {
  return n = Sf(n), L(n.getFullYear() % 100, e, 2);
}
function c1(n, e) {
  return L(n.getFullYear() % 1e4, e, 4);
}
function l1(n, e) {
  var t = n.getDay();
  return n = t >= 4 || t === 0 ? Fe(n) : Fe.ceil(n), L(n.getFullYear() % 1e4, e, 4);
}
function s1(n) {
  var e = n.getTimezoneOffset();
  return (e > 0 ? "-" : (e *= -1, "+")) + L(e / 60 | 0, "0", 2) + L(e % 60, "0", 2);
}
function Fa(n, e) {
  return L(n.getUTCDate(), e, 2);
}
function h1(n, e) {
  return L(n.getUTCHours(), e, 2);
}
function g1(n, e) {
  return L(n.getUTCHours() % 12 || 12, e, 2);
}
function d1(n, e) {
  return L(1 + Sr.count(Xn(n), n), e, 3);
}
function $f(n, e) {
  return L(n.getUTCMilliseconds(), e, 3);
}
function p1(n, e) {
  return $f(n, e) + "000";
}
function m1(n, e) {
  return L(n.getUTCMonth() + 1, e, 2);
}
function b1(n, e) {
  return L(n.getUTCMinutes(), e, 2);
}
function y1(n, e) {
  return L(n.getUTCSeconds(), e, 2);
}
function M1(n) {
  var e = n.getUTCDay();
  return e === 0 ? 7 : e;
}
function v1(n, e) {
  return L(Cr.count(Xn(n) - 1, n), e, 2);
}
function Cf(n) {
  var e = n.getUTCDay();
  return e >= 4 || e === 0 ? Ae(n) : Ae.ceil(n);
}
function w1(n, e) {
  return n = Cf(n), L(Ae.count(Xn(n), n) + (Xn(n).getUTCDay() === 4), e, 2);
}
function x1(n) {
  return n.getUTCDay();
}
function T1(n, e) {
  return L(sr.count(Xn(n) - 1, n), e, 2);
}
function S1(n, e) {
  return L(n.getUTCFullYear() % 100, e, 2);
}
function $1(n, e) {
  return n = Cf(n), L(n.getUTCFullYear() % 100, e, 2);
}
function C1(n, e) {
  return L(n.getUTCFullYear() % 1e4, e, 4);
}
function N1(n, e) {
  var t = n.getUTCDay();
  return n = t >= 4 || t === 0 ? Ae(n) : Ae.ceil(n), L(n.getUTCFullYear() % 1e4, e, 4);
}
function D1() {
  return "+0000";
}
function Aa() {
  return "%";
}
function ka(n) {
  return +n;
}
function Ya(n) {
  return Math.floor(+n / 1e3);
}
var we, Nf, Df;
U1({
  dateTime: "%x, %X",
  date: "%-m/%-d/%Y",
  time: "%-I:%M:%S %p",
  periods: ["AM", "PM"],
  days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
  shortDays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
  shortMonths: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
});
function U1(n) {
  return we = Us(n), Nf = we.format, we.parse, Df = we.utcFormat, we.utcParse, we;
}
function E1(n) {
  return new Date(n);
}
function F1(n) {
  return n instanceof Date ? +n : +/* @__PURE__ */ new Date(+n);
}
function iu(n, e, t, r, i, u, a, o, c, f) {
  var l = cf(), s = l.invert, h = l.domain, g = f(".%L"), d = f(":%S"), p = f("%I:%M"), m = f("%I %p"), M = f("%a %d"), x = f("%b %d"), b = f("%B"), y = f("%Y");
  function T(v) {
    return (c(v) < v ? g : o(v) < v ? d : a(v) < v ? p : u(v) < v ? m : r(v) < v ? i(v) < v ? M : x : t(v) < v ? b : y)(v);
  }
  return l.invert = function(v) {
    return new Date(s(v));
  }, l.domain = function(v) {
    return arguments.length ? h(Array.from(v, F1)) : h().map(E1);
  }, l.ticks = function(v) {
    var C = h();
    return n(C[0], C[C.length - 1], v ?? 10);
  }, l.tickFormat = function(v, C) {
    return C == null ? T : f(C);
  }, l.nice = function(v) {
    var C = h();
    return (!v || typeof v.range != "function") && (v = e(C[0], C[C.length - 1], v ?? 10)), v ? h(pf(C, v)) : l;
  }, l.copy = function() {
    return Ut(l, iu(n, e, t, r, i, u, a, o, c, f));
  }, l;
}
function A1() {
  return kn.apply(iu(Ns, Ds, Wn, tu, $r, Et, nu, _i, ae, Nf).domain([new Date(2e3, 0, 1), new Date(2e3, 0, 2)]), arguments);
}
function k1() {
  return kn.apply(iu($s, Cs, Xn, ru, Cr, Sr, eu, Ki, ae, Df).domain([Date.UTC(2e3, 0, 1), Date.UTC(2e3, 0, 2)]), arguments);
}
function Nr() {
  var n = 0, e = 1, t, r, i, u, a = on, o = !1, c;
  function f(s) {
    return s == null || isNaN(s = +s) ? c : a(i === 0 ? 0.5 : (s = (u(s) - t) * i, o ? Math.max(0, Math.min(1, s)) : s));
  }
  f.domain = function(s) {
    return arguments.length ? ([n, e] = s, t = u(n = +n), r = u(e = +e), i = t === r ? 0 : 1 / (r - t), f) : [n, e];
  }, f.clamp = function(s) {
    return arguments.length ? (o = !!s, f) : o;
  }, f.interpolator = function(s) {
    return arguments.length ? (a = s, f) : a;
  };
  function l(s) {
    return function(h) {
      var g, d;
      return arguments.length ? ([g, d] = h, a = s(g, d), f) : [a(0), a(1)];
    };
  }
  return f.range = l(ge), f.rangeRound = l(xr), f.unknown = function(s) {
    return arguments.length ? (c = s, f) : c;
  }, function(s) {
    return u = s, t = s(n), r = s(e), i = t === r ? 0 : 1 / (r - t), f;
  };
}
function ee(n, e) {
  return e.domain(n.domain()).interpolator(n.interpolator()).clamp(n.clamp()).unknown(n.unknown());
}
function uu() {
  var n = de(Nr()(on));
  return n.copy = function() {
    return ee(n, uu());
  }, Kn.apply(n, arguments);
}
function Uf() {
  var n = Gi(Nr()).domain([1, 10]);
  return n.copy = function() {
    return ee(n, Uf()).base(n.base());
  }, Kn.apply(n, arguments);
}
function Ef() {
  var n = Zi(Nr());
  return n.copy = function() {
    return ee(n, Ef()).constant(n.constant());
  }, Kn.apply(n, arguments);
}
function au() {
  var n = Qi(Nr());
  return n.copy = function() {
    return ee(n, au()).exponent(n.exponent());
  }, Kn.apply(n, arguments);
}
function Y1() {
  return au.apply(null, arguments).exponent(0.5);
}
function Dr() {
  var n = 0, e = 0.5, t = 1, r = 1, i, u, a, o, c, f = on, l, s = !1, h;
  function g(p) {
    return isNaN(p = +p) ? h : (p = 0.5 + ((p = +l(p)) - u) * (r * p < r * u ? o : c), f(s ? Math.max(0, Math.min(1, p)) : p));
  }
  g.domain = function(p) {
    return arguments.length ? ([n, e, t] = p, i = l(n = +n), u = l(e = +e), a = l(t = +t), o = i === u ? 0 : 0.5 / (u - i), c = u === a ? 0 : 0.5 / (a - u), r = u < i ? -1 : 1, g) : [n, e, t];
  }, g.clamp = function(p) {
    return arguments.length ? (s = !!p, g) : s;
  }, g.interpolator = function(p) {
    return arguments.length ? (f = p, g) : f;
  };
  function d(p) {
    return function(m) {
      var M, x, b;
      return arguments.length ? ([M, x, b] = m, f = Xi(p, [M, x, b]), g) : [f(0), f(0.5), f(1)];
    };
  }
  return g.range = d(ge), g.rangeRound = d(xr), g.unknown = function(p) {
    return arguments.length ? (h = p, g) : h;
  }, function(p) {
    return l = p, i = p(n), u = p(e), a = p(t), o = i === u ? 0 : 0.5 / (u - i), c = u === a ? 0 : 0.5 / (a - u), r = u < i ? -1 : 1, g;
  };
}
function Ff() {
  var n = de(Dr()(on));
  return n.copy = function() {
    return ee(n, Ff());
  }, Kn.apply(n, arguments);
}
function Af() {
  var n = Gi(Dr()).domain([0.1, 1, 10]);
  return n.copy = function() {
    return ee(n, Af()).base(n.base());
  }, Kn.apply(n, arguments);
}
function kf() {
  var n = Zi(Dr());
  return n.copy = function() {
    return ee(n, kf()).constant(n.constant());
  }, Kn.apply(n, arguments);
}
function ou() {
  var n = Qi(Dr());
  return n.copy = function() {
    return ee(n, ou()).exponent(n.exponent());
  }, Kn.apply(n, arguments);
}
function R1() {
  return ou.apply(null, arguments).exponent(0.5);
}
function Yn(n) {
  for (var e = n.length / 6 | 0, t = new Array(e), r = 0; r < e; ) t[r] = "#" + n.slice(r * 6, ++r * 6);
  return t;
}
const q1 = Yn("1f77b4ff7f0e2ca02cd627289467bd8c564be377c27f7f7fbcbd2217becf"), P1 = Yn("7fc97fbeaed4fdc086ffff99386cb0f0027fbf5b17666666"), I1 = Yn("1b9e77d95f027570b3e7298a66a61ee6ab02a6761d666666"), H1 = Yn("4269d0efb118ff725c6cc5b03ca951ff8ab7a463f297bbf59c6b4e9498a0"), L1 = Yn("a6cee31f78b4b2df8a33a02cfb9a99e31a1cfdbf6fff7f00cab2d66a3d9affff99b15928"), O1 = Yn("fbb4aeb3cde3ccebc5decbe4fed9a6ffffcce5d8bdfddaecf2f2f2"), z1 = Yn("b3e2cdfdcdaccbd5e8f4cae4e6f5c9fff2aef1e2cccccccc"), W1 = Yn("e41a1c377eb84daf4a984ea3ff7f00ffff33a65628f781bf999999"), X1 = Yn("66c2a5fc8d628da0cbe78ac3a6d854ffd92fe5c494b3b3b3"), B1 = Yn("8dd3c7ffffb3bebadafb807280b1d3fdb462b3de69fccde5d9d9d9bc80bdccebc5ffed6f");
function Le(n, e, t) {
  return n.fields = e || [], n.fname = t, n;
}
function j1(n) {
  return n.length === 1 ? G1(n[0]) : Z1(n);
}
const G1 = (n) => function(e) {
  return e[n];
}, Z1 = (n) => {
  const e = n.length;
  return function(t) {
    for (let r = 0; r < e; ++r)
      t = t[n[r]];
    return t;
  };
};
function Ce(n) {
  throw Error(n);
}
function Q1(n) {
  const e = [], t = n.length;
  let r = null, i = 0, u = "", a, o, c;
  n = n + "";
  function f() {
    e.push(u + n.substring(a, o)), u = "", a = o + 1;
  }
  for (a = o = 0; o < t; ++o)
    if (c = n[o], c === "\\")
      u += n.substring(a, o++), a = o;
    else if (c === r)
      f(), r = null, i = -1;
    else {
      if (r)
        continue;
      a === i && c === '"' || a === i && c === "'" ? (a = o + 1, r = c) : c === "." && !i ? o > a ? f() : a = o + 1 : c === "[" ? (o > a && f(), i = a = o + 1) : c === "]" && (i || Ce("Access path missing open bracket: " + n), i > 0 && f(), i = 0, a = o + 1);
    }
  return i && Ce("Access path missing closing bracket: " + n), r && Ce("Access path missing closing quote: " + n), o > a && (o++, f()), e;
}
function V1(n, e, t) {
  const r = Q1(n);
  return n = r.length === 1 ? r[0] : n, Le(j1(r), [n], n);
}
V1("id");
Le((n) => n, [], "identity");
const Ge = Le(() => 0, [], "zero"), J1 = Le(() => 1, [], "one");
Le(() => !0, [], "true");
Le(() => !1, [], "false");
var _1 = Array.isArray;
function Yf(n) {
  return n[n.length - 1];
}
function K1(n) {
  return n != null ? _1(n) ? n : [n] : [];
}
function nh(n) {
  return typeof n == "function";
}
function eh(n) {
  return nh(n) ? n : () => n;
}
function th(n) {
  for (let e, t, r = 1, i = arguments.length; r < i; ++r) {
    e = arguments[r];
    for (t in e)
      n[t] = e[t];
  }
  return n;
}
const rh = Object.prototype.hasOwnProperty;
function ih(n, e) {
  return rh.call(n, e);
}
function uh(n) {
  return n && Yf(n) - n[0] || 0;
}
function ah(n) {
  const e = {}, t = n.length;
  for (let r = 0; r < t; ++r) e[n[r]] = !0;
  return e;
}
const jr = /* @__PURE__ */ new Date(), Gr = /* @__PURE__ */ new Date();
function J(n, e, t, r) {
  function i(u) {
    return n(u = arguments.length === 0 ? /* @__PURE__ */ new Date() : /* @__PURE__ */ new Date(+u)), u;
  }
  return i.floor = (u) => (n(u = /* @__PURE__ */ new Date(+u)), u), i.ceil = (u) => (n(u = new Date(u - 1)), e(u, 1), n(u), u), i.round = (u) => {
    const a = i(u), o = i.ceil(u);
    return u - a < o - u ? a : o;
  }, i.offset = (u, a) => (e(u = /* @__PURE__ */ new Date(+u), a == null ? 1 : Math.floor(a)), u), i.range = (u, a, o) => {
    const c = [];
    if (u = i.ceil(u), o = o == null ? 1 : Math.floor(o), !(u < a) || !(o > 0)) return c;
    let f;
    do
      c.push(f = /* @__PURE__ */ new Date(+u)), e(u, o), n(u);
    while (f < u && u < a);
    return c;
  }, i.filter = (u) => J((a) => {
    if (a >= a) for (; n(a), !u(a); ) a.setTime(a - 1);
  }, (a, o) => {
    if (a >= a)
      if (o < 0) for (; ++o <= 0; )
        for (; e(a, -1), !u(a); )
          ;
      else for (; --o >= 0; )
        for (; e(a, 1), !u(a); )
          ;
  }), t && (i.count = (u, a) => (jr.setTime(+u), Gr.setTime(+a), n(jr), n(Gr), Math.floor(t(jr, Gr))), i.every = (u) => (u = Math.floor(u), !isFinite(u) || !(u > 0) ? null : u > 1 ? i.filter(r ? (a) => r(a) % u === 0 : (a) => i.count(0, a) % u === 0) : i)), i;
}
const vt = J(() => {
}, (n, e) => {
  n.setTime(+n + e);
}, (n, e) => e - n);
vt.every = (n) => (n = Math.floor(n), !isFinite(n) || !(n > 0) ? null : n > 1 ? J((e) => {
  e.setTime(Math.floor(e / n) * n);
}, (e, t) => {
  e.setTime(+e + t * n);
}, (e, t) => (t - e) / n) : vt);
vt.range;
const wt = 1e3, Jn = wt * 60, xt = Jn * 60, Tt = xt * 24, Rf = Tt * 7, fu = J((n) => {
  n.setTime(n - n.getMilliseconds());
}, (n, e) => {
  n.setTime(+n + e * wt);
}, (n, e) => (e - n) / wt, (n) => n.getUTCSeconds());
fu.range;
const qf = J((n) => {
  n.setTime(n - n.getMilliseconds() - n.getSeconds() * wt);
}, (n, e) => {
  n.setTime(+n + e * Jn);
}, (n, e) => (e - n) / Jn, (n) => n.getMinutes());
qf.range;
const Pf = J((n) => {
  n.setUTCSeconds(0, 0);
}, (n, e) => {
  n.setTime(+n + e * Jn);
}, (n, e) => (e - n) / Jn, (n) => n.getUTCMinutes());
Pf.range;
const If = J((n) => {
  n.setTime(n - n.getMilliseconds() - n.getSeconds() * wt - n.getMinutes() * Jn);
}, (n, e) => {
  n.setTime(+n + e * xt);
}, (n, e) => (e - n) / xt, (n) => n.getHours());
If.range;
const Hf = J((n) => {
  n.setUTCMinutes(0, 0, 0);
}, (n, e) => {
  n.setTime(+n + e * xt);
}, (n, e) => (e - n) / xt, (n) => n.getUTCHours());
Hf.range;
const lt = J(
  (n) => n.setHours(0, 0, 0, 0),
  (n, e) => n.setDate(n.getDate() + e),
  (n, e) => (e - n - (e.getTimezoneOffset() - n.getTimezoneOffset()) * Jn) / Tt,
  (n) => n.getDate() - 1
);
lt.range;
const st = J((n) => {
  n.setUTCHours(0, 0, 0, 0);
}, (n, e) => {
  n.setUTCDate(n.getUTCDate() + e);
}, (n, e) => (e - n) / Tt, (n) => n.getUTCDate() - 1);
st.range;
const oh = J((n) => {
  n.setUTCHours(0, 0, 0, 0);
}, (n, e) => {
  n.setUTCDate(n.getUTCDate() + e);
}, (n, e) => (e - n) / Tt, (n) => Math.floor(n / Tt));
oh.range;
function be(n) {
  return J((e) => {
    e.setDate(e.getDate() - (e.getDay() + 7 - n) % 7), e.setHours(0, 0, 0, 0);
  }, (e, t) => {
    e.setDate(e.getDate() + t * 7);
  }, (e, t) => (t - e - (t.getTimezoneOffset() - e.getTimezoneOffset()) * Jn) / Rf);
}
const cu = be(0), fh = be(1), ch = be(2), lh = be(3), sh = be(4), hh = be(5), gh = be(6);
cu.range;
fh.range;
ch.range;
lh.range;
sh.range;
hh.range;
gh.range;
function ye(n) {
  return J((e) => {
    e.setUTCDate(e.getUTCDate() - (e.getUTCDay() + 7 - n) % 7), e.setUTCHours(0, 0, 0, 0);
  }, (e, t) => {
    e.setUTCDate(e.getUTCDate() + t * 7);
  }, (e, t) => (t - e) / Rf);
}
const lu = ye(0), dh = ye(1), ph = ye(2), mh = ye(3), bh = ye(4), yh = ye(5), Mh = ye(6);
lu.range;
dh.range;
ph.range;
mh.range;
bh.range;
yh.range;
Mh.range;
const Si = J((n) => {
  n.setDate(1), n.setHours(0, 0, 0, 0);
}, (n, e) => {
  n.setMonth(n.getMonth() + e);
}, (n, e) => e.getMonth() - n.getMonth() + (e.getFullYear() - n.getFullYear()) * 12, (n) => n.getMonth());
Si.range;
const $i = J((n) => {
  n.setUTCDate(1), n.setUTCHours(0, 0, 0, 0);
}, (n, e) => {
  n.setUTCMonth(n.getUTCMonth() + e);
}, (n, e) => e.getUTCMonth() - n.getUTCMonth() + (e.getUTCFullYear() - n.getUTCFullYear()) * 12, (n) => n.getUTCMonth());
$i.range;
const su = J((n) => {
  n.setMonth(0, 1), n.setHours(0, 0, 0, 0);
}, (n, e) => {
  n.setFullYear(n.getFullYear() + e);
}, (n, e) => e.getFullYear() - n.getFullYear(), (n) => n.getFullYear());
su.every = (n) => !isFinite(n = Math.floor(n)) || !(n > 0) ? null : J((e) => {
  e.setFullYear(Math.floor(e.getFullYear() / n) * n), e.setMonth(0, 1), e.setHours(0, 0, 0, 0);
}, (e, t) => {
  e.setFullYear(e.getFullYear() + t * n);
});
su.range;
const hu = J((n) => {
  n.setUTCMonth(0, 1), n.setUTCHours(0, 0, 0, 0);
}, (n, e) => {
  n.setUTCFullYear(n.getUTCFullYear() + e);
}, (n, e) => e.getUTCFullYear() - n.getUTCFullYear(), (n) => n.getUTCFullYear());
hu.every = (n) => !isFinite(n = Math.floor(n)) || !(n > 0) ? null : J((e) => {
  e.setUTCFullYear(Math.floor(e.getUTCFullYear() / n) * n), e.setUTCMonth(0, 1), e.setUTCHours(0, 0, 0, 0);
}, (e, t) => {
  e.setUTCFullYear(e.getUTCFullYear() + t * n);
});
hu.range;
const fn = "year", Sn = "quarter", hn = "month", rn = "week", $n = "date", an = "day", Bn = "dayofyear", En = "hours", Fn = "minutes", jn = "seconds", Gn = "milliseconds", vh = [fn, Sn, hn, rn, $n, an, Bn, En, Fn, jn, Gn], Zr = vh.reduce((n, e, t) => (n[e] = 1 + t, n), {});
function wh(n) {
  const e = K1(n).slice(), t = {};
  return e.length || Ce("Missing time unit."), e.forEach((i) => {
    ih(Zr, i) ? t[i] = 1 : Ce(`Invalid time unit: ${i}.`);
  }), (t[rn] || t[an] ? 1 : 0) + (t[Sn] || t[hn] || t[$n] ? 1 : 0) + (t[Bn] ? 1 : 0) > 1 && Ce(`Incompatible time units: ${n}`), e.sort((i, u) => Zr[i] - Zr[u]), e;
}
const xh = {
  [fn]: "%Y ",
  [Sn]: "Q%q ",
  [hn]: "%b ",
  [$n]: "%d ",
  [rn]: "W%U ",
  [an]: "%a ",
  [Bn]: "%j ",
  [En]: "%H:00",
  [Fn]: "00:%M",
  [jn]: ":%S",
  [Gn]: ".%L",
  [`${fn}-${hn}`]: "%Y-%m ",
  [`${fn}-${hn}-${$n}`]: "%Y-%m-%d ",
  [`${En}-${Fn}`]: "%H:%M"
};
function Jg(n, e) {
  const t = th({}, xh, e), r = wh(n), i = r.length;
  let u = "", a = 0, o, c;
  for (a = 0; a < i; )
    for (o = r.length; o > a; --o)
      if (c = r.slice(a, o).join("-"), t[c] != null) {
        u += t[c], a = o;
        break;
      }
  return u.trim();
}
const ie = /* @__PURE__ */ new Date();
function gu(n) {
  return ie.setFullYear(n), ie.setMonth(0), ie.setDate(1), ie.setHours(0, 0, 0, 0), ie;
}
function _g(n) {
  return Lf(new Date(n));
}
function Kg(n) {
  return Ci(new Date(n));
}
function Lf(n) {
  return lt.count(gu(n.getFullYear()) - 1, n);
}
function Ci(n) {
  return cu.count(gu(n.getFullYear()) - 1, n);
}
function Ni(n) {
  return gu(n).getDay();
}
function Th(n, e, t, r, i, u, a) {
  if (0 <= n && n < 100) {
    const o = new Date(-1, e, t, r, i, u, a);
    return o.setFullYear(n), o;
  }
  return new Date(n, e, t, r, i, u, a);
}
function nd(n) {
  return Of(new Date(n));
}
function ed(n) {
  return Di(new Date(n));
}
function Of(n) {
  const e = Date.UTC(n.getUTCFullYear(), 0, 1);
  return st.count(e - 1, n);
}
function Di(n) {
  const e = Date.UTC(n.getUTCFullYear(), 0, 1);
  return lu.count(e - 1, n);
}
function Ui(n) {
  return ie.setTime(Date.UTC(n, 0, 1)), ie.getUTCDay();
}
function Sh(n, e, t, r, i, u, a) {
  if (0 <= n && n < 100) {
    const o = new Date(Date.UTC(-1, e, t, r, i, u, a));
    return o.setUTCFullYear(t.y), o;
  }
  return new Date(Date.UTC(n, e, t, r, i, u, a));
}
function zf(n, e, t, r, i) {
  const u = e || 1, a = Yf(n), o = (M, x, b) => (b = b || M, $h(t[b], r[b], M === a && u, x)), c = /* @__PURE__ */ new Date(), f = ah(n), l = f[fn] ? o(fn) : eh(2012), s = f[hn] ? o(hn) : f[Sn] ? o(Sn) : Ge, h = f[rn] && f[an] ? o(an, 1, rn + an) : f[rn] ? o(rn, 1) : f[an] ? o(an, 1) : f[$n] ? o($n, 1) : f[Bn] ? o(Bn, 1) : J1, g = f[En] ? o(En) : Ge, d = f[Fn] ? o(Fn) : Ge, p = f[jn] ? o(jn) : Ge, m = f[Gn] ? o(Gn) : Ge;
  return function(M) {
    c.setTime(+M);
    const x = l(c);
    return i(x, s(c), h(c, x), g(c), d(c), p(c), m(c));
  };
}
function $h(n, e, t, r) {
  const i = t <= 1 ? n : r ? (u, a) => r + t * Math.floor((n(u, a) - r) / t) : (u, a) => t * Math.floor(n(u, a) / t);
  return e ? (u, a) => e(i(u, a), a) : i;
}
function ke(n, e, t) {
  return e + n * 7 - (t + 6) % 7;
}
const Ch = {
  [fn]: (n) => n.getFullYear(),
  [Sn]: (n) => Math.floor(n.getMonth() / 3),
  [hn]: (n) => n.getMonth(),
  [$n]: (n) => n.getDate(),
  [En]: (n) => n.getHours(),
  [Fn]: (n) => n.getMinutes(),
  [jn]: (n) => n.getSeconds(),
  [Gn]: (n) => n.getMilliseconds(),
  [Bn]: (n) => Lf(n),
  [rn]: (n) => Ci(n),
  [rn + an]: (n, e) => ke(Ci(n), n.getDay(), Ni(e)),
  [an]: (n, e) => ke(1, n.getDay(), Ni(e))
}, Nh = {
  [Sn]: (n) => 3 * n,
  [rn]: (n, e) => ke(n, 0, Ni(e))
};
function td(n, e) {
  return zf(n, e || 1, Ch, Nh, Th);
}
const Dh = {
  [fn]: (n) => n.getUTCFullYear(),
  [Sn]: (n) => Math.floor(n.getUTCMonth() / 3),
  [hn]: (n) => n.getUTCMonth(),
  [$n]: (n) => n.getUTCDate(),
  [En]: (n) => n.getUTCHours(),
  [Fn]: (n) => n.getUTCMinutes(),
  [jn]: (n) => n.getUTCSeconds(),
  [Gn]: (n) => n.getUTCMilliseconds(),
  [Bn]: (n) => Of(n),
  [rn]: (n) => Di(n),
  [an]: (n, e) => ke(1, n.getUTCDay(), Ui(e)),
  [rn + an]: (n, e) => ke(Di(n), n.getUTCDay(), Ui(e))
}, Uh = {
  [Sn]: (n) => 3 * n,
  [rn]: (n, e) => ke(n, 0, Ui(e))
};
function rd(n, e) {
  return zf(n, e || 1, Dh, Uh, Sh);
}
const Eh = {
  [fn]: su,
  [Sn]: Si.every(3),
  [hn]: Si,
  [rn]: cu,
  [$n]: lt,
  [an]: lt,
  [Bn]: lt,
  [En]: If,
  [Fn]: qf,
  [jn]: fu,
  [Gn]: vt
}, Fh = {
  [fn]: hu,
  [Sn]: $i.every(3),
  [hn]: $i,
  [rn]: lu,
  [$n]: st,
  [an]: st,
  [Bn]: st,
  [En]: Hf,
  [Fn]: Pf,
  [jn]: fu,
  [Gn]: vt
};
function du(n) {
  return Eh[n];
}
function pu(n) {
  return Fh[n];
}
function Wf(n, e, t) {
  return n ? n.offset(e, t) : void 0;
}
function id(n, e, t) {
  return Wf(du(n), e, t);
}
function ud(n, e, t) {
  return Wf(pu(n), e, t);
}
function Xf(n, e, t, r) {
  return n ? n.range(e, t, r) : void 0;
}
function ad(n, e, t, r) {
  return Xf(du(n), e, t, r);
}
function od(n, e, t, r) {
  return Xf(pu(n), e, t, r);
}
const nt = 1e3, et = nt * 60, tt = et * 60, Ur = tt * 24, Ah = Ur * 7, Ra = Ur * 30, Ei = Ur * 365, Bf = [fn, hn, $n, En, Fn, jn, Gn], rt = Bf.slice(0, -1), it = rt.slice(0, -1), ut = it.slice(0, -1), kh = ut.slice(0, -1), Yh = [fn, rn], qa = [fn, hn], jf = [fn], Ze = [[rt, 1, nt], [rt, 5, 5 * nt], [rt, 15, 15 * nt], [rt, 30, 30 * nt], [it, 1, et], [it, 5, 5 * et], [it, 15, 15 * et], [it, 30, 30 * et], [ut, 1, tt], [ut, 3, 3 * tt], [ut, 6, 6 * tt], [ut, 12, 12 * tt], [kh, 1, Ur], [Yh, 1, Ah], [qa, 1, Ra], [qa, 3, 3 * Ra], [jf, 1, Ei]];
function fd(n) {
  const e = n.extent, t = n.maxbins || 40, r = Math.abs(uh(e)) / t;
  let i = dr((o) => o[2]).right(Ze, r), u, a;
  return i === Ze.length ? (u = jf, a = ht(e[0] / Ei, e[1] / Ei, t)) : i ? (i = Ze[r / Ze[i - 1][2] < Ze[i][2] / r ? i - 1 : i], u = i[0], a = i[1]) : (u = Bf, a = Math.max(ht(e[0], e[1], t), 1)), {
    units: u,
    step: a
  };
}
function Rh(n, e, t) {
  const r = n - e + t * 2;
  return n ? r > 0 ? r : 1 : 0;
}
const qh = "identity", mu = "linear", _n = "log", bu = "pow", yu = "sqrt", Mu = "symlog", Ye = "time", Re = "utc", Oe = "sequential", Ft = "diverging", St = "quantile", vu = "quantize", wu = "threshold", Ph = "ordinal", Ih = "point", Hh = "band", Lh = "bin-ordinal", _ = "continuous", At = "discrete", kt = "discretizing", Mn = "interpolating", xu = "temporal";
function Oh(n) {
  return function(e) {
    let t = e[0], r = e[1], i;
    return r < t && (i = t, t = r, r = i), [n.invert(t), n.invert(r)];
  };
}
function zh(n) {
  return function(e) {
    const t = n.range();
    let r = e[0], i = e[1], u = -1, a, o, c, f;
    for (i < r && (o = r, r = i, i = o), c = 0, f = t.length; c < f; ++c)
      t[c] >= r && t[c] <= i && (u < 0 && (u = c), a = c);
    if (!(u < 0))
      return r = n.invertExtent(t[u]), i = n.invertExtent(t[a]), [r[0] === void 0 ? r[1] : r[0], i[1] === void 0 ? i[0] : i[1]];
  };
}
function Tu() {
  const n = Hi().unknown(void 0), e = n.domain, t = n.range;
  let r = [0, 1], i, u, a = !1, o = 0, c = 0, f = 0.5;
  delete n.unknown;
  function l() {
    const s = e().length, h = r[1] < r[0], g = r[1 - h], d = Rh(s, o, c);
    let p = r[h - 0];
    i = (g - p) / (d || 1), a && (i = Math.floor(i)), p += (g - p - i * (s - o)) * f, u = i * (1 - o), a && (p = Math.round(p), u = Math.round(u));
    const m = xc(s).map((M) => p + i * M);
    return t(h ? m.reverse() : m);
  }
  return n.domain = function(s) {
    return arguments.length ? (e(s), l()) : e();
  }, n.range = function(s) {
    return arguments.length ? (r = [+s[0], +s[1]], l()) : r.slice();
  }, n.rangeRound = function(s) {
    return r = [+s[0], +s[1]], a = !0, l();
  }, n.bandwidth = function() {
    return u;
  }, n.step = function() {
    return i;
  }, n.round = function(s) {
    return arguments.length ? (a = !!s, l()) : a;
  }, n.padding = function(s) {
    return arguments.length ? (c = Math.max(0, Math.min(1, s)), o = c, l()) : o;
  }, n.paddingInner = function(s) {
    return arguments.length ? (o = Math.max(0, Math.min(1, s)), l()) : o;
  }, n.paddingOuter = function(s) {
    return arguments.length ? (c = Math.max(0, Math.min(1, s)), l()) : c;
  }, n.align = function(s) {
    return arguments.length ? (f = Math.max(0, Math.min(1, s)), l()) : f;
  }, n.invertRange = function(s) {
    if (s[0] == null || s[1] == null) return;
    const h = r[1] < r[0], g = h ? t().reverse() : t(), d = g.length - 1;
    let p = +s[0], m = +s[1], M, x, b;
    if (!(p !== p || m !== m) && (m < p && (b = p, p = m, m = b), !(m < g[0] || p > r[1 - h])))
      return M = Math.max(0, ce(g, p) - 1), x = p === m ? M : ce(g, m) - 1, p - g[M] > u + 1e-10 && ++M, h && (b = M, M = d - x, x = d - b), M > x ? void 0 : e().slice(M, x + 1);
  }, n.invert = function(s) {
    const h = n.invertRange([s, s]);
    return h && h[0];
  }, n.copy = function() {
    return Tu().domain(e()).range(r).round(a).paddingInner(o).paddingOuter(c).align(f);
  }, l();
}
function Gf(n) {
  const e = n.copy;
  return n.padding = n.paddingOuter, delete n.paddingInner, n.copy = function() {
    return Gf(e());
  }, n;
}
function Wh() {
  return Gf(Tu().paddingInner(1));
}
var Xh = Array.prototype.map;
function Bh(n) {
  return Xh.call(n, t0);
}
const jh = Array.prototype.slice;
function Zf() {
  let n = [], e = [];
  function t(r) {
    return r == null || r !== r ? void 0 : e[(ce(n, r) - 1) % e.length];
  }
  return t.domain = function(r) {
    return arguments.length ? (n = Bh(r), t) : n.slice();
  }, t.range = function(r) {
    return arguments.length ? (e = jh.call(r), t) : e.slice();
  }, t.tickFormat = function(r, i) {
    return hf(n[0], Vn(n), r ?? 10, i);
  }, t.copy = function() {
    return Zf().domain(t.domain()).range(t.range());
  }, t;
}
const hr = /* @__PURE__ */ new Map(), Qf = Symbol("vega_scale");
function Vf(n) {
  return n[Qf] = !0, n;
}
function cd(n) {
  return n && n[Qf] === !0;
}
function Gh(n, e, t) {
  const r = function() {
    const u = e();
    return u.invertRange || (u.invertRange = u.invert ? Oh(u) : u.invertExtent ? zh(u) : void 0), u.type = n, Vf(u);
  };
  return r.metadata = f0(r0(t)), r;
}
function W(n, e, t) {
  return arguments.length > 1 ? (hr.set(n, Gh(n, e, t)), this) : Zh(n) ? hr.get(n) : void 0;
}
W(qh, df);
W(mu, gf, _);
W(_n, mf, [_, _n]);
W(bu, Vi, _);
W(yu, ms, _);
W(Mu, bf, _);
W(Ye, A1, [_, xu]);
W(Re, k1, [_, xu]);
W(Oe, uu, [_, Mn]);
W(`${Oe}-${mu}`, uu, [_, Mn]);
W(`${Oe}-${_n}`, Uf, [_, Mn, _n]);
W(`${Oe}-${bu}`, au, [_, Mn]);
W(`${Oe}-${yu}`, Y1, [_, Mn]);
W(`${Oe}-${Mu}`, Ef, [_, Mn]);
W(`${Ft}-${mu}`, Ff, [_, Mn]);
W(`${Ft}-${_n}`, Af, [_, Mn, _n]);
W(`${Ft}-${bu}`, ou, [_, Mn]);
W(`${Ft}-${yu}`, R1, [_, Mn]);
W(`${Ft}-${Mu}`, kf, [_, Mn]);
W(St, yf, [kt, St]);
W(vu, Mf, kt);
W(wu, vf, kt);
W(Lh, Zf, [At, kt]);
W(Ph, Hi, At);
W(Hh, Tu, At);
W(Ih, Wh, At);
function Zh(n) {
  return hr.has(n);
}
function Me(n, e) {
  const t = hr.get(n);
  return t && t.metadata[e];
}
function ld(n) {
  return Me(n, _);
}
function Qh(n) {
  return Me(n, At);
}
function Vh(n) {
  return Me(n, kt);
}
function Jh(n) {
  return Me(n, _n);
}
function _h(n) {
  return Me(n, xu);
}
function sd(n) {
  return Me(n, Mn);
}
function hd(n) {
  return Me(n, St);
}
const Kh = ["clamp", "base", "constant", "exponent"];
function gd(n, e) {
  const t = e[0], r = Vn(e) - t;
  return function(i) {
    return n(t + i * r);
  };
}
function ng(n, e, t) {
  return Xi(eg(e || "rgb", t), n);
}
function dd(n, e) {
  const t = new Array(e), r = e + 1;
  for (let i = 0; i < e; ) t[i] = n(++i / r);
  return t;
}
function pd(n, e, t) {
  const r = t - e;
  let i, u, a;
  return !r || !Number.isFinite(r) ? u0(0.5) : (i = (u = n.type).indexOf("-"), u = i < 0 ? u : u.slice(i + 1), a = W(u)().domain([e, t]).range([0, 1]), Kh.forEach((o) => n[o] ? a[o](n[o]()) : 0), a);
}
function eg(n, e) {
  const t = G0[tg(n)];
  return e != null && t && t.gamma ? t.gamma(e) : t;
}
function tg(n) {
  return "interpolate" + n.toLowerCase().split("-").map((e) => e[0].toUpperCase() + e.slice(1)).join("");
}
const rg = {
  blues: "cfe1f2bed8eca8cee58fc1de74b2d75ba3cf4592c63181bd206fb2125ca40a4a90",
  greens: "d3eecdc0e6baabdda594d3917bc77d60ba6c46ab5e329a512089430e7735036429",
  greys: "e2e2e2d4d4d4c4c4c4b1b1b19d9d9d8888887575756262624d4d4d3535351e1e1e",
  oranges: "fdd8b3fdc998fdb87bfda55efc9244f87f2cf06b18e4580bd14904b93d029f3303",
  purples: "e2e1efd4d4e8c4c5e0b4b3d6a3a0cc928ec3827cb97566ae684ea25c3696501f8c",
  reds: "fdc9b4fcb49afc9e80fc8767fa7051f6573fec3f2fdc2a25c81b1db21218970b13",
  blueGreen: "d5efedc1e8e0a7ddd18bd2be70c6a958ba9144ad77319c5d2089460e7736036429",
  bluePurple: "ccddecbad0e4a8c2dd9ab0d4919cc98d85be8b6db28a55a6873c99822287730f71",
  greenBlue: "d3eecec5e8c3b1e1bb9bd8bb82cec269c2ca51b2cd3c9fc7288abd1675b10b60a1",
  orangeRed: "fddcaffdcf9bfdc18afdad77fb9562f67d53ee6545e24932d32d1ebf130da70403",
  purpleBlue: "dbdaebc8cee4b1c3de97b7d87bacd15b9fc93a90c01e7fb70b70ab056199045281",
  purpleBlueGreen: "dbd8eac8cee4b0c3de93b7d872acd1549fc83892bb1c88a3097f8702736b016353",
  purpleRed: "dcc9e2d3b3d7ce9eccd186c0da6bb2e14da0e23189d91e6fc61159ab07498f023a",
  redPurple: "fccfccfcbec0faa9b8f98faff571a5ec539ddb3695c41b8aa908808d0179700174",
  yellowGreen: "e4f4acd1eca0b9e2949ed68880c97c62bb6e47aa5e3297502083440e723b036034",
  yellowOrangeBrown: "feeaa1fedd84fecc63feb746fca031f68921eb7215db5e0bc54c05ab3d038f3204",
  yellowOrangeRed: "fee087fed16ffebd59fea849fd903efc7335f9522bee3423de1b20ca0b22af0225",
  blueOrange: "134b852f78b35da2cb9dcae1d2e5eff2f0ebfce0bafbbf74e8932fc5690d994a07",
  brownBlueGreen: "704108a0651ac79548e3c78af3e6c6eef1eac9e9e48ed1c74da79e187a72025147",
  purpleGreen: "5b1667834792a67fb6c9aed3e6d6e8eff0efd9efd5aedda971bb75368e490e5e29",
  purpleOrange: "4114696647968f83b7b9b4d6dadbebf3eeeafce0bafbbf74e8932fc5690d994a07",
  redBlue: "8c0d25bf363adf745ef4ae91fbdbc9f2efeed2e5ef9dcae15da2cb2f78b3134b85",
  redGrey: "8c0d25bf363adf745ef4ae91fcdccbfaf4f1e2e2e2c0c0c0969696646464343434",
  yellowGreenBlue: "eff9bddbf1b4bde5b594d5b969c5be45b4c22c9ec02182b82163aa23479c1c3185",
  redYellowBlue: "a50026d4322cf16e43fcac64fedd90faf8c1dcf1ecabd6e875abd04a74b4313695",
  redYellowGreen: "a50026d4322cf16e43fcac63fedd8df9f7aed7ee8ea4d86e64bc6122964f006837",
  pinkYellowGreen: "8e0152c0267edd72adf0b3d6faddedf5f3efe1f2cab6de8780bb474f9125276419",
  spectral: "9e0142d13c4bf0704afcac63fedd8dfbf8b0e0f3a1a9dda269bda94288b55e4fa2",
  viridis: "440154470e61481a6c482575472f7d443a834144873d4e8a39568c35608d31688e2d708e2a788e27818e23888e21918d1f988b1fa08822a8842ab07f35b77943bf7154c56866cc5d7ad1518fd744a5db36bcdf27d2e21be9e51afde725",
  magma: "0000040404130b0924150e3720114b2c11603b0f704a107957157e651a80721f817f24828c29819a2e80a8327db6377ac43c75d1426fde4968e95462f1605df76f5cfa7f5efc8f65fe9f6dfeaf78febf84fece91fddea0fcedaffcfdbf",
  inferno: "0000040403130c0826170c3b240c4f330a5f420a68500d6c5d126e6b176e781c6d86216b932667a12b62ae305cbb3755c73e4cd24644dd513ae65c30ed6925f3771af8850ffb9506fca50afcb519fac62df6d645f2e661f3f484fcffa4",
  plasma: "0d088723069033059742039d5002a25d01a66a00a87801a88405a7900da49c179ea72198b12a90ba3488c33d80cb4779d35171da5a69e16462e76e5bed7953f2834cf68f44fa9a3dfca636fdb32ffec029fcce25f9dc24f5ea27f0f921",
  cividis: "00205100235800265d002961012b65042e670831690d346b11366c16396d1c3c6e213f6e26426e2c456e31476e374a6e3c4d6e42506e47536d4c566d51586e555b6e5a5e6e5e616e62646f66676f6a6a706e6d717270717573727976737c79747f7c75827f758682768985778c8877908b78938e789691789a94789e9778a19b78a59e77a9a177aea575b2a874b6ab73bbaf71c0b26fc5b66dc9b96acebd68d3c065d8c462ddc85fe2cb5ce7cf58ebd355f0d652f3da4ff7de4cfae249fce647",
  rainbow: "6e40aa883eb1a43db3bf3cafd83fa4ee4395fe4b83ff576eff6659ff7847ff8c38f3a130e2b72fcfcc36bee044aff05b8ff4576ff65b52f6673af27828ea8d1ddfa319d0b81cbecb23abd82f96e03d82e14c6edb5a5dd0664dbf6e40aa",
  sinebow: "ff4040fc582af47218e78d0bd5a703bfbf00a7d5038de70b72f41858fc2a40ff402afc5818f4720be78d03d5a700bfbf03a7d50b8de71872f42a58fc4040ff582afc7218f48d0be7a703d5bf00bfd503a7e70b8df41872fc2a58ff4040",
  turbo: "23171b32204a3e2a71453493493eae4b49c54a53d7485ee44569ee4074f53c7ff8378af93295f72e9ff42ba9ef28b3e926bce125c5d925cdcf27d5c629dcbc2de3b232e9a738ee9d3ff39347f68950f9805afc7765fd6e70fe667cfd5e88fc5795fb51a1f84badf545b9f140c5ec3cd0e637dae034e4d931ecd12ef4c92bfac029ffb626ffad24ffa223ff9821ff8d1fff821dff771cfd6c1af76118f05616e84b14df4111d5380fcb2f0dc0260ab61f07ac1805a313029b0f00950c00910b00",
  browns: "eedbbdecca96e9b97ae4a865dc9856d18954c7784cc0673fb85536ad44339f3632",
  tealBlues: "bce4d89dd3d181c3cb65b3c245a2b9368fae347da0306a932c5985",
  teals: "bbdfdfa2d4d58ac9c975bcbb61b0af4da5a43799982b8b8c1e7f7f127273006667",
  warmGreys: "dcd4d0cec5c1c0b8b4b3aaa7a59c9998908c8b827f7e7673726866665c5a59504e",
  goldGreen: "f4d166d5ca60b6c35c98bb597cb25760a6564b9c533f8f4f33834a257740146c36",
  goldOrange: "f4d166f8be5cf8aa4cf5983bf3852aef701be2621fd65322c54923b142239e3a26",
  goldRed: "f4d166f6be59f9aa51fc964ef6834bee734ae56249db5247cf4244c43141b71d3e",
  lightGreyRed: "efe9e6e1dad7d5cbc8c8bdb9bbaea9cd967ddc7b43e15f19df4011dc000b",
  lightGreyTeal: "e4eaead6dcddc8ced2b7c2c7a6b4bc64b0bf22a6c32295c11f85be1876bc",
  lightMulti: "e0f1f2c4e9d0b0de9fd0e181f6e072f6c053f3993ef77440ef4a3c",
  lightOrange: "f2e7daf7d5baf9c499fab184fa9c73f68967ef7860e8645bde515bd43d5b",
  lightTealBlue: "e3e9e0c0dccf9aceca7abfc859afc0389fb9328dad2f7ca0276b95255988",
  darkBlue: "3232322d46681a5c930074af008cbf05a7ce25c0dd38daed50f3faffffff",
  darkGold: "3c3c3c584b37725e348c7631ae8b2bcfa424ecc31ef9de30fff184ffffff",
  darkGreen: "3a3a3a215748006f4d048942489e4276b340a6c63dd2d836ffeb2cffffaa",
  darkMulti: "3737371f5287197d8c29a86995ce3fffe800ffffff",
  darkRed: "3434347036339e3c38cc4037e75d1eec8620eeab29f0ce32ffeb2c"
}, ig = {
  accent: P1,
  category10: q1,
  category20: "1f77b4aec7e8ff7f0effbb782ca02c98df8ad62728ff98969467bdc5b0d58c564bc49c94e377c2f7b6d27f7f7fc7c7c7bcbd22dbdb8d17becf9edae5",
  category20b: "393b795254a36b6ecf9c9ede6379398ca252b5cf6bcedb9c8c6d31bd9e39e7ba52e7cb94843c39ad494ad6616be7969c7b4173a55194ce6dbdde9ed6",
  category20c: "3182bd6baed69ecae1c6dbefe6550dfd8d3cfdae6bfdd0a231a35474c476a1d99bc7e9c0756bb19e9ac8bcbddcdadaeb636363969696bdbdbdd9d9d9",
  dark2: I1,
  observable10: H1,
  paired: L1,
  pastel1: O1,
  pastel2: z1,
  set1: W1,
  set2: X1,
  set3: B1,
  tableau10: "4c78a8f58518e4575672b7b254a24beeca3bb279a2ff9da69d755dbab0ac",
  tableau20: "4c78a89ecae9f58518ffbf7954a24b88d27ab79a20f2cf5b43989483bcb6e45756ff9d9879706ebab0acd67195fcbfd2b279a2d6a5c99e765fd8b5a5"
};
function Jf(n) {
  if (Ii(n)) return n;
  const e = n.length / 6 | 0, t = new Array(e);
  for (let r = 0; r < e; )
    t[r] = "#" + n.slice(r * 6, ++r * 6);
  return t;
}
function _f(n, e) {
  for (const t in n) ug(t, e(n[t]));
}
const Pa = {};
_f(ig, Jf);
_f(rg, (n) => ng(Jf(n)));
function ug(n, e) {
  return n = n && n.toLowerCase(), arguments.length > 1 ? (Pa[n] = e, this) : Pa[n];
}
const ag = "symbol", og = "discrete", md = "gradient", fg = (n) => Ii(n) ? n.map((e) => String(e)) : String(n), cg = (n, e) => n[1] - e[1], lg = (n, e) => e[1] - n[1];
function bd(n, e, t) {
  let r;
  return a0(e) && (n.bins && (e = Math.max(e, n.bins.length)), t != null && (e = Math.min(e, Math.floor(o0(n.domain()) / t || 1) + 1))), e0(e) && (r = e.step, e = e.interval), Ro(e) && (e = n.type === Ye ? du(e) : n.type == Re ? pu(e) : Xt("Only time and utc scales accept interval strings."), r && (e = e.every(r))), e;
}
function sg(n, e, t) {
  let r = n.range(), i = r[0], u = Vn(r), a = cg;
  if (i > u && (r = u, u = i, i = r, a = lg), i = Math.floor(i), u = Math.ceil(u), e = e.map((o) => [o, n(o)]).filter((o) => i <= o[1] && o[1] <= u).sort(a).map((o) => o[0]), t > 0 && e.length > 1) {
    const o = [e[0], Vn(e)];
    for (; e.length > t && e.length >= 3; )
      e = e.filter((c, f) => !(f % 2));
    e.length < 3 && (e = o);
  }
  return e;
}
function Kf(n, e) {
  return n.bins ? sg(n, n.bins, e) : n.ticks ? n.ticks(e) : n.domain();
}
function hg(n, e, t, r, i, u) {
  const a = e.type;
  let o = fg;
  if (a === Ye || i === Ye)
    o = n.timeFormat(r);
  else if (a === Re || i === Re)
    o = n.utcFormat(r);
  else if (Jh(a)) {
    const c = n.formatFloat(r);
    if (u || e.bins)
      o = c;
    else {
      const f = nc(e, t, !1);
      o = (l) => f(l) ? c(l) : "";
    }
  } else if (e.tickFormat) {
    const c = e.domain();
    o = n.formatSpan(c[0], c[c.length - 1], t, r);
  } else r && (o = n.format(r));
  return o;
}
function nc(n, e, t) {
  const r = Kf(n, e), i = n.base(), u = Math.log(i), a = Math.max(1, i * e / r.length), o = (c) => {
    let f = c / Math.pow(i, Math.round(Math.log(c) / u));
    return f * i < i - 0.5 && (f *= i), f <= a;
  };
  return t ? r.filter(o) : o;
}
const Fi = {
  [St]: "quantiles",
  [vu]: "thresholds",
  [wu]: "domain"
}, ec = {
  [St]: "quantiles",
  [vu]: "domain"
};
function gg(n, e) {
  return n.bins ? mg(n.bins) : n.type === _n ? nc(n, e, !0) : Fi[n.type] ? pg(n[Fi[n.type]]()) : Kf(n, e);
}
function dg(n, e, t) {
  const r = e[ec[e.type]](), i = r.length;
  let u = i > 1 ? r[1] - r[0] : r[0], a;
  for (a = 1; a < i; ++a)
    u = Math.min(u, r[a] - r[a - 1]);
  return n.formatSpan(0, u, 3 * 10, t);
}
function pg(n) {
  const e = [-1 / 0].concat(n);
  return e.max = 1 / 0, e;
}
function mg(n) {
  const e = n.slice(0, -1);
  return e.max = Vn(n), e;
}
const bg = (n) => Fi[n.type] || n.bins;
function yg(n, e, t, r, i, u, a) {
  const o = ec[e.type] && u !== Ye && u !== Re ? dg(n, e, i) : hg(n, e, t, i, u, a);
  return r === ag && bg(e) ? Mg(o) : r === og ? vg(o) : wg(o);
}
const Mg = (n) => (e, t, r) => {
  const i = Ia(r[t + 1], Ia(r.max, 1 / 0)), u = Ha(e, n), a = Ha(i, n);
  return u && a ? u + " – " + a : a ? "< " + a : "≥ " + u;
}, Ia = (n, e) => n ?? e, vg = (n) => (e, t) => t ? n(e) : null, wg = (n) => (e) => n(e), Ha = (n, e) => Number.isFinite(n) ? e(n) : null;
function yd(n) {
  const e = n.domain(), t = e.length - 1;
  let r = +e[0], i = +Vn(e), u = i - r;
  if (n.type === wu) {
    const a = t ? u / t : 0.1;
    r -= a, i += a, u = i - r;
  }
  return (a) => (a - r) / u;
}
function xg(n, e, t, r) {
  const i = r || e.type;
  return Ro(t) && _h(i) && (t = t.replace(/%a/g, "%A").replace(/%b/g, "%B")), !t && i === Ye ? n.timeFormat("%A, %d %B %Y, %X") : !t && i === Re ? n.utcFormat("%A, %d %B %Y, %X UTC") : yg(n, e, 5, null, t, r, !0);
}
function Md(n, e, t) {
  t = t || {};
  const r = Math.max(3, t.maxlen || 7), i = xg(n, e, t.format, t.formatType);
  if (Vh(e.type)) {
    const u = gg(e).slice(1).map(i), a = u.length;
    return `${a} boundar${a === 1 ? "y" : "ies"}: ${u.join(", ")}`;
  } else if (Qh(e.type)) {
    const u = e.domain(), a = u.length, o = a > r ? u.slice(0, r - 2).map(i).join(", ") + ", ending with " + u.slice(-1).map(i) : u.map(i).join(", ");
    return `${a} value${a === 1 ? "" : "s"}: ${o}`;
  } else {
    const u = e.domain();
    return `values from ${i(u[0])} to ${i(Vn(u))}`;
  }
}
const Tg = wo(), Sg = [
  // standard properties in d3-geo
  "clipAngle",
  "clipExtent",
  "scale",
  "translate",
  "center",
  "rotate",
  "parallels",
  "precision",
  "reflectX",
  "reflectY",
  // extended properties in d3-geo-projections
  "coefficient",
  "distance",
  "fraction",
  "lobes",
  "parallel",
  "radius",
  "ratio",
  "spacing",
  "tilt"
];
function $g(n, e) {
  return function t() {
    const r = e();
    return r.type = n, r.path = wo().projection(r), r.copy = r.copy || function() {
      const i = t();
      return Sg.forEach((u) => {
        r[u] && i[u](r[u]());
      }), i.path.pointRadius(r.path.pointRadius()), i;
    }, Vf(r);
  };
}
function Cg(n, e) {
  if (!n || typeof n != "string")
    throw new Error("Projection type must be a name string.");
  return n = n.toLowerCase(), arguments.length > 1 ? (gr[n] = $g(n, e), this) : gr[n] || null;
}
function vd(n) {
  return n && n.path || Tg;
}
const gr = {
  // base d3-geo projection types
  albers: To,
  albersusa: Cl,
  azimuthalequalarea: Nl,
  azimuthalequidistant: Dl,
  conicconformal: Fl,
  conicequalarea: er,
  conicequidistant: Yl,
  equalEarth: ql,
  equirectangular: Al,
  gnomonic: Pl,
  identity: Il,
  mercator: Ul,
  mollweide: Ql,
  naturalEarth1: Hl,
  orthographic: Ll,
  stereographic: Ol,
  transversemercator: zl
};
for (const n in gr)
  Cg(n, gr[n]);
export {
  Ec as $,
  le as A,
  pu as B,
  Ng as C,
  $n as D,
  Dg as E,
  Fg as F,
  jg as G,
  En as H,
  Eg as I,
  Yg as J,
  Pg as K,
  Tc as L,
  Fn as M,
  fd as N,
  wh as O,
  rd as P,
  Sn as Q,
  td as R,
  jn as S,
  vh as T,
  dr as U,
  Sc as V,
  rn as W,
  kg as X,
  fn as Y,
  Qn as Z,
  Hg as _,
  On as a,
  Ka as a$,
  Ig as a0,
  Lg as a1,
  vc as a2,
  Du as a3,
  Nu as a4,
  Gg as a5,
  Zg as a6,
  Qh as a7,
  Md as a8,
  bd as a9,
  xr as aA,
  ge as aB,
  Hh as aC,
  Ih as aD,
  Rh as aE,
  ug as aF,
  wu as aG,
  St as aH,
  vu as aI,
  dd as aJ,
  gd as aK,
  Ft as aL,
  vd as aM,
  ur as aN,
  Sg as aO,
  Cg as aP,
  $c as aQ,
  Bg as aR,
  Hc as aS,
  Lc as aT,
  Og as aU,
  zg as aV,
  Wg as aW,
  Oc as aX,
  Xg as aY,
  Ug as aZ,
  ce as a_,
  hg as aa,
  sg as ab,
  Kf as ac,
  ag as ad,
  yg as ae,
  gg as af,
  md as ag,
  pd as ah,
  yd as ai,
  W as aj,
  Oe as ak,
  mu as al,
  ld as am,
  Ye as an,
  Re as ao,
  Ph as ap,
  _u as aq,
  _n as ar,
  yu as as,
  bu as at,
  Mu as au,
  Jh as av,
  Lh as aw,
  sd as ax,
  ng as ay,
  eg as az,
  O as b,
  kc as b0,
  Pc as b1,
  Dc as b2,
  Ac as b3,
  qc as b4,
  no as b5,
  Yc as b6,
  Ic as b7,
  _a as b8,
  Fc as b9,
  Rc as ba,
  mi as bb,
  bi as bc,
  pi as bd,
  ud as be,
  od as bf,
  id as bg,
  ad as bh,
  Jg as bi,
  Kg as bj,
  ed as bk,
  _g as bl,
  nd as bm,
  cd as bn,
  Zh as bo,
  hd as bp,
  Vh as bq,
  Bn as br,
  qg as bs,
  Rg as bt,
  Ag as bu,
  R as c,
  Ne as d,
  A as e,
  Zt as f,
  xe as g,
  ei as h,
  ni as i,
  tn as j,
  eo as k,
  Vg as l,
  yn as m,
  mn as n,
  cn as o,
  xc as p,
  Fu as q,
  G as r,
  E as s,
  gn as t,
  Qg as u,
  ht as v,
  hn as w,
  Gn as x,
  an as y,
  du as z
};
