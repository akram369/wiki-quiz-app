const API = "https://wiki-quiz-app-d4rz.onrender.com";

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
  const url = document.getElementById("wikiUrl").value.trim();
  const resultDiv = document.getElementById("quizResult");

  if (!url) {
    alert("Enter a Wikipedia URL");
    return;
  }

  resultDiv.innerHTML = "<p>⏳ Generating quiz, please wait...</p>";

  try {
    const res = await fetch(
      `${API}/quiz/generate?url=${encodeURIComponent(url)}`,
      { method: "POST" }
    );

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`API Error ${res.status}: ${text}`);
    }

    const data = await res.json();

    if (!data.quiz || data.quiz.length === 0) {
      throw new Error("No quiz data returned from API");
    }

    renderQuiz(data, "quizResult");

  } catch (err) {
    console.error(err);
    resultDiv.innerHTML = `
      <p style="color:red;">
        ❌ Failed to generate quiz.<br>
        ${err.message}
      </p>
    `;
  }
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

  document.querySelectorAll(".answer").forEach(a =>
    a.classList.remove("hidden")
  );

  document.getElementById("scoreBox").innerHTML =
    `<h3>🎯 Your Score: ${score} / ${CURRENT_QUIZ.length}</h3>`;

  document.getElementById("submitBtn").disabled = true;
}

/* ---------- HISTORY ---------- */
async function loadHistory() {
  const table = document.getElementById("historyTable");
  table.innerHTML = "<tr><td colspan='3'>Loading...</td></tr>";

  try {
    const res = await fetch(`${API}/quiz/history`);
    const data = await res.json();

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

  } catch (err) {
    table.innerHTML = "<tr><td colspan='3'>Failed to load history</td></tr>";
  }
}

/* ---------- MODAL ---------- */
async function viewDetails(url) {
  try {
    const res = await fetch(
      `${API}/quiz/generate?url=${encodeURIComponent(url)}`,
      { method: "POST" }
    );
    const data = await res.json();
    renderQuiz(data, "modalBody");
    document.getElementById("modal").classList.remove("hidden");
  } catch {
    alert("Failed to load quiz details");
  }
}

function closeModal() {
  document.getElementById("modal").classList.add("hidden");
}
