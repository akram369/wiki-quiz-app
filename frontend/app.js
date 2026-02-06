const API = "http://127.0.0.1:8000";

/* ---------- GLOBAL STATE ---------- */
let CURRENT_QUIZ = [];

/* ---------- TABS ---------- */
function showTab(tab, btn) {
  document.querySelectorAll(".tab").forEach(t => t.classList.add("hidden"));
  document.querySelectorAll(".tabs button").forEach(b => b.classList.remove("active"));
  document.getElementById(tab).classList.remove("hidden");
  btn.classList.add("active");
  if (tab === "history") loadHistory();
}

/* ---------- GENERATE QUIZ ---------- */
async function generateQuiz() {
  const url = document.getElementById("wikiUrl").value;
  if (!url) return alert("Enter Wikipedia URL");

  const res = await fetch(
    `${API}/quiz/generate?url=${encodeURIComponent(url)}`,
    { method: "POST" }
  );

  const data = await res.json();
  renderQuiz(data, "quizResult");
}

/* ---------- RENDER QUIZ ---------- */
function renderQuiz(data, containerId) {
  CURRENT_QUIZ = data.quiz;

  const c = document.getElementById(containerId);
  c.innerHTML = `
    <h2>${data.title}</h2>
    <p>${data.summary}</p>
    <p><b>Cached:</b> ${data.cached}</p>

    <h3>Take Quiz</h3>
    <form id="quizForm"></form>

    <button type="button" id="submitBtn" onclick="submitQuiz()">
      Submit Quiz
    </button>

    <div id="scoreBox"></div>

    <h3>Related Topics</h3>
    <ul>${data.related_topics.map(t => `<li>${t}</li>`).join("")}</ul>
  `;

  const form = document.getElementById("quizForm");

  data.quiz.forEach((q, i) => {
    form.innerHTML += `
      <div class="quiz-card">
        <h4>Q${i + 1}. ${q.question}</h4>

        ${q.options.map(o => `
          <label>
            <input type="radio" name="q${i}" value="${o}">
            ${o}
          </label><br>
        `).join("")}

        <p class="answer hidden">
          ✅ <b>Answer:</b> ${q.answer}<br>
          <i>${q.explanation}</i>
        </p>
      </div>
    `;
  });
}

/* ---------- SUBMIT QUIZ ---------- */
function submitQuiz() {
  let score = 0;

  CURRENT_QUIZ.forEach((q, i) => {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);
    if (selected && selected.value === q.answer) score++;
  });

  // reveal answers
  document.querySelectorAll(".answer").forEach(a =>
    a.classList.remove("hidden")
  );

  document.getElementById("scoreBox").innerHTML =
    `<h3>🎯 Your Score: ${score} / ${CURRENT_QUIZ.length}</h3>`;

  // disable resubmission
  document.getElementById("submitBtn").disabled = true;
}

/* ---------- HISTORY ---------- */
async function loadHistory() {
  const res = await fetch(`${API}/quiz/history`);
  const data = await res.json();

  const table = document.getElementById("historyTable");
  table.innerHTML = "";

  data.forEach(a => {
    table.innerHTML += `
      <tr>
        <td>${a.title}</td>
        <td><a href="${a.url}" target="_blank">Link</a></td>
        <td>
          <button onclick="viewDetails('${a.url}')">Details</button>
        </td>
      </tr>
    `;
  });
}

/* ---------- MODAL ---------- */
async function viewDetails(url) {
  const res = await fetch(
    `${API}/quiz/generate?url=${encodeURIComponent(url)}`,
    { method: "POST" }
  );
  const data = await res.json();
  renderQuiz(data, "modalBody");
  document.getElementById("modal").classList.remove("hidden");
}

function closeModal() {
  document.getElementById("modal").classList.add("hidden");
}
