(function(){
  var panes = document.querySelectorAll(".pane");
  var rows  = document.querySelectorAll(".files a.row");
  var keys  = document.querySelectorAll(".fkeys a");
  var tab   = document.getElementById("curname");
  var line  = document.getElementById("curfile");
  var order = Array.prototype.map.call(keys, function(a){ return a.getAttribute("href").slice(1); });

  
  
  function playRace(){
    document.querySelectorAll("#perf .lane").forEach(function(lane){
      var fill = lane.querySelector(".bar span"), el = lane.querySelector(".t[data-to]");
      if (fill) { fill.style.animation = "none"; void fill.offsetWidth; fill.style.animation = ""; }
      if (!el) return;
      var to = parseFloat(el.dataset.to), ms = parseFloat(el.dataset.d) * 1000, t0 = 0;
      function step(now){
        if (!t0) t0 = now;
        var p = Math.min(1, (now - t0) / ms);
        el.textContent = (to * p).toFixed(2) + " s";
        if (p < 1) requestAnimationFrame(step);
      }
      el.textContent = "0.00 s";
      requestAnimationFrame(step);
    });
  }

  function open(id){
    var found = false;
    panes.forEach(function(pane){
      var on = pane.id === id;
      pane.classList.toggle("on", on);
      if (on) found = true;
    });
    if (!found) return false;
    var name = "";
    rows.forEach(function(a){
      var on = a.getAttribute("href") === "#" + id;
      a.classList.toggle("on", on);
      a.setAttribute("aria-current", on ? "true" : "false");
      if (on) name = a.querySelector(".c1").textContent;
    });
    keys.forEach(function(a){
      a.classList.toggle("on", a.getAttribute("href") === "#" + id);
    });
    rows.forEach(function(a, n){ if (a.getAttribute("href") === "#" + id) cursor = n; });
    if (tab) tab.textContent = name;
    if (line) line.textContent = name;
    var view = document.querySelector(".view");
    if (view) view.scrollTop = 0;
    if (id === "perf" && !matchMedia("(prefers-reduced-motion: reduce)").matches) playRace();
    return true;
  }

  
  
  var cursor = -1;
  function step(by){
    if (!rows.length) return;
    var n = (cursor < 0 ? (by > 0 ? 0 : rows.length - 1) : cursor + by);
    n = (n + rows.length) % rows.length;
    var id = rows[n].getAttribute("href").slice(1);
    if (open(id)) { history.replaceState(null, "", "#" + id); rows[n].focus(); }
  }

  function pick(e){
    var id = this.getAttribute("href").slice(1);
    if (open(id)) { e.preventDefault(); history.replaceState(null, "", "#" + id); }
  }
  rows.forEach(function(a){ a.addEventListener("click", pick); });
  keys.forEach(function(a){ a.addEventListener("click", pick); });

  addEventListener("keydown", function(e){
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      var el = document.activeElement;
      var inList = !!(el && el.classList && el.classList.contains("row"));
      
      
      if (!inList && el && el !== document.body && el !== document.documentElement) return;
      e.preventDefault();
      step(e.key === "ArrowDown" ? 1 : -1);
      return;
    }

    if (e.shiftKey) return;
    
    var m = /^F([1-7])$/.exec(e.key);
    if (!m) return;
    var id = order[parseInt(m[1], 10) - 1];
    if (id && open(id)) e.preventDefault();
  });
  addEventListener("hashchange", function(){ open(location.hash.slice(1)); });

  open(location.hash.slice(1)) || open("readme");
})();
