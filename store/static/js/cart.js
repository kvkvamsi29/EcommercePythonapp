(function () {
  if (window.__cartJSLoaded) {
    console.warn("cart.js already loaded");
    return;
  }
  window.__cartJSLoaded = true;



  function updateCartBadge(count) {
    const badge = document.getElementById("cartBadge");
    if (!badge) return;

    badge.innerText = count;

    badge.classList.add("bump");
    setTimeout(() => badge.classList.remove("bump"), 200);
  }

  document.addEventListener("click", function (e) {
    const btn = e.target.closest("[data-add-to-cart]");
    if (!btn) return;

    // 🛑 Block if already added
    if (btn.disabled) return;

    e.preventDefault();

    const productId = btn.dataset.addToCart;


    fetch(`/api/cart/add/${productId}/`, {
      headers: { "X-Requested-With": "XMLHttpRequest" }
    })
      .then(res => {
        if (!res.ok) throw new Error("Server error");
        return res.json();   // ✅ parse JSON
      })
      .then(data => {s
          window.location.reload();
        if (data.status === "ok") {
          updateCartBadge(data.count);

          // ✅ lock button
          btn.classList.add("in-cart", "added");
          btn.innerText = "✓ Product in Cart";
          btn.disabled = true;
            setTimeout(() => {
    btn.classList.remove("added");
   
  }, 400);

        }
      })
      .catch(err => console.error("❌ Cart error:", err));
  });

})();

document.addEventListener("click", function (e) {
  const btn = e.target.closest("[data-cart-action]");
  if (!btn) return;

  e.preventDefault();

  const productId = btn.dataset.productId;
  const action = btn.dataset.cartAction;

  fetch(`/cart/add/${productId}/?action=${action}`, {
    headers: {
      "X-Requested-With": "XMLHttpRequest"
    }
  })
    .then(res => res.json())
    .then(data => {
      if (data.status !== "ok") return;

      // ✅ Update cart badge
      const badge = document.getElementById("cartBadge");
      if (badge) badge.innerText = data.count;
      
      // ✅ Reload ONLY cart section (safe + fast)
      fetch(window.location.href)
        .then(r => r.text())
        .then(html => {
          const doc = new DOMParser().parseFromString(html, "text/html");
          const newCart = doc.querySelector(".cart-wrapper");
          const currentCart = document.querySelector(".cart-wrapper");
          if (newCart && currentCart) {
            currentCart.innerHTML = newCart.innerHTML;
          }
        });
    });
});
