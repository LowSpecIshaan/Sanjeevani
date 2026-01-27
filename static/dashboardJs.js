let activeSection = null; // track which section is open

document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.getElementById("hamburger");
  const navLinks = document.getElementById("navLinks");

  // Hamburger menu toggle
  hamburger.addEventListener("click", (e) => {
    e.stopPropagation();
    navLinks.classList.toggle("active");
  });

  // Close menu when clicking outside
  document.addEventListener("click", (e) => {
    if (navLinks.classList.contains("active") && !navLinks.contains(e.target)) {
      navLinks.classList.remove("active");
    }
  });

  // Prevent clicks inside navLinks from closing it
  navLinks.addEventListener("click", (e) => e.stopPropagation());

  // Mobile dropdown toggle (like Language menu)
  document.querySelectorAll(".dropdown > a").forEach(item => {
    item.addEventListener("click", (e) => {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        item.parentElement.classList.toggle("open");
      }
    });
  });
});

// Show section dynamically
function showSection(section) {
  const content = document.getElementById("content");
  if (activeSection === section) {
    content.innerHTML = "";
    activeSection = null;
    return;
  }
  activeSection = section;
  content.innerHTML = ""; // Clear previous content

  if (section === "medical") {
    content.innerHTML = `
    <h3 class="section-title">Medical History</h3>
    <div class="table-container">
      <table id="medicalTable">
        <thead>
          <tr>
            <th>Date</th>
            <th>Condition</th>
            <th>Notes</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="medicalBody"></tbody>
      </table>
    </div>

    <button id="openFormBtn" class="btn">+ Add Record</button>

    <!-- Add Modal -->
    <div id="formModal" class="modal">
      <div class="modal-content">
        <span id="closeModal" class="close">&times;</span>
        <h3>Add Medical Record</h3>
        <form id="medicalForm">
          <label>Date:</label>
          <input type="date" name="date_diagnosed" required>
          <label>Condition:</label>
          <input type="text" name="condition" required>
          <label>Details:</label>
          <input type="text" name="details">
          <button type="submit" class="btn">Save</button>
        </form>
      </div>
    </div>

    <!-- Edit Modal -->
    <div id="editModal" class="modal">
      <div class="modal-content">
        <span id="closeEditModal" class="close">&times;</span>
        <h3>Edit Medical Record</h3>
        <form id="editForm">
          <input type="hidden" name="id">
          <label>Date:</label>
          <input type="date" name="date_diagnosed" required>
          <label>Condition:</label>
          <input type="text" name="condition" required>
          <label>Details:</label>
          <input type="text" name="details">
          <button type="submit" class="btn">Update</button>
        </form>
      </div>
    </div>
    `;

    const medicalBody = document.getElementById("medicalBody");
    const formModal = document.getElementById("formModal");
    const editModal = document.getElementById("editModal");
    const medicalForm = document.getElementById("medicalForm");
    const editForm = document.getElementById("editForm");

    // Open Add Modal
    document.getElementById("openFormBtn").onclick = () => formModal.style.display = "flex";

    // Close Modals
    document.getElementById("closeModal").onclick = () => formModal.style.display = "none";
    document.getElementById("closeEditModal").onclick = () => editModal.style.display = "none";

    // Add Record
    medicalForm.onsubmit = (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(e.target).entries());
      fetch("/api/medical-history", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
        .then(res => res.json())
        .then(newRecord => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${newRecord.date_diagnosed || ""}</td>
            <td>${newRecord.condition}</td>
            <td>${newRecord.details || ""}</td>
            <td>
              <button class="btn edit-btn" data-id="${newRecord.id}">Edit</button>
              <button class="btn delete-btn" data-id="${newRecord.id}">Delete</button>
            </td>
          `;
          medicalBody.appendChild(row);
          formModal.style.display = "none";
          e.target.reset();
        });
    };

    // Fetch existing records
    fetch("/api/medical-history")
      .then(res => res.json())
      .then(data => {
        medicalBody.innerHTML = "";
        data.forEach(row => {
          medicalBody.innerHTML += `
            <tr>
              <td>${row.date_diagnosed || ""}</td>
              <td>${row.condition}</td>
              <td>${row.details || ""}</td>
              <td>
                <button class="btn edit-btn" data-id="${row.id}">Edit</button>
                <button class="btn delete-btn" data-id="${row.id}">Delete</button>
              </td>
            </tr>
          `;
        });
      });

    // Event delegation for Edit & Delete buttons
    medicalBody.addEventListener("click", (e) => {
      const target = e.target;
      const row = target.closest("tr");
      const id = target.dataset.id;

      if (target.classList.contains("edit-btn")) {
        editForm.id.value = id;
        editForm.date_diagnosed.value = row.children[0].innerText;
        editForm.condition.value = row.children[1].innerText;
        editForm.details.value = row.children[2].innerText;
        editModal.style.display = "flex";
      }

      if (target.classList.contains("delete-btn")) {
        fetch(`/api/medical-history/${id}`, { method: "DELETE" })
          .then(res => res.json())
          .then(() => row.remove());
      }
    });

    // Handle Edit form submit
    editForm.onsubmit = (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(e.target).entries());
      const id = data.id;
      delete data.id;

      fetch(`/api/medical-history/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      })
        .then(res => res.json())
        .then(updated => {
          const row = medicalBody.querySelector(`button.edit-btn[data-id="${id}"]`).closest("tr");
          row.children[0].innerText = updated.date_diagnosed || "";
          row.children[1].innerText = updated.condition;
          row.children[2].innerText = updated.details || "";
          editModal.style.display = "none";
        });
    };

  } else if (section === "support") {
    content.innerHTML = `
    <h3 class="section-title">AI Healthcare Support</h3>
    <div id="chatbox" style="border:1px solid #ccc; border-radius:8px; padding:10px; height:400px; overflow-y:auto; background:white; margin-bottom:10px;"></div>
    <div style="display:flex; gap:10px; align-items: flex-start;">
      <input id="userInput" type="text" placeholder="Type your question..." style="flex:1; padding:8px; border-radius:6px; border:1px solid #ccc;">
      <button onclick="sendMessage()" style="padding:8px 15px; border:none; border-radius:6px; background:#3EAFE3; color:white;">Send</button>
    </div>
  `;
  } else if (section === "reminders") {
    content.innerHTML = `<h3>Reminders</h3><ul><li>Take BP medicine - 8 AM</li><li>Doctor visit - Sept 20</li></ul>`;
  } else if (section === "documents") {
    content.innerHTML = `<h3>Emergency</h3>
  <p>Select an action:</p>
  <ul style="list-style:none; padding:0;">
    <li style="margin:10px 0;">
      <button onclick="window.location.href='tel:102'" 
              style="width:100%; padding:50px; background:#dc2626; color:white; border:none; border-radius:6px; font-size:40px;">
        Call Ambulance
      </button>
    </li>
    <li style="margin:10px 0;">
      <button onclick="window.location.href='sms:+919876543210?body=I need help!!'" 
              style="width:100%; padding:50px; background:#f97316; color:white; border:none; border-radius:6px; font-size:40px;">
        Send Emergency SMS
      </button>
    </li>
  </ul>`;
  }

  content.scrollIntoView({ behavior: "smooth", block: "start" });
}

