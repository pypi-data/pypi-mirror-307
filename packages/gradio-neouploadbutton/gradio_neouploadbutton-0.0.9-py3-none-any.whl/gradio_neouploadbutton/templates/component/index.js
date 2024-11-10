const {
  SvelteComponent: Ee,
  append_hydration: he,
  attr: g,
  bubble: Be,
  check_outros: Ge,
  children: be,
  claim_element: ne,
  claim_space: ge,
  create_slot: ve,
  detach: O,
  element: te,
  empty: _e,
  get_all_dirty_from_scope: we,
  get_slot_changes: ke,
  group_outros: Me,
  init: Ne,
  insert_hydration: x,
  listen: Oe,
  safe_not_equal: Ue,
  set_style: C,
  space: ze,
  src_url_equal: $,
  toggle_class: R,
  transition_in: ee,
  transition_out: ie,
  update_slot_base: Ce
} = window.__gradio__svelte__internal;
function We(l) {
  let e, i, t, n, a, d, c = (
    /*icon*/
    l[7] && ce(l)
  );
  const f = (
    /*#slots*/
    l[12].default
  ), s = ve(
    f,
    l,
    /*$$scope*/
    l[11],
    null
  );
  return {
    c() {
      e = te("button"), c && c.c(), i = ze(), s && s.c(), this.h();
    },
    l(o) {
      e = ne(o, "BUTTON", { class: !0, id: !0 });
      var u = be(e);
      c && c.l(u), i = ge(u), s && s.l(u), u.forEach(O), this.h();
    },
    h() {
      g(e, "class", t = /*size*/
      l[4] + " " + /*variant*/
      l[3] + " " + /*elem_classes*/
      l[1].join(" ") + " svelte-8huxfn"), g(
        e,
        "id",
        /*elem_id*/
        l[0]
      ), e.disabled = /*disabled*/
      l[8], R(e, "hidden", !/*visible*/
      l[2]), C(
        e,
        "flex-grow",
        /*scale*/
        l[9]
      ), C(
        e,
        "width",
        /*scale*/
        l[9] === 0 ? "fit-content" : null
      ), C(e, "min-width", typeof /*min_width*/
      l[10] == "number" ? `calc(min(${/*min_width*/
      l[10]}px, 100%))` : null);
    },
    m(o, u) {
      x(o, e, u), c && c.m(e, null), he(e, i), s && s.m(e, null), n = !0, a || (d = Oe(
        e,
        "click",
        /*click_handler*/
        l[13]
      ), a = !0);
    },
    p(o, u) {
      /*icon*/
      o[7] ? c ? c.p(o, u) : (c = ce(o), c.c(), c.m(e, i)) : c && (c.d(1), c = null), s && s.p && (!n || u & /*$$scope*/
      2048) && Ce(
        s,
        f,
        o,
        /*$$scope*/
        o[11],
        n ? ke(
          f,
          /*$$scope*/
          o[11],
          u,
          null
        ) : we(
          /*$$scope*/
          o[11]
        ),
        null
      ), (!n || u & /*size, variant, elem_classes*/
      26 && t !== (t = /*size*/
      o[4] + " " + /*variant*/
      o[3] + " " + /*elem_classes*/
      o[1].join(" ") + " svelte-8huxfn")) && g(e, "class", t), (!n || u & /*elem_id*/
      1) && g(
        e,
        "id",
        /*elem_id*/
        o[0]
      ), (!n || u & /*disabled*/
      256) && (e.disabled = /*disabled*/
      o[8]), (!n || u & /*size, variant, elem_classes, visible*/
      30) && R(e, "hidden", !/*visible*/
      o[2]), u & /*scale*/
      512 && C(
        e,
        "flex-grow",
        /*scale*/
        o[9]
      ), u & /*scale*/
      512 && C(
        e,
        "width",
        /*scale*/
        o[9] === 0 ? "fit-content" : null
      ), u & /*min_width*/
      1024 && C(e, "min-width", typeof /*min_width*/
      o[10] == "number" ? `calc(min(${/*min_width*/
      o[10]}px, 100%))` : null);
    },
    i(o) {
      n || (ee(s, o), n = !0);
    },
    o(o) {
      ie(s, o), n = !1;
    },
    d(o) {
      o && O(e), c && c.d(), s && s.d(o), a = !1, d();
    }
  };
}
function Ae(l) {
  let e, i, t, n, a = (
    /*icon*/
    l[7] && re(l)
  );
  const d = (
    /*#slots*/
    l[12].default
  ), c = ve(
    d,
    l,
    /*$$scope*/
    l[11],
    null
  );
  return {
    c() {
      e = te("a"), a && a.c(), i = ze(), c && c.c(), this.h();
    },
    l(f) {
      e = ne(f, "A", {
        href: !0,
        rel: !0,
        "aria-disabled": !0,
        class: !0,
        id: !0
      });
      var s = be(e);
      a && a.l(s), i = ge(s), c && c.l(s), s.forEach(O), this.h();
    },
    h() {
      g(
        e,
        "href",
        /*link*/
        l[6]
      ), g(e, "rel", "noopener noreferrer"), g(
        e,
        "aria-disabled",
        /*disabled*/
        l[8]
      ), g(e, "class", t = /*size*/
      l[4] + " " + /*variant*/
      l[3] + " " + /*elem_classes*/
      l[1].join(" ") + " svelte-8huxfn"), g(
        e,
        "id",
        /*elem_id*/
        l[0]
      ), R(e, "hidden", !/*visible*/
      l[2]), R(
        e,
        "disabled",
        /*disabled*/
        l[8]
      ), C(
        e,
        "flex-grow",
        /*scale*/
        l[9]
      ), C(
        e,
        "pointer-events",
        /*disabled*/
        l[8] ? "none" : null
      ), C(
        e,
        "width",
        /*scale*/
        l[9] === 0 ? "fit-content" : null
      ), C(e, "min-width", typeof /*min_width*/
      l[10] == "number" ? `calc(min(${/*min_width*/
      l[10]}px, 100%))` : null);
    },
    m(f, s) {
      x(f, e, s), a && a.m(e, null), he(e, i), c && c.m(e, null), n = !0;
    },
    p(f, s) {
      /*icon*/
      f[7] ? a ? a.p(f, s) : (a = re(f), a.c(), a.m(e, i)) : a && (a.d(1), a = null), c && c.p && (!n || s & /*$$scope*/
      2048) && Ce(
        c,
        d,
        f,
        /*$$scope*/
        f[11],
        n ? ke(
          d,
          /*$$scope*/
          f[11],
          s,
          null
        ) : we(
          /*$$scope*/
          f[11]
        ),
        null
      ), (!n || s & /*link*/
      64) && g(
        e,
        "href",
        /*link*/
        f[6]
      ), (!n || s & /*disabled*/
      256) && g(
        e,
        "aria-disabled",
        /*disabled*/
        f[8]
      ), (!n || s & /*size, variant, elem_classes*/
      26 && t !== (t = /*size*/
      f[4] + " " + /*variant*/
      f[3] + " " + /*elem_classes*/
      f[1].join(" ") + " svelte-8huxfn")) && g(e, "class", t), (!n || s & /*elem_id*/
      1) && g(
        e,
        "id",
        /*elem_id*/
        f[0]
      ), (!n || s & /*size, variant, elem_classes, visible*/
      30) && R(e, "hidden", !/*visible*/
      f[2]), (!n || s & /*size, variant, elem_classes, disabled*/
      282) && R(
        e,
        "disabled",
        /*disabled*/
        f[8]
      ), s & /*scale*/
      512 && C(
        e,
        "flex-grow",
        /*scale*/
        f[9]
      ), s & /*disabled*/
      256 && C(
        e,
        "pointer-events",
        /*disabled*/
        f[8] ? "none" : null
      ), s & /*scale*/
      512 && C(
        e,
        "width",
        /*scale*/
        f[9] === 0 ? "fit-content" : null
      ), s & /*min_width*/
      1024 && C(e, "min-width", typeof /*min_width*/
      f[10] == "number" ? `calc(min(${/*min_width*/
      f[10]}px, 100%))` : null);
    },
    i(f) {
      n || (ee(c, f), n = !0);
    },
    o(f) {
      ie(c, f), n = !1;
    },
    d(f) {
      f && O(e), a && a.d(), c && c.d(f);
    }
  };
}
function ce(l) {
  let e, i, t;
  return {
    c() {
      e = te("img"), this.h();
    },
    l(n) {
      e = ne(n, "IMG", { class: !0, src: !0, alt: !0 }), this.h();
    },
    h() {
      g(e, "class", "button-icon svelte-8huxfn"), $(e.src, i = /*icon*/
      l[7].url) || g(e, "src", i), g(e, "alt", t = `${/*value*/
      l[5]} icon`);
    },
    m(n, a) {
      x(n, e, a);
    },
    p(n, a) {
      a & /*icon*/
      128 && !$(e.src, i = /*icon*/
      n[7].url) && g(e, "src", i), a & /*value*/
      32 && t !== (t = `${/*value*/
      n[5]} icon`) && g(e, "alt", t);
    },
    d(n) {
      n && O(e);
    }
  };
}
function re(l) {
  let e, i, t;
  return {
    c() {
      e = te("img"), this.h();
    },
    l(n) {
      e = ne(n, "IMG", { class: !0, src: !0, alt: !0 }), this.h();
    },
    h() {
      g(e, "class", "button-icon svelte-8huxfn"), $(e.src, i = /*icon*/
      l[7].url) || g(e, "src", i), g(e, "alt", t = `${/*value*/
      l[5]} icon`);
    },
    m(n, a) {
      x(n, e, a);
    },
    p(n, a) {
      a & /*icon*/
      128 && !$(e.src, i = /*icon*/
      n[7].url) && g(e, "src", i), a & /*value*/
      32 && t !== (t = `${/*value*/
      n[5]} icon`) && g(e, "alt", t);
    },
    d(n) {
      n && O(e);
    }
  };
}
function Fe(l) {
  let e, i, t, n;
  const a = [Ae, We], d = [];
  function c(f, s) {
    return (
      /*link*/
      f[6] && /*link*/
      f[6].length > 0 ? 0 : 1
    );
  }
  return e = c(l), i = d[e] = a[e](l), {
    c() {
      i.c(), t = _e();
    },
    l(f) {
      i.l(f), t = _e();
    },
    m(f, s) {
      d[e].m(f, s), x(f, t, s), n = !0;
    },
    p(f, [s]) {
      let o = e;
      e = c(f), e === o ? d[e].p(f, s) : (Me(), ie(d[o], 1, 1, () => {
        d[o] = null;
      }), Ge(), i = d[e], i ? i.p(f, s) : (i = d[e] = a[e](f), i.c()), ee(i, 1), i.m(t.parentNode, t));
    },
    i(f) {
      n || (ee(i), n = !0);
    },
    o(f) {
      ie(i), n = !1;
    },
    d(f) {
      f && O(t), d[e].d(f);
    }
  };
}
function Re(l, e, i) {
  let { $$slots: t = {}, $$scope: n } = e, { elem_id: a = "" } = e, { elem_classes: d = [] } = e, { visible: c = !0 } = e, { variant: f = "secondary" } = e, { size: s = "lg" } = e, { value: o = null } = e, { link: u = null } = e, { icon: m = null } = e, { disabled: b = !1 } = e, { scale: L = null } = e, { min_width: S = void 0 } = e;
  function q(h) {
    Be.call(this, l, h);
  }
  return l.$$set = (h) => {
    "elem_id" in h && i(0, a = h.elem_id), "elem_classes" in h && i(1, d = h.elem_classes), "visible" in h && i(2, c = h.visible), "variant" in h && i(3, f = h.variant), "size" in h && i(4, s = h.size), "value" in h && i(5, o = h.value), "link" in h && i(6, u = h.link), "icon" in h && i(7, m = h.icon), "disabled" in h && i(8, b = h.disabled), "scale" in h && i(9, L = h.scale), "min_width" in h && i(10, S = h.min_width), "$$scope" in h && i(11, n = h.$$scope);
  }, [
    a,
    d,
    c,
    f,
    s,
    o,
    u,
    m,
    b,
    L,
    S,
    n,
    t,
    q
  ];
}
class Ve extends Ee {
  constructor(e) {
    super(), Ne(this, e, Re, Fe, Ue, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
var He = Object.defineProperty, Je = (l, e, i) => e in l ? He(l, e, { enumerable: !0, configurable: !0, writable: !0, value: i }) : l[e] = i, D = (l, e, i) => (Je(l, typeof e != "symbol" ? e + "" : e, i), i), Ie = (l, e, i) => {
  if (!e.has(l))
    throw TypeError("Cannot " + i);
}, j = (l, e, i) => (Ie(l, e, "read from private field"), i ? i.call(l) : e.get(l)), Ke = (l, e, i) => {
  if (e.has(l))
    throw TypeError("Cannot add the same private member more than once");
  e instanceof WeakSet ? e.add(l) : e.set(l, i);
}, Pe = (l, e, i, t) => (Ie(l, e, "write to private field"), e.set(l, i), i), B;
new Intl.Collator(0, { numeric: 1 }).compare;
async function Qe(l, e) {
  return l.map(
    (i) => new Xe({
      path: i.name,
      orig_name: i.name,
      blob: i,
      size: i.size,
      mime_type: i.type,
      is_stream: e
    })
  );
}
class Xe {
  constructor({
    path: e,
    url: i,
    orig_name: t,
    size: n,
    blob: a,
    is_stream: d,
    mime_type: c,
    alt_text: f
  }) {
    D(this, "path"), D(this, "url"), D(this, "orig_name"), D(this, "size"), D(this, "blob"), D(this, "is_stream"), D(this, "mime_type"), D(this, "alt_text"), D(this, "meta", { _type: "gradio.FileData" }), this.path = e, this.url = i, this.orig_name = t, this.size = n, this.blob = i ? void 0 : a, this.is_stream = d, this.mime_type = c, this.alt_text = f;
  }
}
typeof process < "u" && process.versions && process.versions.node;
class Wi extends TransformStream {
  /** Constructs a new instance. */
  constructor(e = { allowCR: !1 }) {
    super({
      transform: (i, t) => {
        for (i = j(this, B) + i; ; ) {
          const n = i.indexOf(`
`), a = e.allowCR ? i.indexOf("\r") : -1;
          if (a !== -1 && a !== i.length - 1 && (n === -1 || n - 1 > a)) {
            t.enqueue(i.slice(0, a)), i = i.slice(a + 1);
            continue;
          }
          if (n === -1)
            break;
          const d = i[n - 1] === "\r" ? n - 1 : n;
          t.enqueue(i.slice(0, d)), i = i.slice(n + 1);
        }
        Pe(this, B, i);
      },
      flush: (i) => {
        if (j(this, B) === "")
          return;
        const t = e.allowCR && j(this, B).endsWith("\r") ? j(this, B).slice(0, -1) : j(this, B);
        i.enqueue(t);
      }
    }), Ke(this, B, "");
  }
}
B = /* @__PURE__ */ new WeakMap();
const {
  SvelteComponent: Ye,
  append_hydration: Ze,
  attr: w,
  binding_callbacks: je,
  children: pe,
  claim_component: xe,
  claim_element: se,
  claim_space: ye,
  claim_text: $e,
  create_component: ei,
  create_slot: ii,
  destroy_component: li,
  detach: V,
  element: oe,
  get_all_dirty_from_scope: ni,
  get_slot_changes: ti,
  init: ai,
  insert_hydration: p,
  listen: le,
  mount_component: fi,
  run_all: Le,
  safe_not_equal: ui,
  set_data: si,
  space: qe,
  src_url_equal: de,
  text: oi,
  transition_in: Se,
  transition_out: Te,
  update_slot_base: _i
} = window.__gradio__svelte__internal, { tick: ci, createEventDispatcher: ri } = window.__gradio__svelte__internal;
function me(l) {
  let e, i, t;
  return {
    c() {
      e = oe("img"), this.h();
    },
    l(n) {
      e = se(n, "IMG", { class: !0, src: !0, alt: !0 }), this.h();
    },
    h() {
      w(e, "class", "button-icon svelte-oc0iyx"), de(e.src, i = /*icon*/
      l[7].url) || w(e, "src", i), w(e, "alt", t = `${/*value*/
      l[1]} icon`);
    },
    m(n, a) {
      p(n, e, a);
    },
    p(n, a) {
      a & /*icon*/
      128 && !de(e.src, i = /*icon*/
      n[7].url) && w(e, "src", i), a & /*value*/
      2 && t !== (t = `${/*value*/
      n[1]} icon`) && w(e, "alt", t);
    },
    d(n) {
      n && V(e);
    }
  };
}
function di(l) {
  let e;
  return {
    c() {
      e = oi(
        /*label*/
        l[0]
      );
    },
    l(i) {
      e = $e(
        i,
        /*label*/
        l[0]
      );
    },
    m(i, t) {
      p(i, e, t);
    },
    p(i, t) {
      t & /*label*/
      1 && si(
        e,
        /*label*/
        i[0]
      );
    },
    d(i) {
      i && V(e);
    }
  };
}
function mi(l) {
  let e, i, t, n, a, d = (
    /*icon*/
    l[7] && me(l)
  );
  const c = (
    /*#slots*/
    l[25].default
  ), f = ii(
    c,
    l,
    /*$$scope*/
    l[27],
    null
  ), s = f || di(l);
  return {
    c() {
      e = oe("div"), d && d.c(), i = qe(), s && s.c(), this.h();
    },
    l(o) {
      e = se(o, "DIV", { role: !0, class: !0 });
      var u = pe(e);
      d && d.l(u), i = ye(u), s && s.l(u), u.forEach(V), this.h();
    },
    h() {
      w(e, "role", "presentation"), w(e, "class", "dragdrop svelte-oc0iyx");
    },
    m(o, u) {
      p(o, e, u), d && d.m(e, null), Ze(e, i), s && s.m(e, null), t = !0, n || (a = [
        le(e, "dragover", bi),
        le(
          e,
          "drop",
          /*drop_files*/
          l[16]
        )
      ], n = !0);
    },
    p(o, u) {
      /*icon*/
      o[7] ? d ? d.p(o, u) : (d = me(o), d.c(), d.m(e, i)) : d && (d.d(1), d = null), f ? f.p && (!t || u & /*$$scope*/
      134217728) && _i(
        f,
        c,
        o,
        /*$$scope*/
        o[27],
        t ? ti(
          c,
          /*$$scope*/
          o[27],
          u,
          null
        ) : ni(
          /*$$scope*/
          o[27]
        ),
        null
      ) : s && s.p && (!t || u & /*label*/
      1) && s.p(o, t ? u : -1);
    },
    i(o) {
      t || (Se(s, o), t = !0);
    },
    o(o) {
      Te(s, o), t = !1;
    },
    d(o) {
      o && V(e), d && d.d(), s && s.d(o), n = !1, Le(a);
    }
  };
}
function hi(l) {
  let e, i, t, n, a, d, c, f, s, o;
  return c = new Ve({
    props: {
      size: (
        /*size*/
        l[6]
      ),
      variant: (
        /*variant*/
        l[10]
      ),
      elem_id: (
        /*elem_id*/
        l[2]
      ),
      elem_classes: (
        /*elem_classes*/
        l[3]
      ),
      visible: (
        /*visible*/
        l[4]
      ),
      scale: (
        /*scale*/
        l[8]
      ),
      min_width: (
        /*min_width*/
        l[9]
      ),
      disabled: (
        /*disabled*/
        l[11]
      ),
      $$slots: { default: [mi] },
      $$scope: { ctx: l }
    }
  }), c.$on(
    "click",
    /*open_file_upload*/
    l[14]
  ), {
    c() {
      e = oe("input"), d = qe(), ei(c.$$.fragment), this.h();
    },
    l(u) {
      e = se(u, "INPUT", {
        class: !0,
        accept: !0,
        type: !0,
        webkitdirectory: !0,
        mozdirectory: !0,
        "data-testid": !0
      }), d = ye(u), xe(c.$$.fragment, u), this.h();
    },
    h() {
      w(e, "class", "hide svelte-oc0iyx"), w(
        e,
        "accept",
        /*accept_file_types*/
        l[13]
      ), w(e, "type", "file"), e.multiple = i = /*file_count*/
      l[5] === "multiple" || void 0, w(e, "webkitdirectory", t = /*file_count*/
      l[5] === "directory" || void 0), w(e, "mozdirectory", n = /*file_count*/
      l[5] === "directory" || void 0), w(e, "data-testid", a = /*label*/
      l[0] + "-upload-button");
    },
    m(u, m) {
      p(u, e, m), l[26](e), p(u, d, m), fi(c, u, m), f = !0, s || (o = [
        le(
          e,
          "change",
          /*load_files_from_upload*/
          l[15]
        ),
        le(e, "click", gi)
      ], s = !0);
    },
    p(u, [m]) {
      (!f || m & /*accept_file_types*/
      8192) && w(
        e,
        "accept",
        /*accept_file_types*/
        u[13]
      ), (!f || m & /*file_count*/
      32 && i !== (i = /*file_count*/
      u[5] === "multiple" || void 0)) && (e.multiple = i), (!f || m & /*file_count*/
      32 && t !== (t = /*file_count*/
      u[5] === "directory" || void 0)) && w(e, "webkitdirectory", t), (!f || m & /*file_count*/
      32 && n !== (n = /*file_count*/
      u[5] === "directory" || void 0)) && w(e, "mozdirectory", n), (!f || m & /*label*/
      1 && a !== (a = /*label*/
      u[0] + "-upload-button")) && w(e, "data-testid", a);
      const b = {};
      m & /*size*/
      64 && (b.size = /*size*/
      u[6]), m & /*variant*/
      1024 && (b.variant = /*variant*/
      u[10]), m & /*elem_id*/
      4 && (b.elem_id = /*elem_id*/
      u[2]), m & /*elem_classes*/
      8 && (b.elem_classes = /*elem_classes*/
      u[3]), m & /*visible*/
      16 && (b.visible = /*visible*/
      u[4]), m & /*scale*/
      256 && (b.scale = /*scale*/
      u[8]), m & /*min_width*/
      512 && (b.min_width = /*min_width*/
      u[9]), m & /*disabled*/
      2048 && (b.disabled = /*disabled*/
      u[11]), m & /*$$scope, label, icon, value*/
      134217859 && (b.$$scope = { dirty: m, ctx: u }), c.$set(b);
    },
    i(u) {
      f || (Se(c.$$.fragment, u), f = !0);
    },
    o(u) {
      Te(c.$$.fragment, u), f = !1;
    },
    d(u) {
      u && (V(e), V(d)), l[26](null), li(c, u), s = !1, Le(o);
    }
  };
}
function bi(l) {
  l.preventDefault(), l.stopPropagation();
}
function gi(l) {
  const e = l.target;
  e.value && (e.value = "");
}
function vi(l, e, i) {
  let { $$slots: t = {}, $$scope: n } = e;
  var a = this && this.__awaiter || function(_, v, k, I) {
    function M(T) {
      return T instanceof k ? T : new k(function(y) {
        y(T);
      });
    }
    return new (k || (k = Promise))(function(T, y) {
      function Z(N) {
        try {
          fe(I.next(N));
        } catch (ue) {
          y(ue);
        }
      }
      function De(N) {
        try {
          fe(I.throw(N));
        } catch (ue) {
          y(ue);
        }
      }
      function fe(N) {
        N.done ? T(N.value) : M(N.value).then(Z, De);
      }
      fe((I = I.apply(_, v || [])).next());
    });
  };
  let { elem_id: d = "" } = e, { elem_classes: c = [] } = e, { visible: f = !0 } = e, { loading_message: s } = e, { label: o } = e, { oldLabel: u } = e, { interactive: m } = e, { oldInteractive: b } = e, { value: L } = e, { file_count: S } = e, { file_types: q = [] } = e, { root: h } = e, { size: H = "lg" } = e, { icon: J = null } = e, { scale: K = 1 } = e, { min_width: P = void 0 } = e, { variant: E = "secondary" } = e, { disabled: U = !1 } = e, { max_file_size: G = null } = e, { upload: Q } = e;
  const z = ri();
  let W, X;
  q == null ? X = null : (q = q.map((_) => _.startsWith(".") ? _ : _ + "/*"), X = q.join(", "));
  function ae() {
    z("click"), W.click();
  }
  function r(_) {
    return a(this, void 0, void 0, function* () {
      var v;
      let k = Array.from(_);
      if (!_.length)
        return;
      S === "single" && (k = [_[0]]);
      let I = yield Qe(k);
      yield ci();
      try {
        I = (v = yield Q(I, h, void 0, G ?? 1 / 0)) === null || v === void 0 ? void 0 : v.filter((M) => M !== null);
      } catch (M) {
        z("error", M.message);
        return;
      }
      i(1, L = S === "single" ? I == null ? void 0 : I[0] : I), z("change", L), z("upload", L);
    });
  }
  function Y(_) {
    return a(this, void 0, void 0, function* () {
      const v = _.target;
      v.files && (i(17, u = o), i(19, b = m), i(0, o = typeof s < "u" ? s : u), i(18, m = !(typeof s < "u")), z("labelChange", o), z("interactiveChange", m), yield r(v.files), i(0, o = u), i(18, m = b), z("labelChange", o), z("interactiveChange", m));
    });
  }
  function A(_) {
    return a(this, void 0, void 0, function* () {
      var v;
      console.log("drop"), _.preventDefault(), _.stopPropagation();
      const k = (v = _.dataTransfer) === null || v === void 0 ? void 0 : v.files;
      k && (i(17, u = o), i(19, b = m), i(0, o = typeof s < "u" ? s : u), i(18, m = !(typeof s < "u")), z("labelChange", o), z("interactiveChange", m), yield r(k), i(0, o = u), i(18, m = b), z("labelChange", o), z("interactiveChange", m));
    });
  }
  function F(_) {
    je[_ ? "unshift" : "push"](() => {
      W = _, i(12, W);
    });
  }
  return l.$$set = (_) => {
    "elem_id" in _ && i(2, d = _.elem_id), "elem_classes" in _ && i(3, c = _.elem_classes), "visible" in _ && i(4, f = _.visible), "loading_message" in _ && i(21, s = _.loading_message), "label" in _ && i(0, o = _.label), "oldLabel" in _ && i(17, u = _.oldLabel), "interactive" in _ && i(18, m = _.interactive), "oldInteractive" in _ && i(19, b = _.oldInteractive), "value" in _ && i(1, L = _.value), "file_count" in _ && i(5, S = _.file_count), "file_types" in _ && i(20, q = _.file_types), "root" in _ && i(22, h = _.root), "size" in _ && i(6, H = _.size), "icon" in _ && i(7, J = _.icon), "scale" in _ && i(8, K = _.scale), "min_width" in _ && i(9, P = _.min_width), "variant" in _ && i(10, E = _.variant), "disabled" in _ && i(11, U = _.disabled), "max_file_size" in _ && i(23, G = _.max_file_size), "upload" in _ && i(24, Q = _.upload), "$$scope" in _ && i(27, n = _.$$scope);
  }, [
    o,
    L,
    d,
    c,
    f,
    S,
    H,
    J,
    K,
    P,
    E,
    U,
    W,
    X,
    ae,
    Y,
    A,
    u,
    m,
    b,
    q,
    s,
    h,
    G,
    Q,
    t,
    F,
    n
  ];
}
class wi extends Ye {
  constructor(e) {
    super(), ai(this, e, vi, hi, ui, {
      elem_id: 2,
      elem_classes: 3,
      visible: 4,
      loading_message: 21,
      label: 0,
      oldLabel: 17,
      interactive: 18,
      oldInteractive: 19,
      value: 1,
      file_count: 5,
      file_types: 20,
      root: 22,
      size: 6,
      icon: 7,
      scale: 8,
      min_width: 9,
      variant: 10,
      disabled: 11,
      max_file_size: 23,
      upload: 24
    });
  }
}
const {
  SvelteComponent: ki,
  claim_component: zi,
  claim_text: Ci,
  create_component: Ii,
  destroy_component: yi,
  detach: Li,
  init: qi,
  insert_hydration: Si,
  mount_component: Ti,
  safe_not_equal: Di,
  set_data: Ei,
  text: Bi,
  transition_in: Gi,
  transition_out: Mi
} = window.__gradio__svelte__internal;
function Ni(l) {
  let e = (
    /*label*/
    (l[1] ? (
      /*gradio*/
      l[17].i18n(
        /*label*/
        l[1]
      )
    ) : "") + ""
  ), i;
  return {
    c() {
      i = Bi(e);
    },
    l(t) {
      i = Ci(t, e);
    },
    m(t, n) {
      Si(t, i, n);
    },
    p(t, n) {
      n & /*label, gradio*/
      131074 && e !== (e = /*label*/
      (t[1] ? (
        /*gradio*/
        t[17].i18n(
          /*label*/
          t[1]
        )
      ) : "") + "") && Ei(i, e);
    },
    d(t) {
      t && Li(i);
    }
  };
}
function Oi(l) {
  let e, i;
  return e = new wi({
    props: {
      elem_id: (
        /*elem_id*/
        l[3]
      ),
      elem_classes: (
        /*elem_classes*/
        l[4]
      ),
      visible: (
        /*visible*/
        l[6]
      ),
      file_count: (
        /*file_count*/
        l[9]
      ),
      file_types: (
        /*file_types*/
        l[10]
      ),
      size: (
        /*size*/
        l[12]
      ),
      scale: (
        /*scale*/
        l[13]
      ),
      icon: (
        /*icon*/
        l[14]
      ),
      min_width: (
        /*min_width*/
        l[15]
      ),
      root: (
        /*root*/
        l[11]
      ),
      value: (
        /*value*/
        l[2]
      ),
      disabled: (
        /*disabled*/
        l[18]
      ),
      variant: (
        /*variant*/
        l[16]
      ),
      label: (
        /*label*/
        l[1]
      ),
      oldLabel: (
        /*oldLabel*/
        l[7]
      ),
      interactive: (
        /*interactive*/
        l[0]
      ),
      oldInteractive: (
        /*oldInteractive*/
        l[8]
      ),
      loading_message: (
        /*loading_message*/
        l[5]
      ),
      max_file_size: (
        /*gradio*/
        l[17].max_file_size
      ),
      upload: (
        /*gradio*/
        l[17].client.upload
      ),
      $$slots: { default: [Ni] },
      $$scope: { ctx: l }
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[22]
  ), e.$on(
    "change",
    /*change_handler*/
    l[23]
  ), e.$on(
    "upload",
    /*upload_handler*/
    l[24]
  ), e.$on(
    "labelChange",
    /*handle_label_change*/
    l[20]
  ), e.$on(
    "interactiveChange",
    /*handle_interactive_change*/
    l[21]
  ), e.$on(
    "error",
    /*error_handler*/
    l[25]
  ), {
    c() {
      Ii(e.$$.fragment);
    },
    l(t) {
      zi(e.$$.fragment, t);
    },
    m(t, n) {
      Ti(e, t, n), i = !0;
    },
    p(t, [n]) {
      const a = {};
      n & /*elem_id*/
      8 && (a.elem_id = /*elem_id*/
      t[3]), n & /*elem_classes*/
      16 && (a.elem_classes = /*elem_classes*/
      t[4]), n & /*visible*/
      64 && (a.visible = /*visible*/
      t[6]), n & /*file_count*/
      512 && (a.file_count = /*file_count*/
      t[9]), n & /*file_types*/
      1024 && (a.file_types = /*file_types*/
      t[10]), n & /*size*/
      4096 && (a.size = /*size*/
      t[12]), n & /*scale*/
      8192 && (a.scale = /*scale*/
      t[13]), n & /*icon*/
      16384 && (a.icon = /*icon*/
      t[14]), n & /*min_width*/
      32768 && (a.min_width = /*min_width*/
      t[15]), n & /*root*/
      2048 && (a.root = /*root*/
      t[11]), n & /*value*/
      4 && (a.value = /*value*/
      t[2]), n & /*disabled*/
      262144 && (a.disabled = /*disabled*/
      t[18]), n & /*variant*/
      65536 && (a.variant = /*variant*/
      t[16]), n & /*label*/
      2 && (a.label = /*label*/
      t[1]), n & /*oldLabel*/
      128 && (a.oldLabel = /*oldLabel*/
      t[7]), n & /*interactive*/
      1 && (a.interactive = /*interactive*/
      t[0]), n & /*oldInteractive*/
      256 && (a.oldInteractive = /*oldInteractive*/
      t[8]), n & /*loading_message*/
      32 && (a.loading_message = /*loading_message*/
      t[5]), n & /*gradio*/
      131072 && (a.max_file_size = /*gradio*/
      t[17].max_file_size), n & /*gradio*/
      131072 && (a.upload = /*gradio*/
      t[17].client.upload), n & /*$$scope, label, gradio*/
      134348802 && (a.$$scope = { dirty: n, ctx: t }), e.$set(a);
    },
    i(t) {
      i || (Gi(e.$$.fragment, t), i = !0);
    },
    o(t) {
      Mi(e.$$.fragment, t), i = !1;
    },
    d(t) {
      yi(e, t);
    }
  };
}
function Ui(l, e, i) {
  let t;
  var n = this && this.__awaiter || function(r, Y, A, F) {
    function _(v) {
      return v instanceof A ? v : new A(function(k) {
        k(v);
      });
    }
    return new (A || (A = Promise))(function(v, k) {
      function I(y) {
        try {
          T(F.next(y));
        } catch (Z) {
          k(Z);
        }
      }
      function M(y) {
        try {
          T(F.throw(y));
        } catch (Z) {
          k(Z);
        }
      }
      function T(y) {
        y.done ? v(y.value) : _(y.value).then(I, M);
      }
      T((F = F.apply(r, Y || [])).next());
    });
  };
  let { elem_id: a = "" } = e, { elem_classes: d = [] } = e, { loading_message: c } = e, { visible: f = !0 } = e, { label: s } = e, { oldLabel: o } = e, { interactive: u } = e, { oldInteractive: m } = e, { value: b } = e, { file_count: L } = e, { file_types: S = [] } = e, { root: q } = e, { size: h = "lg" } = e, { scale: H = null } = e, { icon: J = null } = e, { min_width: K = void 0 } = e, { variant: P = "secondary" } = e, { gradio: E } = e;
  function U(r, Y) {
    return n(this, void 0, void 0, function* () {
      i(2, b = r), E.dispatch(Y);
    });
  }
  function G(r) {
    i(1, s = r.detail);
  }
  function Q(r) {
    i(0, u = r.detail);
  }
  const z = () => E.dispatch("click"), W = ({ detail: r }) => U(r, "change"), X = ({ detail: r }) => U(r, "upload"), ae = ({ detail: r }) => {
    E.dispatch("error", r);
  };
  return l.$$set = (r) => {
    "elem_id" in r && i(3, a = r.elem_id), "elem_classes" in r && i(4, d = r.elem_classes), "loading_message" in r && i(5, c = r.loading_message), "visible" in r && i(6, f = r.visible), "label" in r && i(1, s = r.label), "oldLabel" in r && i(7, o = r.oldLabel), "interactive" in r && i(0, u = r.interactive), "oldInteractive" in r && i(8, m = r.oldInteractive), "value" in r && i(2, b = r.value), "file_count" in r && i(9, L = r.file_count), "file_types" in r && i(10, S = r.file_types), "root" in r && i(11, q = r.root), "size" in r && i(12, h = r.size), "scale" in r && i(13, H = r.scale), "icon" in r && i(14, J = r.icon), "min_width" in r && i(15, K = r.min_width), "variant" in r && i(16, P = r.variant), "gradio" in r && i(17, E = r.gradio);
  }, l.$$.update = () => {
    l.$$.dirty & /*interactive*/
    1 && i(18, t = !u);
  }, [
    u,
    s,
    b,
    a,
    d,
    c,
    f,
    o,
    m,
    L,
    S,
    q,
    h,
    H,
    J,
    K,
    P,
    E,
    t,
    U,
    G,
    Q,
    z,
    W,
    X,
    ae
  ];
}
class Ai extends ki {
  constructor(e) {
    super(), qi(this, e, Ui, Oi, Di, {
      elem_id: 3,
      elem_classes: 4,
      loading_message: 5,
      visible: 6,
      label: 1,
      oldLabel: 7,
      interactive: 0,
      oldInteractive: 8,
      value: 2,
      file_count: 9,
      file_types: 10,
      root: 11,
      size: 12,
      scale: 13,
      icon: 14,
      min_width: 15,
      variant: 16,
      gradio: 17
    });
  }
}
export {
  wi as BaseUploadButton,
  Ai as default
};
