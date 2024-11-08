const {
  SvelteComponent: P,
  append: d,
  attr: k,
  destroy_each: F,
  detach: O,
  element: m,
  empty: x,
  ensure_array_like: T,
  flush: G,
  init: $,
  insert: M,
  listen: A,
  noop: E,
  run_all: ee,
  safe_not_equal: te,
  set_data: Y,
  set_input_value: ne,
  space: V,
  text: I,
  toggle_class: H
} = window.__gradio__svelte__internal, { tick: K } = window.__gradio__svelte__internal;
function L(n, e, t) {
  const o = n.slice();
  return o[16] = e[t], o;
}
function Q(n, e, t) {
  const o = n.slice();
  return o[19] = e[t], o;
}
function le(n) {
  let e, t = (
    /*pageNumber*/
    n[19] + ""
  ), o, c, s;
  function _() {
    return (
      /*click_handler_1*/
      n[11](
        /*pageNumber*/
        n[19]
      )
    );
  }
  return {
    c() {
      e = m("button"), o = I(t), k(e, "class", "page-button svelte-1bca5rq"), H(
        e,
        "selected",
        /*page*/
        n[1] === /*pageNumber*/
        n[19]
      );
    },
    m(u, f) {
      M(u, e, f), d(e, o), c || (s = A(e, "click", _), c = !0);
    },
    p(u, f) {
      n = u, f & /*page, max_page*/
      10 && t !== (t = /*pageNumber*/
      n[19] + "") && Y(o, t), f & /*page, paginationRange, max_page*/
      10 && H(
        e,
        "selected",
        /*page*/
        n[1] === /*pageNumber*/
        n[19]
      );
    },
    d(u) {
      u && O(e), c = !1, s();
    }
  };
}
function ie(n) {
  let e;
  return {
    c() {
      e = m("span"), e.textContent = "...", k(e, "class", "dots svelte-1bca5rq");
    },
    m(t, o) {
      M(t, e, o);
    },
    p: E,
    d(t) {
      t && O(e);
    }
  };
}
function U(n) {
  let e;
  function t(s, _) {
    return (
      /*pageNumber*/
      s[19] === "..." ? ie : le
    );
  }
  let o = t(n), c = o(n);
  return {
    c() {
      c.c(), e = x();
    },
    m(s, _) {
      c.m(s, _), M(s, e, _);
    },
    p(s, _) {
      o === (o = t(s)) && c ? c.p(s, _) : (c.d(1), c = o(s), c && (c.c(), c.m(e.parentNode, e)));
    },
    d(s) {
      s && O(e), c.d(s);
    }
  };
}
function W(n) {
  let e, t = (
    /*size*/
    n[16] + ""
  ), o, c, s;
  return {
    c() {
      e = m("option"), o = I(t), c = I(" per page"), e.__value = /*size*/
      n[16], ne(e, e.__value), e.selected = s = /*size*/
      n[16] === /*page_size*/
      n[2];
    },
    m(_, u) {
      M(_, e, u), d(e, o), d(e, c);
    },
    p(_, u) {
      u & /*page_size*/
      4 && s !== (s = /*size*/
      _[16] === /*page_size*/
      _[2]) && (e.selected = s);
    },
    d(_) {
      _ && O(e);
    }
  };
}
function se(n) {
  let e, t, o, c, s, _, u, f, g, j, w, v, y, S, C, q, J, R, a = T(X(
    /*page*/
    n[1],
    /*max_page*/
    n[3]
  )), r = [];
  for (let i = 0; i < a.length; i += 1)
    r[i] = U(Q(n, a, i));
  let b = T(
    /*page_size_options*/
    n[4]
  ), h = [];
  for (let i = 0; i < b.length; i += 1)
    h[i] = W(L(n, b, i));
  return {
    c() {
      e = m("div"), t = m("span"), o = I("Total "), c = I(
        /*total*/
        n[0]
      ), s = I(" Items"), _ = V(), u = m("button"), f = m("div"), j = V();
      for (let i = 0; i < r.length; i += 1)
        r[i].c();
      w = V(), v = m("button"), y = m("div"), C = V(), q = m("select");
      for (let i = 0; i < h.length; i += 1)
        h[i].c();
      k(t, "class", "total svelte-1bca5rq"), k(f, "class", "arrow-prev svelte-1bca5rq"), k(u, "class", "nav-button svelte-1bca5rq"), u.disabled = g = /*page*/
      n[1] === 1, k(y, "class", "arrow-next svelte-1bca5rq"), k(v, "class", "nav-button svelte-1bca5rq"), v.disabled = S = /*page*/
      n[1] === /*max_page*/
      n[3] || /*max_page*/
      n[3] <= 0, k(q, "class", "page-size-selector svelte-1bca5rq"), k(e, "class", "pagination svelte-1bca5rq");
    },
    m(i, p) {
      M(i, e, p), d(e, t), d(t, o), d(t, c), d(t, s), d(e, _), d(e, u), d(u, f), d(e, j);
      for (let l = 0; l < r.length; l += 1)
        r[l] && r[l].m(e, null);
      d(e, w), d(e, v), d(v, y), d(e, C), d(e, q);
      for (let l = 0; l < h.length; l += 1)
        h[l] && h[l].m(q, null);
      J || (R = [
        A(
          u,
          "click",
          /*click_handler*/
          n[10]
        ),
        A(
          v,
          "click",
          /*click_handler_2*/
          n[12]
        ),
        A(
          q,
          "change",
          /*handle_page_size_change*/
          n[7]
        )
      ], J = !0);
    },
    p(i, [p]) {
      if (p & /*total*/
      1 && Y(
        c,
        /*total*/
        i[0]
      ), p & /*page*/
      2 && g !== (g = /*page*/
      i[1] === 1) && (u.disabled = g), p & /*paginationRange, page, max_page, handle_page_click, Number*/
      42) {
        a = T(X(
          /*page*/
          i[1],
          /*max_page*/
          i[3]
        ));
        let l;
        for (l = 0; l < a.length; l += 1) {
          const z = Q(i, a, l);
          r[l] ? r[l].p(z, p) : (r[l] = U(z), r[l].c(), r[l].m(e, w));
        }
        for (; l < r.length; l += 1)
          r[l].d(1);
        r.length = a.length;
      }
      if (p & /*page, max_page*/
      10 && S !== (S = /*page*/
      i[1] === /*max_page*/
      i[3] || /*max_page*/
      i[3] <= 0) && (v.disabled = S), p & /*page_size_options, page_size*/
      20) {
        b = T(
          /*page_size_options*/
          i[4]
        );
        let l;
        for (l = 0; l < b.length; l += 1) {
          const z = L(i, b, l);
          h[l] ? h[l].p(z, p) : (h[l] = W(z), h[l].c(), h[l].m(q, null));
        }
        for (; l < h.length; l += 1)
          h[l].d(1);
        h.length = b.length;
      }
    },
    i: E,
    o: E,
    d(i) {
      i && O(e), F(r, i), F(h, i), J = !1, ee(R);
    }
  };
}
function X(n, e) {
  const t = [];
  if (e <= 0) return t;
  const o = 2, c = Math.max(2, n - o), s = Math.min(e - 1, n + o);
  c > 2 ? t.push(1, "...") : t.push(1);
  for (let _ = c; _ <= s; _++)
    t.push(_);
  return s < e - 1 ? t.push("...", e) : s === e - 1 && t.push(e), t;
}
function oe(n, e, t) {
  var o = this && this.__awaiter || function(a, r, b, h) {
    function i(p) {
      return p instanceof b ? p : new b(function(l) {
        l(p);
      });
    }
    return new (b || (b = Promise))(function(p, l) {
      function z(N) {
        try {
          B(h.next(N));
        } catch (D) {
          l(D);
        }
      }
      function Z(N) {
        try {
          B(h.throw(N));
        } catch (D) {
          l(D);
        }
      }
      function B(N) {
        N.done ? p(N.value) : i(N.value).then(z, Z);
      }
      B((h = h.apply(a, r || [])).next());
    });
  };
  let { gradio: c } = e, { value: s = "" } = e;
  const _ = (a) => {
    try {
      return JSON.parse(a || "{}");
    } catch (r) {
      return console.log(r), { total: 0, page: 1, page_size: 10 };
    }
  };
  let u = 0, f = 1, g = 10;
  const j = [10, 20, 50, 100];
  let w;
  function v(a) {
    a !== f && (t(1, f = a), t(8, s = JSON.stringify({ total: u, page: f, page_size: g })));
  }
  function y(a) {
    const r = f + a;
    r >= 1 && r <= w && (t(1, f = r), t(8, s = JSON.stringify({ total: u, page: f, page_size: g })));
  }
  function S(a) {
    return o(this, void 0, void 0, function* () {
      const r = parseInt(a.target.value);
      r !== g && (t(2, g = r), t(1, f = 1), yield K(), t(8, s = JSON.stringify({ total: u, page: f, page_size: g })));
    });
  }
  function C() {
    return o(this, void 0, void 0, function* () {
      const a = _(s);
      t(0, u = a.total), t(1, f = a.page), t(2, g = a.page_size), t(3, w = Math.ceil(u / g)), console.log("max_page", w, u, f, g), yield K(), c.dispatch("change");
    });
  }
  const q = () => y(-1), J = (a) => v(Number(a)), R = () => y(1);
  return n.$$set = (a) => {
    "gradio" in a && t(9, c = a.gradio), "value" in a && t(8, s = a.value);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    256 && C();
  }, [
    u,
    f,
    g,
    w,
    j,
    v,
    y,
    S,
    s,
    c,
    q,
    J,
    R
  ];
}
class ce extends P {
  constructor(e) {
    super(), $(this, e, oe, se, te, { gradio: 9, value: 8 });
  }
  get gradio() {
    return this.$$.ctx[9];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), G();
  }
  get value() {
    return this.$$.ctx[8];
  }
  set value(e) {
    this.$$set({ value: e }), G();
  }
}
export {
  ce as default
};