function sendMessage() {
  const input = document.getElementById("userInput");
  const chatbox = document.getElementById("chatbox");
  const message = input.value.trim();

  if (!message) return;

  // Show user message
  chatbox.innerHTML += `<div style="display: inline-block; float:right; word-break: break-word; max-width: 70%; text-align:right; margin:5px; background: #ffb143ff; padding:6px; border-radius:12px"><b>You:</b> ${message}</div>`;
  input.value = "";

  // Call backend API (Flask) to get AI reply
  fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
    .then(res => res.json())
    .then(data => {
      chatbox.innerHTML += `<div style="display: inline-block; float:left; word-break: break-word; max-width: 70%; text-align:left; margin:5px; background: #dfdbdfff; padding:6px; border-radius:12px"><b>AI:</b> ${data.reply}</div>`;
      chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(err => {
      chatbox.innerHTML += `<div style="text-align:left; margin:5px; color:red;"><b>Error:</b> Could not connect.</div>`;
    });
}


// Hero slider
let current = 0;
const slides = document.querySelectorAll('.hero-image img');
const total = slides.length;

function showSlide(index) {
  slides.forEach((img, i) => img.classList.toggle('active', i === index));
}

setInterval(() => {
  current = (current + 1) % total;
  showSlide(current);
}, 4000);

showSlide(current);
