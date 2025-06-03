const sheet = document.getElementById("a4-sheet");
const exportBtn = document.getElementById("exportBtn");
const jsonOutput = document.getElementById("json-output");

document.querySelectorAll(".toolbar button[data-type]").forEach((btn) => {
  btn.addEventListener("click", () => addElement(btn.dataset.type));
});

let elements = [];

function addElement(type) {
  const el = document.createElement("div");
  el.classList.add("draggable");
  el.setAttribute("draggable", true);
  el.style.position = "absolute";

  let content = "";
  let inputType = "";

  switch (type) {
    case "text":
      content = "Texte";
      el.innerText = content;
      // Permettre l'édition sur double-clic
      el.addEventListener("dblclick", function () {
        const currentText = el.innerText;
        const input = document.createElement("input");
        input.type = "text";
        input.value = currentText;
        input.style.width = "90%";
        el.innerHTML = "";
        el.appendChild(input);
        input.focus();
        // Sauvegarder le texte modifié
        function saveEdit() {
          el.innerText = input.value;
          // Mettre à jour le contenu dans elements
          const found = elements.find((e) => e.dom === el);
          if (found) {
            found.data.content = input.value;
          }
        }
        input.addEventListener("blur", saveEdit);
        input.addEventListener("keydown", function (e) {
          if (e.key === "Enter") {
            input.blur();
          }
        });
      });
      break;
    case "input":
      content = "Champ";
      el.innerHTML = `<input type="text" placeholder="Texte">`;
      inputType = "text";
      break;
    case "checkbox":
      content = "Case";
      el.innerHTML = `<input type="checkbox">`;
      inputType = "checkbox";
      break;
    case "image":
      content = ""; // Par défaut, pas de base64
      // Créer un input pour l'import local
      el.innerHTML = `<img src="assets/default-image.png" width="50"><br><input type="file" accept="image/*" style="display:none">`;
      const img = el.querySelector("img");
      const fileInput = el.querySelector("input[type='file']");
      // Afficher le sélecteur de fichier au double-clic
      el.addEventListener("dblclick", () => fileInput.click());
      // Stocker le base64 dans l'objet data
      let imageBase64 = null;
      fileInput.addEventListener("change", function (e) {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function (evt) {
            img.src = evt.target.result;
            imageBase64 = evt.target.result.split(",")[1]; // enlever le préfixe data:image/xxx;base64,
            // Mettre à jour le contenu dans elements
            const found = elements.find((e) => e.dom === el);
            if (found) {
              found.data.content = imageBase64;
            }
          };
          reader.readAsDataURL(file);
        }
      });
      break;
  }

  // Ajout du handle de redimensionnement
  const resizeHandle = document.createElement("div");
  resizeHandle.style.position = "absolute";
  resizeHandle.style.right = "0";
  resizeHandle.style.bottom = "0";
  resizeHandle.style.width = "12px";
  resizeHandle.style.height = "12px";
  resizeHandle.style.background = "#888";
  resizeHandle.style.cursor = "se-resize";
  resizeHandle.style.borderRadius = "2px";
  resizeHandle.style.zIndex = "10";
  el.appendChild(resizeHandle);

  // Position initiale
  el.style.left = "50px";
  el.style.top = "50px";
  el.style.width = "100px";
  el.style.height = "20px";

  // Redimensionnement
  resizeHandle.addEventListener("mousedown", function (e) {
    e.stopPropagation();
    e.preventDefault();
    const startX = e.clientX;
    const startY = e.clientY;
    const startWidth = parseInt(
      document.defaultView.getComputedStyle(el).width,
      10
    );
    const startHeight = parseInt(
      document.defaultView.getComputedStyle(el).height,
      10
    );
    function doDrag(ev) {
      const newWidth = Math.max(30, startWidth + ev.clientX - startX);
      const newHeight = Math.max(20, startHeight + ev.clientY - startY);
      el.style.width = newWidth + "px";
      el.style.height = newHeight + "px";
      // Mettre à jour l'objet data
      const found = elements.find((e) => e.dom === el);
      if (found) {
        found.data.width = newWidth;
        found.data.height = newHeight;
      }
      // Adapter le contenu interne
      if (type === "text") {
        el.style.lineHeight = newHeight + "px";
        el.style.wordBreak = "break-word";
        el.style.overflow = "hidden";
      } else if (type === "input") {
        const input = el.querySelector("input[type='text']");
        if (input) {
          input.style.width = newWidth - 8 + "px";
          input.style.height = newHeight - 8 + "px";
        }
      } else if (type === "checkbox") {
        const input = el.querySelector("input[type='checkbox']");
        if (input) {
          input.style.width = Math.min(newWidth - 8, 30) + "px";
          input.style.height = Math.min(newHeight - 8, 30) + "px";
        }
      } else if (type === "image") {
        const img = el.querySelector("img");
        if (img) {
          img.style.width = newWidth - 8 + "px";
          img.style.height = newHeight - 28 + "px";
        }
      }
    }
    function stopDrag() {
      document.removeEventListener("mousemove", doDrag);
      document.removeEventListener("mouseup", stopDrag);
    }
    document.addEventListener("mousemove", doDrag);
    document.addEventListener("mouseup", stopDrag);
  });

  sheet.appendChild(el);

  const obj = {
    element_type: type,
    content,
    x: 50,
    y: 50,
    width: 100,
    height: 20,
    input_type: inputType || undefined,
  };

  elements.push({ dom: el, data: obj });

  setupDrag(el, obj);
}

function setupDrag(el, data) {
  let offsetX = 0,
    offsetY = 0;

  el.addEventListener("dragstart", (e) => {
    const rect = el.getBoundingClientRect();
    offsetX = e.clientX - rect.left;
    offsetY = e.clientY - rect.top;
  });

  el.addEventListener("dragend", (e) => {
    const sheetRect = sheet.getBoundingClientRect();
    const x = e.clientX - sheetRect.left - offsetX;
    const y = e.clientY - sheetRect.top - offsetY;
    el.style.left = `${x}px`;
    el.style.top = `${y}px`;
    data.x = x;
    data.y = y;
  });
}

exportBtn.addEventListener("click", () => {
  const content = elements.map((e) => {
    // Pour les images, exporter le base64 directement (plus rapide)
    if (e.data.element_type === "image" && e.data.content) {
      return { ...e.data, content: e.data.content };
    }
    return e.data;
  });
  const json = {
    file_name: "template_a4",
    font: "Helvetica",
    font_size: 12,
    content,
  };
  jsonOutput.textContent = JSON.stringify(json, null, 2);

  try {
    response = fetch("http://localhost:8000/template", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(json),
    });
    response
      .then((res) => {
        if (!res.ok) {
          throw new Error("Network response was not ok");
        }
        return res.blob(); // <-- lire la réponse comme un blob (PDF)
      })
      .then((blob) => {
        if (!blob || blob.size === 0) {
          alert("Le PDF généré est vide ou la réponse est incorrecte.");
          console.error("Blob vide ou invalide", blob);
          return;
        }
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "template.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch((err) => {
        alert("Erreur lors du téléchargement du PDF : " + err);
        console.error("Erreur fetch ou téléchargement :", err);
      });
  } catch (error) {
    console.error("Error:", error);
  }
});
